from time_utils import TimeUtils
from freezegun import freeze_time


@freeze_time("1990-02-08 01:23:45")
def test_get_current_timestamp():
    assert TimeUtils.get_current_timestamp() == "1990_02_08_01_23_45"


@freeze_time("1990-02-08 01:23:45")
def test_get_current_date():
    assert TimeUtils.get_current_date() == "1990_02_08"


def test_convert_seconds_to_duration():
    assert TimeUtils.convert_seconds_to_duration(15) == "0:00:15"
    assert TimeUtils.convert_seconds_to_duration(3601) == "1:00:01"


def test_convert_duration_to_seconds():
    assert TimeUtils.convert_duration_to_seconds("0:01:15") == 75
    assert TimeUtils.convert_duration_to_seconds("1:00:01") == 3601
