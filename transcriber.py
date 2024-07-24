import os
import time
from faster_whisper import WhisperModel
import subprocess

log_box = None

def set_log_box(log_widget):
    global log_box
    log_box = log_widget

def log(message):
    if log_box:
        log_box.insert("end", message + "\n")
        log_box.see("end")
    else:
        print(message.encode('utf-8', errors='replace').decode('utf-8'))

def load_model(model_size="base", device="cpu", compute_type="int8"):
    log("Loading the model...")
    return WhisperModel(model_size, device=device, compute_type=compute_type)

def convert_to_audio(input_file, output_file):
    try:
        command = ["ffmpeg", "-i", input_file, "-q:a", "0", "-map", "a", output_file]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        log(f"Error converting video to audio: {e}")
        raise

def transcribe_audio(model_size, device, audio_path, include_timecodes, log_func, language):
    try:
        start_time = time.time()
        log_func(f"Starting transcription for {audio_path}")

        model = load_model(model_size, device)

        supported_languages = {
            "autodetect": None, "Afrikaans": "af", "Arabic": "ar", "Armenian": "hy", "Azerbaijani": "az",
            "Belarusian": "be", "Bosnian": "bs", "Bulgarian": "bg", "Catalan": "ca", "Chinese": "zh",
            "Croatian": "hr", "Czech": "cs", "Danish": "da", "Dutch": "nl", "English": "en",
            "Estonian": "et", "Finnish": "fi", "French": "fr", "Galician": "gl", "German": "de",
            "Greek": "el", "Hebrew": "he", "Hindi": "hi", "Hungarian": "hu", "Icelandic": "is",
            "Indonesian": "id", "Italian": "it", "Japanese": "ja", "Kannada": "kn", "Kazakh": "kk",
            "Korean": "ko", "Latvian": "lv", "Lithuanian": "lt", "Macedonian": "mk", "Malay": "ms",
            "Marathi": "mr", "Maori": "mi", "Nepali": "ne", "Norwegian": "no", "Persian": "fa",
            "Polish": "pl", "Portuguese": "pt", "Romanian": "ro", "Russian": "ru", "Serbian": "sr",
            "Slovak": "sk", "Slovenian": "sl", "Spanish": "es", "Swahili": "sw", "Swedish": "sv",
            "Tagalog": "tl", "Tamil": "ta", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk",
            "Urdu": "ur", "Vietnamese": "vi", "Welsh": "cy"
        }

        language_code = supported_languages.get(language, None)

        segments, _ = model.transcribe(audio_path, language=language_code)
        transcriptions = []
        for segment in segments:
            start, end, text = segment.start, segment.end, segment.text
            if include_timecodes:
                transcriptions.append(f"{start:.2f}-{end:.2f}: {text}")
            else:
                transcriptions.append(text)

        transcription_time = time.time() - start_time
        log_func(f"Transcription completed in {transcription_time:.2f} seconds.")
        return transcriptions
    except Exception as e:
        log_func(f"An error occurred: {e}")
        return []

def write_transcriptions_to_file(transcriptions, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        for line in transcriptions:
            file.write(line + '\n')
