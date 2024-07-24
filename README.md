
# SimpleAutoSubs

SimpleAutoSubs is a tool for transcribing and embedding subtitles into videos using [Faster Whisper](https://github.com/SYSTRAN/faster-whisper) and [FFmpeg](https://ffmpeg.org/). The tool offers an easy-to-use GUI to transcribe videos seamlessly embed the transcription as subtitles.

SimpleAutoSubs was developed as part of the [LaCAS Project](https://lacas.inalco.fr/le-projet-lacas) for [INALCO](https://www.inalco.fr/) (Institut National des Langues et Civilisations Orientales).

## Features

- Handles .mp4, .mkv, and .avi inputs. 
- Generate and embed subtitles into video files
- GPU acceleration support

## Installation

### Prerequisites

- Python 3.6 or higher
- FFmpeg
- CUDA Toolkit (If you want GPU acceleration), Note : as of now, faster-whisper only supports CUDA 11.x. 

Check [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit) for installation instructions.


[FFMPEG installation tutorials](https://gist.github.com/barbietunnie/47a3de3de3274956617ce092a3bc03a1) 

### Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/SeidSmatti/SimpleAutoSubs.git
    cd SimpleAutoSubs
    ```

2. Create a virtual environment and activate it (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Install tkinter
   
   For Mac OS
   ```sh
   brew install python-tk
   ```

   For Linux (Debian based)
   ```
   sudo apt-get install python3-tk
   ```

   For Windows

   Usually comes pre-installed with Python, if not see the [official documentation](https://tkdocs.com/tutorial/install.html)
   
## Usage

Run the main script:
```sh
python main.py
```

### GUI Overview

1. **Input File**: Browse and select the video file you want to transcribe. (If the file format is not supported, you can ```ffmpeg -i sourcefile.ext newfile.mp4```)
2. **Output File**: Browse and select the location to save the final video with embedded subtitles.
3. **Model Size**: Choose the size of the Whisper model.
4. **Use GPU**: Check this box if you want to use GPU acceleration.
5. **Include timecodes** : Always check the box except if you only want to use the program to get a clean transcription. (For such cases I recommend [SimpleWhisper](https://github.com/SeidSmatti/SimpleWhisper).
6. **Start Transcription**: Click this button to start the transcription process. (You can correct the eventual mistakes in the textbox before embedding)
7. **Embed Subtitles**: Click this button to embed the generated subtitles into the video.


### Logs

The log box at the bottom of the GUI displays the progress and any messages or errors that occur during the process.

## More Resources

For more information on Whisper, faster-whisper, and CUDA:
- [Open-AI Whisper](https://github.com/openai/whisper)
- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper)
- [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)

## Additions 
- 22/07/2024 : Added manual language selection.

## License

This project is licensed under the GNU General Public License. See the [LICENSE](LICENSE) file for details.

