import os
import sys
import argparse
import speech_recognition as sr
from pydub import AudioSegment
from tqdm import tqdm
import concurrent.futures
from queue import Queue
from functools import partial

def get_ffmpeg_path():
    if hasattr(sys, '_MEIPASS'):
        # When running in a PyInstaller bundle
        ffmpeg_dir = os.path.join(sys._MEIPASS, 'ffmpeg')
    else:
        # When running in a normal Python environment
        ffmpeg_dir = os.path.abspath("ffmpeg")

    ffmpeg_path = os.path.join(ffmpeg_dir, 'ffmpeg.exe')
    ffprobe_path = os.path.join(ffmpeg_dir, 'ffprobe.exe')
    ffplay_path = os.path.join(ffmpeg_dir, 'ffplay.exe')

    return ffmpeg_path, ffprobe_path, ffplay_path

ffmpeg_path, ffprobe_path, ffplay_path = get_ffmpeg_path()
os.environ["FFMPEG_BINARY"] = ffmpeg_path
os.environ["FFPROBE_BINARY"] = ffprobe_path
os.environ["FFPLAY_BINARY"] = ffplay_path

# Function to process each audio chunk and recognize speech
def recognize_chunk(chunk_index, audio_chunk, recognizer, language, results_queue, progress_bar):
    chunk_wav = f"chunk_{chunk_index}.wav"
    audio_chunk.export(chunk_wav, format="wav")

    with sr.AudioFile(chunk_wav) as source:
        audio_data = recognizer.record(source)
        try:
            result = recognizer.recognize_google(audio_data, language=language, show_all=True)
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            result = None
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            result = None
    
    os.remove(chunk_wav)
    results_queue.put((chunk_index, result))
    progress_bar.update(1)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Convert MP3 to text using Google Speech Recognition")
    parser.add_argument("file_path", type=str, help="Path to the MP3 file")
    parser.add_argument("-i", "--language", type=str, default="it-IT", help="Language code for recognition (default: it-IT). Use 'en-US' for English")

    args = parser.parse_args()
    mp3_file = args.file_path
    language = args.language

    # Convert MP3 to WAV
    audio = AudioSegment.from_mp3(mp3_file)
    duration = len(audio)  # Duration in milliseconds

    # Ensure the audio is not empty
    if len(audio) == 0:
        print("The audio file is empty.")
        return

    print(f"Total duration of audio: {duration / 60000:.2f} min")

    # Split audio into chunks of 5 minutes each (300,000 ms)
    chunk_length = 1 * 60 * 1000  # 5 minutes in milliseconds
    chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]

    # Initialize recognizer
    recognizer = sr.Recognizer()
    output_file = "recognition_result.txt"
    results_queue = Queue()

    with open(output_file, "w", encoding="utf-8") as file:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            chunk_bars = [tqdm(total=1, desc=f"Chunk {i}", position=i + 1, leave=False) for i in range(len(chunks))]
            futures = {
                executor.submit(partial(recognize_chunk, i, chunk, recognizer, language, results_queue, chunk_bars[i])): i
                for i, chunk in enumerate(chunks)
            }
            
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Overall Progress", position=0, leave=True):
                chunk_index = futures[future]
                try:
                    future.result()
                except Exception as exc:
                    print(f"Chunk {chunk_index} generated an exception: {exc}")

        # Retrieve results from the queue and write to file
        results = [None] * len(chunks)
        while not results_queue.empty():
            chunk_index, result = results_queue.get()
            results[chunk_index] = result

        for i, result in enumerate(results):
            if result:
                file.write(f"Chunk {i}:\n{result}\n")

    print(f"Recognition result written to {output_file}")

if __name__ == "__main__":
    main()
