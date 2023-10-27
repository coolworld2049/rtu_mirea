import argparse

from loguru import logger

from .client import HDFSClient


class HDFSClientCLI(HDFSClient):
    def __init__(self, host, port, user):
        super().__init__(host, port, user)

    def call_func(self, func_name):
        spl = func_name.split()
        if len(spl) == 0:
            return
        if spl[0] == "mkdir" and len(spl) == 2:
            self.mkdir(spl[1])
        elif spl[0] == "put" and len(spl) == 2:
            hdfs_file_name = spl[1].split("/")[-1]
            self.put(file=spl[1], hdfs_file_name=hdfs_file_name)
        elif spl[0] == "get" and len(spl) == 3:
            self.get(spl[1], spl[2])
        elif spl[0] == "add" and len(spl) == 3:
            self.add(spl[1], spl[2])
        elif spl[0] == "delete" and len(spl) == 2:
            self.delete(spl[1])
        elif spl[0] == "ls" and len(spl) == 1:
            self.ls()
        elif spl[0] == "cd" and len(spl) == 2:
            self.cd(spl[1])
        elif spl[0] == "lls" and len(spl) == 1:
            self.lls()
        elif spl[0] == "lcd" and len(spl) == 2:
            self.lcd(spl[1])
        else:
            logger.error("Command not exist")

    def run(self):
        try:
            while True:
                cmd = input(
                    f"{self.user}@{self.host}:{self.port} "
                    f"[{self.current_hdfs_path}] "
                    f"[{self.local_current_path}] $ "
                )
                self.call_func(cmd)
        except KeyboardInterrupt:
            print("\n")


def main():
    parser = argparse.ArgumentParser(
        prog="python -m hdfs_cli", description="HDFS Command Line Interface"
    )
    parser.add_argument("connection_string", type=str, help="HDFS user@host:port")
    args = parser.parse_args()
    user = str(args.connection_string).split("@")[0]
    host, port = str(args.connection_string).split("@")[1].split(":")
    cli = HDFSClientCLI(host, port, user)
    cli.run()


if __name__ == "__main__":
    main()
