import speech_recognition as sr
from queue import Queue
from time import sleep

def main():
    data_queue = Queue()
    recorder = sr.Recognizer()
    recorder.dynamic_energy_threshold = False
    source = sr.Microphone(sample_rate=16000)
    with source:
        recorder.adjust_for_ambient_noise(source)
    def record_callback(_, audio:sr.AudioData) -> None:
        data = audio.get_raw_data()
        data_queue.put(data)
    recorder.listen_in_background(source, record_callback, phrase_time_limit=5)
    while True:
        try:
            if not data_queue.empty():
                data_queue.queue.clear()
                print("received audio")
            else:
                # Infinite loops are bad for processors, must sleep.
                sleep(0.25)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()