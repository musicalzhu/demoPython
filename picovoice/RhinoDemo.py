import pvrhino
import struct
import pyaudio
import os

pa = None
handle = None
audio_stream = None

try:
    pa = pyaudio.PyAudio()
    inpath = "/home/pi/python/picovoice/chess_en_raspberry-pi_2021-08-02-utc_v1_6_0.rhn"

    handle = pvrhino.create(inpath)

    audio_stream = pa.open(
                        rate=handle.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=handle.frame_length)

    def get_next_audio_frame():
        pcm = audio_stream.read(handle.frame_length)
        pcm = struct.unpack_from("h" * handle.frame_length, pcm)
        return pcm

    letterDic = {
    "ALPHA": 'A',
    "BRAVO": 'B',
    "CHARLIE": 'C',
    "DELTA": 'D',
    "ECHO":'E',
    "FOXTROT": 'F',
    "GOLF": 'G',
    "HOTEL": 'H'
    }

    numberDic = {
    "ONE": 1,
    "TWO": 2,
    "THREE": 3,
    "FOUR": 4,
    "FIVE": 5,
    "SIX": 6,
    "SEVEN": 7,
    "EIGHT": 8
    }

    def format_speech(recognized_text):

        from_letter = recognized_text.get("r1")
        from_number = recognized_text.get("l1")
        to_letter = recognized_text.get("r2")
        to_number = recognized_text.get("l2")
            
        from_letter = letterDic.get(from_letter.upper())
        from_number = numberDic.get(from_number.upper())
        to_letter = letterDic.get(to_letter.upper())
        to_number = numberDic.get(to_number.upper())
            
        return from_letter,from_number,to_letter,to_number


    while True:
        is_finalized = handle.process(get_next_audio_frame())

        if is_finalized:
            inference = handle.get_inference()
            if not inference.is_understood:
                # add code to handle unsupported commands
                print("unsupported commands!")
            else:
                intent = inference.intent
                slots = inference.slots
                # add code to take action based on inferred intent and slot values
                print("intent: " + str(intent) + "  slots: " + str(slots))
                print("format_speech: " + str(format_speech(slots)))
   

finally:
    if handle is not None:
        handle.delete()

    if audio_stream is not None:
        audio_stream.close()

    if pa is not None:
            pa.terminate()

