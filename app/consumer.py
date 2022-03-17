import yaml
import sys
import concurrent.futures
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

import logger
import config
from website import Website
from checkentry import CheckEntry

logger = logger.getLogger('consumer')
config = config.config()
MAX_RETRY = 3
RETRY_INTERVAL = 5

def processMessage(msg):
    """
    Get entry object from the message and transform it to YAML object/dict.
    """
    try:
        yamlObj = yaml.load(msg.value, Loader=yaml.FullLoader)
        logger.info(f"Message received: {yamlObj}")
        entry = CheckEntry(**yamlObj)
        entry.save()
        logger.info(f"CheckEntry saved: {entry.__dict__}")
        return entry
    except Exception as e:
        logger.error("Exception when processing message.", exc_info=True)
        return None

def start():
    """
    Consumer main flow.
    Connect to kafka and wait for message...
    """
    logger.info(f"Connecting to kafka topic")
    consumer = None
    for x in range(MAX_RETRY):
        try:
            consumer = KafkaConsumer (
                  config.kafka.topic,
                  bootstrap_servers=f"{config.kafka.server}:{config.kafka.port}",
                  group_id=config.kafka.consumer.group,
                  security_protocol="SSL",
                  ssl_cafile=config.kafka.ssl.cafile,
                  ssl_certfile=config.kafka.ssl.certfile,
                  ssl_keyfile=config.kafka.ssl.keyfile
                )

            logger.info("Connected to kafka.")
        except NoBrokersAvailable as e:
            logger.error("kafka.errors.NoBrokersAvailable - please check network connection or kakfa servers from config file.")
            time.sleep(RETRY_INTERVAL)

    if not consumer:
        logger.critical("Couldn't connect to kafka brokers")
        sys.exit(1);

    logger.info("Waiting for messages...")

    try:
        # each message will be processed in a new thread
        #TODO: improve msg error handling, like reprocessing it or send to a dead letter queue
        for msg in consumer:
            logger.debug(f"Message received [key: {msg.key}, timestamp: {msg.timestamp}, topic: {msg.topic}, partition: {msg.partition}, offset: {msg.offset}], starting to process it.")
            with concurrent.futures.ThreadPoolExecutor(max_workers=config.consumer.threads) as pool:
                pool.submit(processMessage, msg)
    except KeyboardInterrupt:
        #handle ctrl+c
        logger.warning("Consumer processes interrupted")
        sys.exit(0)

if __name__ == "__main__":
    start()