import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

FTP_USER = os.getenv("FTP_USER", "ftp")
FTP_PASSWORD = os.getenv("FTP_PASSWORD", "ftp")
FTP_HOSTNAME = os.getenv("FTP_HOSTNAME", "0.0.0.0")
FTP_PORT = os.getenv("FTP_PORT", 2121)
FTP_DIRECTORY = os.getenv("FTP_DIRECTORY", "/homedir/")


def main():
    authorizer = DummyAuthorizer()

    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmwMT')
    authorizer.add_anonymous(FTP_DIRECTORY)

    handler = FTPHandler
    handler.authorizer = authorizer

    handler.banner = "Hello! Welcome to the remote-executor app."

    # handler.masquerade_address = '151.25.42.11'
    # handler.passive_ports = range(60000, 65535)

    address = (FTP_HOSTNAME, FTP_PORT)
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    server.serve_forever()


if __name__ == '__main__':
    if not os.path.exists(FTP_DIRECTORY):
        os.makedirs(FTP_DIRECTORY)
    main()
