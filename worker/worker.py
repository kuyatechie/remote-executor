#!/usr/bin/env python
import pika
import os
from lib.deserializer import Deserializer
from lib.executor import Executor
from lib.database import DatabaseConnector
from lib.diskspace import DiskSpaceUtility


MQ_HOSTNAME = os.getenv("MQ_HOSTNAME", "localhost")

executor = Executor()
ds = DiskSpaceUtility()
db = DatabaseConnector()

connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOSTNAME))


def callback(ch, method, properties, body):
    # Received
    print(" [x] Received %r" % body)
    # Deserialize
    deserializer = Deserializer(body)
    message = deserializer.get_message()
    # Check diskspace_before
    free_diskspace = ds.get_free_space()
    db.update_task_diskspace_before(message['uid'],free_diskspace)
    # Record start time
    db.update_task_start_time(message['uid'])
    # Execute Shell Script
    retcode = executor.execute(message['script'], message['arguments'], message['uid'])
    # Record end time
    db.update_task_finish_time(message['uid'])
    # Check diskspace_after
    free_diskspace = ds.get_free_space()
    db.update_task_diskspace_after(message['uid'],free_diskspace)
    # Record retcode
    db.update_task_retcode(message['uid'], retcode)
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)


def main():
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue='task_queue')
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()
