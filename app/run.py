import consumer
import producer
import logger
import multiprocessing
import time
import initdb
import sys

logger = logger.getLogger('run')

def main():

    try:
        logger.info("Starting the database initilization...")
        initdb.init()
        logger.info("Database initialized. We should have enough data to run.")

        processes = []

        logger.info("Starting the consumer process.")
        # start a new process for the consumer
        p = multiprocessing.Process(target=consumer.start)
        processes.append(p)
        p.start()

        time.sleep(2)

        logger.info("Starting the producer process.")
        # start a new process for the producer
        p = multiprocessing.Process(target=producer.start)
        processes.append(p)
        p.start()
        
        logger.info("Waiting for the processes to end...")
        for process in processes:
            process.join()
            
    except KeyboardInterrupt:
        # handle ctrl+c
        logger.warning("Main process interrupted.")
        sys.exit(0)

if __name__ == "__main__":
    main()