import json
import pika
import os

MQ_HOSTNAME = os.getenv("MQ_HOSTNAME", "localhost")


class MessageGenerator:
    def __init__(self, uid, script, arguments):
        self.uid = uid
        self.script = script
        self.arguments = arguments
        self.command = dict()

    def generate_args(self):
#        args = ""
        args = []
        for key, value in self.arguments.items():
#            args = args + key + " " + value + " "
            args.append(key)
            args.append(value)
        return args

    def generate_message(self):
        self.command['uid'] = str(self.uid)
        self.command['script'] = self.script
        self.command['arguments'] = self.generate_args()
        return json.dumps(self.command)


class Messenger:
    __instance = None

    def __new__(cls):
        if Messenger.__instance is None:
            Messenger.__instance = object.__new__(cls)
        return Messenger.__instance

    def submit(self, message):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOSTNAME))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='task_queue', durable=True)
        self.channel.basic_publish(exchange='',
                              routing_key="task_queue",
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,
                              ))
        self.connection.close()