import whisper
from datetime import timedelta
import os

def transcribe_audio(file):
    #model = whisper.load_model("base") # Change this to your desired model
    model = whisper.load_model("large")
    #print("Whisper model loaded.")
    #video = download_video(path)
    transcribe = model.transcribe(file)
    #os.remove(video["file_name"])
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
        #segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"

        #srtFilename = os.path.join(r"C:\Transcribe_project", "your_srt_file_name.srt")
        srtFilename = './result.srt'
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    return srtFilename


#transcribe_audio("./test.mp3")
#transcribe_audio("2022-OpenHouse.m4a")
transcribe_audio("M1acc.mp3")
#model = whisper.load_model("base")
#model = whisper.load_model("large")
#result = model.transcribe("test.mp3")
#result = model.transcribe("2022-OpenHouse.m4a")

#print(result)
#print(result["text"])
