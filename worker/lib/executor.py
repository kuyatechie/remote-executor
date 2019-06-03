import subprocess
import os

WORKER_SCRIPT_PATH = os.getenv("WORKER_SCRIPT_PATH", "/app/scripts")
WORKER_DIRECTORY_PATH = os.getenv("WORKER_DIRECTORY_PATH", "/homedir")
WORKER_STDOUT_PATH = os.getenv("WORKER_STDOUT_PATH", "/homedir/logs/executor")
WORKER_STDERR_PATH = os.getenv("WORKER_STDERR_PATH", "/homedir/logs/executor")
WORKER_ALLOW_SHELL = os.getenv("WORKER_ALLOW_SHELL", 1)


class Executor:
    def __init__(self, script_path=WORKER_SCRIPT_PATH):
        self.script_path = script_path
        self.script = ""
        self.arguments = ""

        if not os.path.exists(WORKER_STDOUT_PATH):
            os.makedirs(WORKER_STDOUT_PATH)

        if not os.path.exists(WORKER_STDERR_PATH):
            os.makedirs(WORKER_STDERR_PATH)

    def execute(self, script, arguments, uid):
        try:
            command = "{}/{}".format(self.script_path, script)
            if not os.path.isfile(command) and bool(WORKER_ALLOW_SHELL):
                command = script
            command_arguments = command + " " + " ".join(filter(None, arguments))
            print(" [x] Command: ", command_arguments)
            stdout_f = open(WORKER_STDOUT_PATH + "/" + uid + "_stdout.log", 'w+')
            stderr_f = open(WORKER_STDERR_PATH + "/" + uid + "_stderr.log", 'w+')
            os.chdir(WORKER_DIRECTORY_PATH)
            return_code = subprocess.call(command_arguments, stdout=stdout_f, stderr=stderr_f, shell=True)
            stdout_f.close()
            stderr_f.close()
            return return_code
        except Exception as e:
            print('Shell script execution failure!', e)
            return 99
