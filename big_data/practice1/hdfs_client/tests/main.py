import pathlib

import pytest
from loguru import logger

from big_data.practice1.hdfs_client.client import HDFSClient

hdfs_dir_name = "/testdir"


@pytest.fixture
def hdfs_client():
    host = "localhost"
    port = 50070
    user = "ivanovnp"
    return HDFSClient(host, port, user)


def test_mkdir(hdfs_client):
    response = hdfs_client.mkdir(hdfs_dir_name)
    logger.info(f"ls '{hdfs_client.ls()}' lls {hdfs_client.lls()}")
    assert response.status_code == 200


def test_put_and_get(hdfs_client):
    logger.info(f"ls '{hdfs_client.ls()}' lls {hdfs_client.lls()}")
    local_file_path = pathlib.Path("/tmp/test_file.txt")
    local_file_path.write_text("Hello HDFS!")

    hdfs_file_name = f"{hdfs_dir_name}/test_file.txt"
    hdfs_client.put(local_file_path.__str__(), hdfs_file_name)

    downloaded_file_path = f"{hdfs_dir_name}/downloaded_file.txt"
    hdfs_client.get(hdfs_file_name, downloaded_file_path.__str__())

    logger.info(f"ls '{hdfs_client.ls()}' lls {hdfs_client.lls()}")
    assert local_file_path.read_text() == pathlib.Path(downloaded_file_path).read_text()
