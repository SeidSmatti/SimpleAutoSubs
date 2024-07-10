import os
import time
import subprocess
from faster_whisper import WhisperModel

# Set up environment variable if necessary
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Load the model
def load_model(model_size="base", device="cpu", compute_type="int8"):
    return WhisperModel(model_size, device=device, compute_type=compute_type)

# Convert video to audio using ffmpeg
def convert_to_audio(input_file, output_file):
    try:
        command = ["ffmpeg", "-i", input_file, "-q:a", "0", "-map", "a", output_file]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error converting video to audio: {e}")

# Transcribe audio with or without timecodes
def transcribe_audio(model_size, device, audio_path, include_timecodes, log):
    model = load_model(model_size, device, "int8" if device == "cpu" else "float16")

    try:
        start_time = time.time()
        log(f"Starting transcription for {audio_path}")

        # Transcribe the audio file
        segments, _ = model.transcribe(audio_path)

        transcriptions = []
        for segment in segments:
            start, end, text = segment.start, segment.end, segment.text
            if include_timecodes:
                transcriptions.append(f"{start:.2f}-{end:.2f}: {text}")
            else:
                transcriptions.append(text)

        transcription_time = time.time() - start_time
        log(f"Transcription completed in {transcription_time:.2f} seconds.")
        return transcriptions
    except Exception as e:
        log(f"An error occurred: {e}")
        return []
