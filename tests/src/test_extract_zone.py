

from unittest.mock import mock_open
import pytest 
from src.extract_zone import fetch_taxi_zone_file

@pytest.fixture
def mock_downloaded_file(mocker):
    ## must return file or None
    mock_response = mocker.MagicMock()
    mock_response.content = b"LocationID,Borough\n1,EWR\n"
    return mock_response


def test_fetch_taxi_zone_file_should_download(mocker,mock_downloaded_file):
    mock_request = mocker.patch('src.extract_zone.requests.get',return_value = mock_downloaded_file)
    mocker.patch('src.extract_zone.Path.mkdir')
    mocker.patch('src.extract_zone.Path.is_file',return_value = False)
    mocker.patch('src.extract_zone.get_stats_on_file')
    mocker.patch('builtins.open',mocker.mock_open())

    fetch_taxi_zone_file()
    mock_request.assert_called_once()

def test_fetch_taxi_zone_file_should_force_download(mocker,mock_downloaded_file):
    mock_request = mocker.patch('src.extract_zone.requests.get',return_value = mock_downloaded_file)
    mocker.patch('src.extract_zone.Path.mkdir')
    mocker.patch('src.extract_zone.Path.is_file',return_value = True)
    mocker.patch('src.extract_zone.get_stats_on_file')
    mocker.patch('builtins.open',mocker.mock_open())

    fetch_taxi_zone_file(True)
    mock_request.assert_called_once()


def test_fetch_taxi_zone_file_should_not_download(mocker,mock_downloaded_file):
    mock_request = mocker.patch('src.extract_zone.requests.get',return_value = mock_downloaded_file)
    mocker.patch('src.extract_zone.Path.mkdir')
    mocker.patch('src.extract_zone.Path.is_file',return_value = True)
    mocker.patch('src.extract_zone.get_stats_on_file')
    mocker.patch('builtins.open',mocker.mock_open())

    fetch_taxi_zone_file()
    mock_request.assert_not_called()
