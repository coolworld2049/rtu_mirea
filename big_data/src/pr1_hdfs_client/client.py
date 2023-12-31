import os
import pathlib

import requests
from loguru import logger
from requests import Response, HTTPError


class HDFSQueryBuilder:
    def __init__(self, user, current_hdfs_path=""):
        self.user = user
        self.current_hdfs_path = current_hdfs_path
        self.query_params = {}

    def with_param(self, key, value):
        self.query_params[key] = value
        return self

    def with_params(self, params):
        self.query_params.update(params)
        return self

    def build(self):
        query = {
            "user.name": self.user,
            "op": self.query_params.get("op", None),
            **self.query_params,
        }
        return query


class HDFSClient(HDFSQueryBuilder):
    def __init__(
        self, host, port, user, current_hdfs_path="/", local_current_path="/home/"
    ):
        super().__init__(user, current_hdfs_path)
        self.current_hdfs_path = current_hdfs_path
        self.local_current_path = local_current_path
        self.user = user
        self.host = host
        self.port = port
        self.base_url = f"http://{self.host}:{self.port}/webhdfs/v1/user/{self.user}"

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
            with requests.request(method, url, params=params, data=data) as resp:
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
            logger.error(f"{file_path} is dir")
            return
        if not file_path.exists():
            logger.error(f"{file_path} not exists")
            return
        return file_path

    def mkdir(self, dir):
        query = HDFSQueryBuilder(self.user).with_param("op", "MKDIRS")
        response = self._make_request(
            "PUT",
            path=dir,
            params=query.build(),
        )
        return response

    def put(self, file: str, hdfs_file: str = None):
        file_path = self.validate_file_path(file)
        if not hdfs_file:
            hdfs_file = pathlib.Path(file).name
        query = HDFSQueryBuilder(self.user).with_param("op", "CREATE")
        query.with_param("overwrite", "true")
        response = self._make_request(
            "PUT",
            path=hdfs_file,
            params=query.build(),
        )
        response = requests.put(
            url=response.url,
            data=file_path.read_text(),
        )
        response.raise_for_status()
        return response

    def get(self, hdfs_file: str, file: str):
        file_path = pathlib.Path(file)
        query = HDFSQueryBuilder(self.user).with_param("op", "OPEN")
        response = self._make_request(
            "GET",
            path=hdfs_file,
            params=query.build(),
        )
        response = requests.get(response.url)
        file_path.write_bytes(response.content)
        return response

    def append(self, file, hdfs_file):
        file_path = self.validate_file_path(file)
        home_file_path = pathlib.Path(self.local_current_path).joinpath(file_path)
        query = HDFSQueryBuilder(self.user).with_param("op", "APPEND")
        response = self._make_request(
            "POST",
            path=hdfs_file,
            params=query.build(),
        )
        response = requests.post(url=response.url, data=home_file_path.read_text())
        response.raise_for_status()
        return response

    def delete(self, hdfs_file: str):
        query = HDFSQueryBuilder(self.user).with_param("op", "DELETE")
        response = self._make_request(
            "DELETE",
            path=hdfs_file,
            params=query.build(),
        )
        return response

    def ls(self):
        query = HDFSQueryBuilder(self.user).with_param("op", "LISTSTATUS")
        response = self._make_request("GET", params=query.build())
        data = response.json()
        for file in data["FileStatuses"]["FileStatus"]:
            logger.info(f'{file["type"]} {file["pathSuffix"]}')

    def cd(self, to_path):
        target_path = self._build_path(self.current_hdfs_path, to_path)
        query = HDFSQueryBuilder(self.user).with_param("op", "GETFILESTATUS")
        response = self._make_request("GET", path=target_path, params=query.build())
        self.current_hdfs_path = target_path

    def lls(self):
        os.system(f"ls {self.local_current_path}")

    def lcd(self, to_path):
        target_path = self._build_path(self.current_hdfs_path, to_path)
        if not target_path.is_dir():
            logger.error(f"{to_path} is not dir")
        self.local_current_path = target_path
