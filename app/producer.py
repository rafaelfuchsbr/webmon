import sys
import time
import concurrent.futures
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

import logger
import config
from dbconnection import DBConnection 
from website import Website 
from checkentry import CheckEntry 

logger = logger.getLogger('producer')
config = config.config()
MAX_RETRY = 3

def publish(entry: CheckEntry, producer: KafkaProducer):
    """
    Publish message to kafka in yaml format.
    """
    logger.info(f"Sending message to kafka (topic: {config.kafka.topic})")
    msg = producer.send(config.kafka.topic, entry.getYaml().encode())
    logger.info(f"Message sent to kafka (topic: {config.kafka.topic}) - [{entry.getYaml()}]")

def getWebsites():
    """
    Get the list of website to check the availability.
    """
    sql = "select website_id from website"
    logger.debug(f"SQL query to get list of websites: {sql}")
    try:
        conn = DBConnection()
        cursor = conn.getCursor()
        cursor.execute(sql)
        websites = []
        logger.info(f"Found {cursor.rowcount} websites to monitor.")

        for row in cursor.fetchall():
            logger.info(f"Adding website with id [{row[0]}] to the list.")
            websites.append(Website(id=row[0]))
    except Exception as e:
        logger.error("Error while getting list of websites.", e)
    return websites

def start():
    logger.debug(f"Connecting to kafka as a producer - server: {config.kafka.server}:{config.kafka.port}")
    producer = None
    for x in range(MAX_RETRY):
        try:
            producer = KafkaProducer(
                bootstrap_servers=f"{config.kafka.server}:{config.kafka.port}",
                security_protocol="SSL",
                ssl_cafile=config.kafka.ssl.cafile,
                ssl_certfile=config.kafka.ssl.certfile,
                ssl_keyfile=config.kafka.ssl.keyfile
            )
            logger.info("Connected to kafka. Starting the producer.")
            break;
        except NoBrokersAvailable as e:
            logger.error("kafka.errors.NoBrokersAvailable - please check network connection or kakfa servers from config file.")

    if not producer:
        #it doesn's make sense to continue if we can't connect to kafka after a few tentatives
        logger.critical("Couldn't connect to kafka brokers")
        sys.exit(1);

    try:
        # infinite loop to process the availability checks forever until crtl+c or process/container is killed
        while True:
            try:
                websites = getWebsites()
            except Exception as e:
                # do not exit if the call fails... wait and try again as a regular new round of checks
                logger.error("Error while getting list of websites.", e)
                time.sleep(config.monitoring.interval)
                continue

            with concurrent.futures.ThreadPoolExecutor(max_workers=config.producer.threads) as pool:
                threads = {}
                for website in websites:
                    logger.info(f"Checking availablity of website - id: {website.id}, name: {website.name}")
                    # send the check to a new thread and wait for its response in a future object
                    threads[pool.submit(website.getCurrentAvailability)] = website

                # check for future objects to return
                for future in concurrent.futures.as_completed(threads):
                    website = threads[future]
                    try:
                        entry = future.result()
                        logger.info(f"Sending availability data thru kafka for website - id: {website.id}, name: {website.name}")
                        # use another thread to publish message to kafka
                        # here we are not waiting for the return
                        pool.submit(publish, entry, producer)
                    except Exception as exc:
                        logger.error(f"Error while publishing the message - {exc}")
                        #TODO: handle error with messages and reprocess
            
            logger.info("Flushing producer before waiting for next round of checks.")
            # make sure messages are sent before moving forward
            producer.flush()
            logger.info(f"Waiting {config.monitoring.interval} seconds before starting next round of checks.")
            time.sleep(config.monitoring.interval)
    except KeyboardInterrupt as e:
        # handle ctrl+c
        logger.warning("Producer process interrupted.", e)
        sys.exit(0)

if __name__ == "__main__":
        start()