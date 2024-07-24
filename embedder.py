import os
import re
import subprocess

def convert_to_srt(input_text, output_file, log):
    lines = input_text.split("\n")
    
    with open(output_file, 'w', encoding='utf-8') as srt_file:
        counter = 1
        for line in lines:
            if re.match(r"^\d+\.\d+-\d+\.\d+:.*$", line):
                time_text = line.split(": ")
                times = time_text[0]
                text = time_text[1].strip()
                
                start_time, end_time = times.split('-')
                
                start_time = format_time(float(start_time))
                end_time = format_time(float(end_time))
                
                srt_file.write(f"{counter}\n")
                srt_file.write(f"{start_time} --> {end_time}\n")
                srt_file.write(f"{text}\n\n")
    log(f"Conversion to {output_file} completed\n")

def format_time(seconds):
    millis = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"

def embed_subtitles(input_video, output_video, subtitles_file, log):
    log(f"Embedding subtitles from {subtitles_file} into {output_video}\n")
    subtitle_style = (
        "FontName=Arial,FontSize=14,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
        "BackColour=&H00000000,Bold=1,Italic=0,BorderStyle=1,Outline=1,Shadow=0,"
        "Alignment=2,MarginV=20"
    )
    
    # Adjust the subtitles file path format for ffmpeg
    subtitles_file = subtitles_file.replace('\\', '/')
    if os.name == 'nt':
        subtitles_file = subtitles_file.replace(':', r'\:')

    command = [
        'ffmpeg',
        '-i', input_video,
        '-vf', f"subtitles='{subtitles_file}':force_style='{subtitle_style}'",
        '-c:a', 'copy',
        output_video
    ]
    try:
        subprocess.run(command, check=True)
        log(f"Subtitles embedded into {output_video} successfully\n")
    except subprocess.CalledProcessError as e:
        log(f"Error embedding subtitles: {e}\n")
        raise RuntimeError(f"Error embedding subtitles: {e}")
