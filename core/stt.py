import os
import whisper
from typing import BinaryIO
import tempfile


class WhisperSTT:
    def __init__(self, model_name: str = "base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_data: BinaryIO, language: str = "pt") -> str:
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as f:
            f.write(audio_data.read())
            temp_path = f.name

        try:
            result = self.model.transcribe(temp_path, language=language)
            return result["text"]
        finally:
            os.unlink(temp_path)

    def transcribe_file(self, file_path: str, language: str = "pt") -> str:
        result = self.model.transcribe(file_path, language=language)
        return result["text"]


stt_engine = WhisperSTT(model_name=os.getenv("OPENAI_WHISPER_MODEL", "base"))