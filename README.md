# MP3 to Text Converter Using Google Speech Recognition

A Python tool to convert MP3 audio files into text transcriptions using Google’s Speech Recognition API. This program handles large audio files by splitting them into manageable chunks and processing each chunk concurrently, enhancing performance and providing progress feedback to the user. 

## Key Features
- **Multi-Threaded Processing**: Breaks down large audio files into chunks and processes them concurrently for faster transcription.
- **Language Support**: Allows you to specify the language code (default: Italian, `it-IT`) for accurate transcription in multiple languages.
- **FFmpeg Integration**: Converts MP3 files to WAV format for better compatibility, utilizing FFmpeg binaries.
- **Progress Tracking**: Displays progress bars for each audio chunk, providing real-time feedback.
- **Error Handling**: Catches network and unrecognizable audio errors for smooth operation.

## Requirements
- **Python 3.x**
- **FFmpeg**: Needed for audio conversion. The tool supports embedding FFmpeg binaries, making it compatible with PyInstaller for bundled distribution.
- **Google Speech Recognition API**: Uses Google’s API for high transcription accuracy.

## Installation

1. Install [Python 3.12.1](https://www.python.org/downloads/)
2. Install the dipendencies using ```pip install -r /path/to/requirements.txt```
4. Install the [FFMPEG Libraries](https://ffmpeg.org/download.html)
   - Windows:
     You must add the `bin` folder to the enviroment variables for the current user, to do so:
      1. Search on the Windows search bar ```Enviroment Variables```
      2. Click once on `Path` then press `Edit`
      3. Click on `New` then add the path to the `bin` folder (example: ```C:\Program Files\ffmpeg\bin```)
      4. Press `Ok` 3 times to apply changes
      5. Check if FFmpeg is installed by running: ```ffmpeg -version``` on the `CMD` this should display the FFmpeg version if the installation was successful.
    - Linux:
       1. For Debian/Ubuntu-based systems:
            ```
            sudo apt update
            sudo apt install ffmpeg
            ```
      2. For Fedora-based systems:
            ```
         sudo dnf install ffmpeg
            ```
      4. For Arch Linux:
            ```
         sudo pacman -S ffmpeg
            ```
      5. Check if FFmpeg is installed by running: ```ffmpeg -version``` this should display the FFmpeg version if the installation was successful.
5. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mp3-to-text-converter.git
   cd mp3-to-text-converter
   ```


## Usage
To use the MP3 to Text Converter, simply provide the path to the MP3 file and, optionally, a language code for transcription.

```python Main.py your_audio_file.mp3 --language en-US```

Command-Line Arguments:
- `file_path` (required): Path to the MP3 file you want to transcribe.
- `--language` (optional): Language code for transcription (default is `it-IT` for Italian). Use `en-US` for English.

Example:
`python Main.py example_audio.mp3 --language en-US` 

The transcription will be saved in a text file named recognition_result.txt in the same directory as the script.

## How It Works
- Audio Conversion: The MP3 file is converted to WAV format using FFmpeg for better compatibility with the speech recognition library.
- Chunking: The audio is split into 1-minute chunks for efficient processing.
- Parallel Processing: Each chunk is transcribed in parallel using multithreading.
- Error Handling: Catches and logs network errors and unrecognizable audio segments.
- Result Compilation: All chunks are compiled into a single output text file.
