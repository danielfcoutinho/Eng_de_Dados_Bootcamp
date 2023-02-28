import datetime
from unittest.mock import patch
from unittest.mock import mock_open

import pytest

from ingestors import DataIngestor
from writers import DataWriter


# Patch é utilizado para sobrescrever um método abstrato da classe
@patch("ingestors.DataIngestor.__abstractmethods__", set())
class TestIngestors:
    def test_checkpoint_filename(self):
        actual = DataIngestor(
            writer=DataWriter,
            coins=["TEST", "DINHEIROS"],
            default_start_date=datetime.date(2021, 6, 12)
        )._checkpoint_filename
        expected = "DataIngestor.checkpoint"
        assert actual == expected

    def test_load_checkpoint_no_checkpoint(self):
        actual = DataIngestor(
            writer=DataWriter,
            coins=["TEST", "DINHEIROS"],
            default_start_date=datetime.date(2021, 6, 12)
        )._load_checkpoint()
        expected = datetime.date(2021, 6, 12)
        assert actual == expected

    @patch("builtins.open", new_callable=mock_open, read_data="2021-06-25")
    def test_load_checkpoint_existing_checkpoint(self, mock):
        actual = DataIngestor(
            writer=DataWriter,
            coins=["TEST", "DINHEIROS"],
            default_start_date=datetime.date(2021, 6, 21)
        )._load_checkpoint()
        expected = datetime.date(2021, 6, 25)
        assert actual == expected

    # Sobreescrevendo para evitar que seja criado o arquivo de checkpoint
    @patch("ingestors.DataIngestor._write_checkpoint", return_value=None)
    def test_update_checkpoint_checkpoint_updated(self, mock):
        data_ingestor = DataIngestor(
            writer=DataWriter,
            coins=["TEST", "DINHEIROS"],
            default_start_date=datetime.date(2021, 6, 12)
        )
        data_ingestor._update_checkpoint(value=datetime.date(2019, 1, 1))
        actual = data_ingestor._checkpoint
        expected = datetime.date(2019, 1, 1)
        assert actual == expected

    @patch("ingestors.DataIngestor._write_checkpoint", return_value=None)
    def test_update_checkpoint_checkpoint_written(self, mock):
        data_ingestor = DataIngestor(
            writer=DataWriter,
            coins=["TEST", "DINHEIROS"],
            default_start_date=datetime.date(2021, 6, 12)
        )
        data_ingestor._update_checkpoint(value=datetime.date(2019, 1, 1))
        mock.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data="2021-06-25")
    @patch("ingestors.DataIngestor._checkpoint_filename", return_value="foobar.checkpoint")
    def test_write_checkpoint(self, mock_checkpoint_filename, mock_open_file):
        data_ingestor = DataIngestor(
            writer=DataWriter,
            coins=["TEST", "DINHEIROS"],
            default_start_date=datetime.date(2021, 6, 12)
        )
        data_ingestor._write_checkpoint()
        mock_open_file.assert_called_with(mock_checkpoint_filename, 'w')
