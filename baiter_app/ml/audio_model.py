import os
import subprocess
import tempfile

from moonshine_voice import (
    Transcriber,
    ModelArch,
    TranscriptEventListener,
    load_wav_file,
)


MODEL_PATH = (
    r"C:\moonshine_cache\download.moonshine.ai"
    r"\model\medium-streaming-en\quantized_26_08_21"
)


def transcribe_audio(audio_path):
    #временный wav файл
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        wav_path = temp_file.name

    try:
        #в wav через FFmpeg
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                audio_path,
                "-ar",
                "16000",
                "-ac",
                "1",
                wav_path,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


        audio_data, sample_rate = load_wav_file(wav_path)

        transcriber = Transcriber(
            model_path=MODEL_PATH,
            model_arch=ModelArch.MEDIUM_STREAMING,
        )

        class Listener(TranscriptEventListener):
            def __init__(self):
                self.lines = []

            def on_line_completed(self, event):
                self.lines.append(event.line.text)

        listener = Listener()
        transcriber.add_listener(listener)

        transcriber.start()

        chunk_size = int(0.1 * sample_rate)

        for i in range(0, len(audio_data), chunk_size):
            chunk = audio_data[i:i + chunk_size]
            transcriber.add_audio(chunk, sample_rate)

        transcriber.stop()
        transcriber.close()

        return " ".join(listener.lines).strip()

    finally:
        #удалить временный wav
        if os.path.exists(wav_path):
            os.remove(wav_path)