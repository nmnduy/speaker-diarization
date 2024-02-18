"""
download model weights to /data
wget wget -O - https://pyannote-speaker-diarization.s3.eu-west-2.amazonaws.com/data-2023-03-25-02.tar.gz | tar xz -C /
"""
import json
import tempfile
import base64

from typing import Dict
from cog import BasePredictor, Input, Path
from pyannote.audio.pipelines import SpeakerDiarization

from lib.diarization import DiarizationPostProcessor


class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory to make running multiple predictions efficient"""
        self.diarization = SpeakerDiarization(
            segmentation="/data/pyannote/segmentation/pytorch_model.bin",
            embedding="/data/speechbrain/spkrec-ecapa-voxceleb",
            clustering="AgglomerativeClustering",
            segmentation_batch_size=32,
            embedding_batch_size=32,
            embedding_exclude_overlap=True,
        )
        self.diarization.instantiate({
            "clustering": {
                "method": "centroid",
                "min_cluster_size": 15,
                "threshold": 0.7153814381597874,
            },
            "segmentation": {
                "min_duration_off": 0.5817029604921046,
                "threshold": 0.4442333667381752,
            },
        })
        self.diarization_post = DiarizationPostProcessor()

    def predict(
        self,
        wavB64Str: str = Input(description="Base64 encoded WAV audio"),
    ) -> Dict:

        closure = {'embeddings': None}

        # write wav to temp file
        with tempfile.NamedTemporaryFile(suffix=".wav") as f:
            with open(f.name, "wb") as wav_file:
                wav_file.write(base64.b64decode(wavB64Str))
                wav_file.flush()

            diarization = self.diarization(f.name)
        embeddings = {
            'data': closure['embeddings'],
            'chunk_duration': self.diarization.segmentation_duration,
            'chunk_offset': self.diarization.segmentation_step * self.diarization.segmentation_duration,
        }
        return self.diarization_post.process(diarization, embeddings)
