import os
import threading
import tempfile
import time
import customtkinter as ctk
from tkinter import filedialog, messagebox
from transcriber import transcribe_audio, convert_to_audio, write_transcriptions_to_file
from embedder import convert_to_srt, embed_subtitles

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Log messages to the log box
def log(message):
    log_box.insert(ctk.END, message + "\n")
    log_box.see(ctk.END)

# Browse file function
def browse_file(entry):
    file_path = filedialog.askopenfilename()
    if file_path:
        entry.delete(0, ctk.END)
        entry.insert(0, file_path)

# Browse output directory function
def browse_output(entry):
    output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if output_path:
        entry.delete(0, ctk.END)
        entry.insert(0, output_path)

# Start transcription process in a separate thread
def start_transcription_thread():
    threading.Thread(target=start_transcription).start()

# Transcription process
# Add import for the new function
from transcriber import transcribe_audio, convert_to_audio, write_transcriptions_to_file

# Update the start_transcription function to save the transcriptions to a file
def start_transcription():
    input_file = file_entry.get()
    model_size = model_size_var.get()
    device = "cuda" if gpu_var.get() else "cpu"
    include_timecodes = timecodes_var.get()
    selected_language = language_var.get()
    
    if not input_file:
        messagebox.showerror("Error", "Please select an input file.")
        return

    output_file = output_entry.get()
    if not output_file:
        messagebox.showerror("Error", "Please select an output file.")
        return

    # Check if input file is video or audio
    with tempfile.TemporaryDirectory() as temp_dir:
        audio_path = os.path.join(temp_dir, "temp_audio.wav")
        if input_file.endswith(('.mp4', '.mkv', '.avi')):
            log("Converting video to audio...")
            convert_to_audio(input_file, audio_path)
        else:
            audio_path = input_file

        # Transcribe audio
        transcriptions = transcribe_audio(model_size, device, audio_path, include_timecodes, log, selected_language)

        # Save transcriptions to file
        write_transcriptions_to_file(transcriptions, output_file)

    # Display transcription for editing
    transcription_textbox.delete("1.0", ctk.END)
    transcription_textbox.insert(ctk.END, "\n".join(transcriptions))


# Start embedding process in a separate thread
def start_embedding_thread():
    threading.Thread(target=start_embedding).start()

def try_delete_file(file_path, retries=5, delay=1):
    """Try to delete a file with retries."""
    for _ in range(retries):
        try:
            os.remove(file_path)
            return
        except PermissionError:
            time.sleep(delay)
    log(f"Could not delete temporary SRT file after multiple attempts. It might still be in use: {file_path}")

# Embedding process
def start_embedding():
    input_text = transcription_textbox.get("1.0", ctk.END).strip()
    input_video = file_entry.get()
    output_video = output_entry.get()

    if not input_text or not input_video or not output_video:
        messagebox.showerror("Error", "Please ensure all fields are filled.")
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix=".srt") as temp_srt:
        convert_to_srt(input_text, temp_srt.name, log)
        try:
            embed_subtitles(input_video, output_video, temp_srt.name, log)
        finally:
            threading.Thread(target=try_delete_file, args=(temp_srt.name,)).start()

# Set up GUI
ctk.set_appearance_mode("dark")  # Modes: "system" (default), "light", "dark"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

root = ctk.CTk()
root.title("SimpleAutoSubs")

frame = ctk.CTkFrame(root)
frame.grid(row=0, column=0, padx=20, pady=20)

ctk.CTkLabel(frame, text="Input File:").grid(row=0, column=0, sticky="w", pady=5)
file_entry = ctk.CTkEntry(frame, width=400)
file_entry.grid(row=0, column=1, padx=5, pady=5)
ctk.CTkButton(frame, text="Browse", command=lambda: browse_file(file_entry)).grid(row=0, column=2, padx=5, pady=5)

ctk.CTkLabel(frame, text="Output File:").grid(row=1, column=0, sticky="w", pady=5)
output_entry = ctk.CTkEntry(frame, width=400)
output_entry.grid(row=1, column=1, padx=5, pady=5)
ctk.CTkButton(frame, text="Browse", command=lambda: browse_output(output_entry)).grid(row=1, column=2, padx=5, pady=5)

ctk.CTkLabel(frame, text="Model Size:").grid(row=2, column=0, sticky="w", pady=5)
model_size_var = ctk.StringVar(value="base")
ctk.CTkComboBox(frame, variable=model_size_var, values=["base", "small", "medium", "large", "large-v2", "large-v3"]).grid(row=2, column=1, padx=5, pady=5)

ctk.CTkLabel(frame, text="Language:").grid(row=3, column=0, sticky="w", pady=5)
language_var = ctk.StringVar(value="autodetect")
supported_languages = [
    ("autodetect", "autodetect"), ("af", "Afrikaans"), ("ar", "Arabic"), ("hy", "Armenian"), ("az", "Azerbaijani"),
    ("be", "Belarusian"), ("bs", "Bosnian"), ("bg", "Bulgarian"), ("ca", "Catalan"), ("zh", "Chinese"),
    ("hr", "Croatian"), ("cs", "Czech"), ("da", "Danish"), ("nl", "Dutch"), ("en", "English"),
    ("et", "Estonian"), ("fi", "Finnish"), ("fr", "French"), ("gl", "Galician"), ("de", "German"),
    ("el", "Greek"), ("he", "Hebrew"), ("hi", "Hindi"), ("hu", "Hungarian"), ("is", "Icelandic"),
    ("id", "Indonesian"), ("it", "Italian"), ("ja", "Japanese"), ("kn", "Kannada"), ("kk", "Kazakh"),
    ("ko", "Korean"), ("lv", "Latvian"), ("lt", "Lithuanian"), ("mk", "Macedonian"), ("ms", "Malay"),
    ("mr", "Marathi"), ("mi", "Maori"), ("ne", "Nepali"), ("no", "Norwegian"), ("fa", "Persian"),
    ("pl", "Polish"), ("pt", "Portuguese"), ("ro", "Romanian"), ("ru", "Russian"), ("sr", "Serbian"),
    ("sk", "Slovak"), ("sl", "Slovenian"), ("es", "Spanish"), ("sw", "Swahili"), ("sv", "Swedish"),
    ("tl", "Tagalog"), ("ta", "Tamil"), ("th", "Thai"), ("tr", "Turkish"), ("uk", "Ukrainian"),
    ("ur", "Urdu"), ("vi", "Vietnamese"), ("cy", "Welsh")
]
language_options = [label for code, label in supported_languages]
ctk.CTkComboBox(frame, variable=language_var, values=language_options).grid(row=3, column=1, padx=5, pady=5)

gpu_var = ctk.BooleanVar()
ctk.CTkCheckBox(frame, text="Use GPU", variable=gpu_var).grid(row=4, column=0, sticky="w", padx=5, pady=5)

timecodes_var = ctk.BooleanVar()
ctk.CTkCheckBox(frame, text="Include Timecodes", variable=timecodes_var).grid(row=4, column=1, sticky="w", padx=5, pady=5)

ctk.CTkButton(frame, text="Start Transcription", command=start_transcription_thread).grid(row=5, column=0, columnspan=3, pady=10)

transcription_textbox = ctk.CTkTextbox(frame, height=200, width=600)
transcription_textbox.grid(row=6, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

ctk.CTkButton(frame, text="Embed Subtitles", command=start_embedding_thread).grid(row=7, column=0, columnspan=3, pady=10)

log_box = ctk.CTkTextbox(frame, height=100, width=600)
log_box.grid(row=8, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

root.mainloop()
