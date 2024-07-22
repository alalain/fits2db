import pytest
from pathlib import Path
from fits2db.fits import FitsFile


def test_valid_fits_file():
    path = Path(r"tests\unit\data\2021-07-07_L1a.fits")
    fits_file = FitsFile(path)
    assert fits_file.file_name == "2021-07-07_L1a.fits"


def test_table_names():
    path = Path(r"tests\unit\data\2021-07-07_L1a.fits")
    fits_file = FitsFile(path)
    assert fits_file.table_names == [
        "CONTROL_NORMAL",
        "CONTROL_BACKUP",
        "ERROR_NORMAL",
        "ERROR_BACKUP",
        "CALIBRATION",
        "CAVITY_EXPOSURE",
        "SHUTTER",
        "HOUSEKEEPING",
        "JTSIM_BROADCAST",
        "TELEMETRY",
    ]


def test_invalid_fits_path():
    path = Path(r"tests\unit\data\2021_L1a.fits")
    with pytest.raises(FileNotFoundError):
        FitsFile(path)


def test_fits_path_not_a_file():
    path = Path(r"tests\unit\data")
    with pytest.raises(ValueError):
        FitsFile(path)


def test_fits_path_not_a_fits_file():
    path = Path(r"tests\unit\data\2021-07-07_L1a.txt")
    with pytest.raises(ValueError):
        FitsFile(path)


def test_corrupt_fits_file():
    path = Path(
        r"C:\Users\cedric.renda\Documents\fits2db\tests\unit\data\2021-07-07_L1a_corrupt.fits"
    )
    with pytest.raises(ValueError):
        FitsFile(path)
