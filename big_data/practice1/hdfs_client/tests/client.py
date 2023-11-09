import pytest

from big_data.practice1.hdfs_client.client import HDFSClient


@pytest.fixture
def hdfs_client():
    host = "localhost"
    port = "50070"
    user = "ivanovnp"
    return HDFSClient(host, port, user)


def test_mkdir(hdfs_client):
    response = hdfs_client.mkdir("test_dir")
    assert response.status_code == 200


def test_put(hdfs_client, tmp_path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Test file content")
    response = hdfs_client.put(test_file.__str__(), f"test_dir/{test_file.name}")
    assert response.status_code == 201


def test_get(hdfs_client, tmp_path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Test file content")

    hdfs_client.put(str(test_file), "test_dir/test_file.txt")

    downloaded_file = tmp_path / "downloaded_file.txt"
    hdfs_client.get("test_dir/test_file.txt", str(downloaded_file))

    assert downloaded_file.read_text() == "Test file content"


def test_append(hdfs_client, tmp_path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Test file content")

    response = hdfs_client.append(str(test_file), "test_dir/test_file.txt")
    assert response.status_code == 200


def test_delete(hdfs_client):
    response = hdfs_client.delete("test_dir/test_file.txt")
    assert response.status_code == 200


def test_ls(hdfs_client):
    hdfs_client.mkdir("test_dir")
    response = hdfs_client.ls()


def test_cd(hdfs_client):
    hdfs_client.mkdir("test_dir")
    hdfs_client.cd("test_dir")
    assert hdfs_client.current_hdfs_path.__str__() == "/test_dir"
