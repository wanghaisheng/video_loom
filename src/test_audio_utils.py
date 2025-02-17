import os
import pytest
from audio_utils import AudioUtils
from file_utils import FileUtils
from pdb import set_trace  # call set_trace() inline to setup debugger


output_directory = os.path.join("src", "test")
mp3_output_filename = "test_generate_mp3_from_mp4.mp3"
aac_output_filename = "test_generate_aac_from_mp4.aac"
mp3_path = FileUtils.get_file_path(os.path.join("src", "test", mp3_output_filename))
aac_path = FileUtils.get_file_path(os.path.join("src", "test", aac_output_filename))
audio_1_path = FileUtils.get_file_path(os.path.join("src", "test", "audio_1.aac"))
audio_2_path = FileUtils.get_file_path(os.path.join("src", "test", "audio_2.aac"))
concatenated_aac_name = "test_concatenate_audios.aac"
concatenated_audio_path = FileUtils.get_file_path(
    os.path.join(output_directory, concatenated_aac_name)
)
mp4_path = FileUtils.get_file_path(
    os.path.join("src", "test", "2023_04_15_19_00_49.mp4")
)
ffmpeg_preset_value = "ultrafast"


def clean_up_test_files():
    # clean up
    if os.path.exists(mp3_path):
        os.remove(mp3_path)

    if os.path.exists(aac_path):
        os.remove(aac_path)

    if os.path.exists(concatenated_audio_path):
        os.remove(concatenated_audio_path)


@pytest.fixture(autouse=True)
def before_each():
    clean_up_test_files()

    assert os.path.exists(mp3_path) == False
    assert os.path.exists(aac_path) == False

    yield

    clean_up_test_files()


def test_generate_mp3_from_mp4():
    AudioUtils.generate_mp3_from_mp4(mp4_path, mp3_path)
    assert os.path.exists(mp3_path) == True


def test_generate_aac_from_mp4():
    AudioUtils.generate_aac_from_mp4(mp4_path, aac_path, ffmpeg_preset_value)
    assert os.path.exists(aac_path) == True


def test_get_audio_duration():
    assert AudioUtils.get_audio_duration(audio_1_path) == 5
    assert AudioUtils.get_audio_duration(audio_2_path) == 10


def test_concatenate_audios():
    audios = [audio_1_path, audio_2_path]  # audio duration = 5, 10 respectively
    AudioUtils.concatenate_audios(audios, output_directory, concatenated_aac_name)
    assert os.path.exists(concatenated_audio_path) == True
    assert AudioUtils.get_audio_duration(concatenated_audio_path) == 15
