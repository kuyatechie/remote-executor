import os

WORKER_DIRECTORY_PATH = os.getenv("WORKER_DIRECTORY_PATH", "/homedir/")


class DiskSpaceUtility(object):

    @staticmethod
    def get_free_space():
        if os.path.isdir(WORKER_DIRECTORY_PATH):
            s = os.statvfs(WORKER_DIRECTORY_PATH)
            return (s.f_bavail * s.f_frsize)/1024
        else:
            return 0
