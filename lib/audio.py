import pathlib
import os
import tempfile
import requests

import ffmpeg


class AudioPreProcessor:
    def __init__(self):
        tmpdir = pathlib.Path(tempfile.mkdtemp())
        self.output_path = str(tmpdir / 'audio.wav')
        self.error = None

    def process(self, audio_file: pathlib.Path):
        audio_file_path = str(audio_file)
        if audio_file_path.endswith('.wav') and audio_file_path.startswith('http'):
            response = requests.get(audio_file_path, stream=True)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            tmp_file.write(chunk)
                self.output_path = tmp_file.name
            else:
                self.error = "Error downloading file " + audio_file_path
        else:
            raise ValueError("Invalid file format " + audio_file_path)

    def cleanup(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
