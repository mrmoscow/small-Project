# AIGO-2023
for  AIGO-2023-NLP-openAI



# AIGO-2023-HW
This is a small project for HomeWork of class Open AI API 之自然語言處理入門與實務

## Requirest python package

- [ ] [Dash](https://dash.plotly.com/)
- [ ] [OpenAI](https://github.com/openai/openai-python)
- [ ] [ffmpeg](https://ffmpeg.org/)

+ openai                   0.27.8
+ dash                     2.11.0
+ dash-core-components     2.0.0
+ dash-html-components     2.0.0
+ dash-table               5.0.0
+ whisper                  1.1.10       

## 使用方式
http://123.194.118.43:8053/
或者你在本地端執行 python ./app.py 使用瀏覽器開啟http://0.0.0.0:8053/

## Support
Please E-mail to: mrmocow@gmail.com

## for 應用1
    ###input,  一段英文文章
    ####output, 一段中文摘要
## for 應用2
    ####input, 上傳mp3 檔案
    ####output,  兩個srt 檔案，一段中英文對照
## note
    ####1. 應用二中 請務必上傳mp3 檔案 之後會加入判斷機制
    ####2. 應用二中 上傳mp3 檔案後，需要時間解析 請稍候 可由網頁瀏覽器上 看uploading 是否繼續執行

##if you can not run the code well
    ###1. change the openai.api_key
    ###2. 由於應用二需要上傳且處理檔案 需要絕對路徑 change the UPLOAD_DIRECTORY, server.route, and location (under def file_download_link)
    ###3. run app-02 for just base part

## License
For open source projects, say how it is licensed.

## Project status
keep working for high score.
