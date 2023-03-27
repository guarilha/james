import click
from src.capturing import Capturing
import numpy as np

with Capturing() as output:
    import time
    import pyaudio
    import wave
    import sys
    import select
    import vlc


def record_audio(filename: str):
    with Capturing() as output:
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt32  # 32 bits per sample
        channels = 2
        fs = 44100  # Record at 44100 samples per second
        silence_threshold = 500  # Set an appropriate threshold value for silence
        consecutive_silent_chunks = 0
        max_silent_chunks = (10 * fs) // chunk  # 10s of silence
        
        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        stream = p.open(
            format=sample_format,
            channels=channels,
            rate=fs,
            frames_per_buffer=chunk,
            input=True,
        )

        frames = []

    click.echo(click.style("Recording, press Enter to stop...", fg='blue'))
    while True:
        data = stream.read(chunk)
        frames.append(data)
        # Detect silence and update the silent chunks count
        if is_silent(data, silence_threshold):
            consecutive_silent_chunks += 1
        else:
            consecutive_silent_chunks = 0

        # Break the loop if Enter key is pressed or 10s of silence is detected
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0] or consecutive_silent_chunks >= max_silent_chunks:
            break
    
    click.echo(click.style("Saving your question...", fg='blue'))
    
    with Capturing() as output:
        # Stop and close the stream
        stream.stop_stream()
        stream.close()

        # Save the recorded data as a WAV file
        wf = wave.open(f"output/{filename}", "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b"".join(frames))
        wf.close()

        return f"output/{filename}"


def play_audio(filepath: str):
    media = vlc.MediaPlayer(filepath)
    media.play()
    time.sleep(0.1)
    # wait for audio to finish playing or for user to press "c" key
    # print("Playing, press Enter to stop...")
    while media.is_playing():
        time.sleep(0.1)
    #     # wait for Enter key
    #     if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
    #         media.stop()
    #         print("Playback stopped by user")
    #         break

def is_silent(data_chunk, threshold):
    """Returns True if the given data chunk is below the threshold."""
    audio_data = np.frombuffer(data_chunk, dtype=np.int32)
    return np.mean(np.abs(audio_data)) < threshold


