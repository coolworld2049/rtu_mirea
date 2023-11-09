import argparse
from functools import lru_cache

from loguru import logger

from .client import HDFSClient

history = []


@lru_cache
def get_history():
    return history


class HDFSClientCLI(HDFSClient):
    def __init__(self, host, port, user):
        super().__init__(host, port, user)

    def call_func(self, command):
        spl = command.split()
        if len(spl) == 0:
            return
        history.append(command)
        if spl[0] == "mkdir" and len(spl) == 2:
            self.mkdir(dir=spl[1])
        elif spl[0] == "put" and len(spl) == 2:
            self.put(file=spl[1])
        elif spl[0] == "get" and len(spl) == 3:
            self.get(hdfs_file=spl[1], file=spl[2])
        elif spl[0] == "append" and len(spl) == 3:
            self.append(file=spl[1], hdfs_file=spl[2])
        elif spl[0] == "rm" and len(spl) == 2:
            self.delete(hdfs_file=spl[1])
        elif spl[0] == "ls" and len(spl) == 1:
            self.ls()
        elif spl[0] == "cd" and len(spl) == 2:
            self.cd(to_path=spl[1])
        elif spl[0] == "lls" and len(spl) == 1:
            self.lls()
        elif spl[0] == "lcd" and len(spl) == 2:
            self.lcd(to_path=spl[1])
        elif spl[0] == "history":
            print("\n".join([f"{i} {x}" for i, x in enumerate(history)]))
        else:
            logger.error(spl)

    def run(self):
        try:
            while True:
                command = input(
                    f"{self.user}@{self.host}:{self.port} "
                    f"HDFS [{self.current_hdfs_path}] "
                    f"LOCALHOST [{self.local_current_path}] $ "
                )
                try:
                    self.call_func(command)
                except Exception as e:
                    logger.error(e)
        except KeyboardInterrupt:
            print("\n")


def main():
    parser = argparse.ArgumentParser(
        prog="python -m hdfs_client", description="HDFS Command Line Interface"
    )
    parser.add_argument(
        "connection_string",
        type=str,
        help="HDFS user@host:port",
    )
    args = parser.parse_args()
    connection_args = str(args.connection_string).split("@")
    user = connection_args[0]
    host, port = connection_args[1].split(":")
    cli = HDFSClientCLI(host, port, user)
    cli.run()


if __name__ == "__main__":
    main()
