import os
import pathlib

import requests
from loguru import logger
from requests import Response, HTTPError


class HDFSClient:
    def __init__(self, host, port, user):
        self.current_hdfs_path = "/"
        self.local_current_path = "/home/"
        self.host = host
        self.port = port
        self.user = user
        self.base_url = f"http://{host}:{port}/webhdfs/v1/user/{self.user}"

    def _build_url(self, path=None, params=None):
        url = f"{self.base_url}{self.current_hdfs_path}{path or ''}"
        if params:
            url += "?" + "&".join(f"{key}={value}" for key, value in params.items())
        logger.debug(f"url '{url}'")
        return url

    def _make_request(
        self, method, path=None, params=None, data=None
    ) -> Response | None:
        url = self._build_url(path, params)
        try:
            with requests.request(
                method,
                url,
                params=params,
                data=data,
            ) as resp:
                resp.raise_for_status()
                return resp
        except requests.exceptions.ConnectionError as ce:
            logger.error(ce)
            raise SystemExit
        except HTTPError as he:
            logger.error(he)
            return None

    @staticmethod
    def _build_path(old_path, new_path):
        if new_path[0] == "/":
            old_path = new_path
            if new_path[-1] != "/":
                old_path += "/"
        else:
            dirs = new_path.split("/")
            for dir in dirs:
                if dir == "." or dir == "":
                    pass
                elif dir == "..":
                    idx = old_path.rfind("/", 0, -1)
                    old_path = old_path[:idx] + "/"
                else:
                    old_path += dir + "/"
        return pathlib.Path(old_path)

    @staticmethod
    def validate_file_path(file: str):
        logger.debug(f"file '{file}'")
        file_path = pathlib.Path(file)
        if file_path.is_dir():
            logger.error(f"{file_path} is a directory")
            return
        if not file_path.exists():
            logger.error(f"{file_path} not found")
            return
        return file_path

    def mkdir(self, dir):
        response = self._make_request(
            "PUT",
            path=dir,
            params={
                "user.name": self.user,
                "op": "MKDIRS",
            },
        )
        return response

    def put(self, file: str, hdfs_file_name: str):
        file_path = self.validate_file_path(file)
        response = self._make_request(
            "PUT",
            path=hdfs_file_name,
            params={
                "user.name": self.user,
                "op": "CREATE",
                "overwrite": "true",
            },
        )
        response = requests.put(
            url=response.url,
            data=file_path.read_text(),
        )
        response.raise_for_status()
        return response

    def get(self, hdfs_file_name: str, file: str):
        file_path = pathlib.Path(file)
        response = self._make_request(
            "GET",
            path=hdfs_file_name,
            params={"op": "OPEN"},
        )
        response = requests.get(response.url)
        file_path.write_bytes(response.content)
        return response

    def add(self, file, hdfs_file_name):
        file_path = self.validate_file_path(file)
        home_file_path = pathlib.Path(self.local_current_path).joinpath(file_path)
        response = self._make_request(
            "POST",
            path=hdfs_file_name,
            params={"user.name": self.user, "op": "APPEND"},
        )
        response = requests.post(url=response.url, data=home_file_path.read_text())
        response.raise_for_status()
        return response

    def delete(self, file_name: str):
        response = self._make_request(
            "DELETE",
            path=file_name,
            params={"user.name": self.user, "op": "DELETE"},
        )
        return response

    def ls(self):
        response = self._make_request(
            "GET",
            params={"user.name": self.user, "op": "LISTSTATUS"},
        )
        data = response.json()
        directories = []
        files = []
        for file in data["FileStatuses"]["FileStatus"]:
            if file["type"] == "DIRECTORY":
                directories.append(file["pathSuffix"])
            elif file["type"] == "FILE":
                files.append(file["pathSuffix"])
        for dir in directories:
            logger.info(f"{dir} (DIR)")
        for file in files:
            logger.info(f"{file} (FILE)")

    def cd(self, to_path):
        target_path = self._build_path(self.current_hdfs_path, to_path)
        response = self._make_request(
            "GET", path=target_path, params={"op": "GETFILESTATUS"}
        )
        self.current_hdfs_path = target_path

    def lls(self):
        os.system(f"ls {self.local_current_path}")

    def lcd(self, to_path):
        target_path = self._build_path(self.current_hdfs_path, to_path)
        if not target_path.is_dir():
            logger.error(f"{to_path} is not directory")
        self.local_current_path = target_path
