import whisper

#model = whisper.load_model("base")
model = whisper.load_model("large")
#result = model.transcribe("test.mp3")
result = model.transcribe("2022-OpenHouse.m4a")

#print(result)

print(result["text"])
