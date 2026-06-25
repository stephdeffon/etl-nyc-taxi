
from unittest.mock import mock_open
import pytest 
from src.extract_trips import fetch_taxi_trip_file


@pytest.fixture
def mock_downloaded_file(mocker):
    ## must return file or None
    mock_response = mocker.MagicMock()
    mock_response.content = b"Fake content"
    return mock_response



def test_fetch_taxi_trip_file_should_download(mocker,mock_downloaded_file):
    mock_request = mocker.patch('src.extract_trips.requests.get',return_value = mock_downloaded_file)
    mocker.patch('src.extract_trips.Path.mkdir')
    mocker.patch('src.extract_trips.Path.is_file',return_value = False)
    mocker.patch('src.extract_trips.get_stats_on_file')
    mocker.patch('builtins.open',mocker.mock_open())

    fetch_taxi_trip_file(1,2001)
    mock_request.assert_called_once()

def test_fetch_taxi_zone_file_should_force_download(mocker,mock_downloaded_file):
    mock_request = mocker.patch('src.extract_trips.requests.get',return_value = mock_downloaded_file)
    mocker.patch('src.extract_trips.Path.mkdir')
    mocker.patch('src.extract_trips.Path.is_file',return_value = True)
    mocker.patch('src.extract_trips.get_stats_on_file')
    mocker.patch('builtins.open',mocker.mock_open())

    fetch_taxi_trip_file(1,2001,True)
    mock_request.assert_called_once()


def test_fetch_taxi_trip_file_should_not_download(mocker,mock_downloaded_file):
    mock_request = mocker.patch('src.extract_trips.requests.get',return_value = mock_downloaded_file)
    mocker.patch('src.extract_trips.Path.mkdir')
    mocker.patch('src.extract_trips.Path.is_file',return_value = True)
    mocker.patch('src.extract_trips.get_stats_on_file')
    mocker.patch('builtins.open',mocker.mock_open())

    fetch_taxi_trip_file(1,2001)
    mock_request.assert_not_called()
