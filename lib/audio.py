import pathlib
import os
import tempfile
import requests


class AudioPreProcessor:
    def __init__(self):
        tmpdir = pathlib.Path(tempfile.mkdtemp())
        self.output_path = str(tmpdir / 'audio.wav')
        self.error = None

    def process(self, audio_file: pathlib.Path):
        # this must be a wav file with 16kHz sample rate
        audio_file_path = str(audio_file)
        self.output_path = audio_file_path

    def cleanup(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
