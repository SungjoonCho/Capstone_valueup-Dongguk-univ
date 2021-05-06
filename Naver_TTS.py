#네이버 음성합성 Open API 

import os
import sys
import urllib.request

client_id = ""
client_secret = ""

encText = urllib.parse.quote("안녕하세요")
data = "speaker=mijin&speed=0&text=" + encText;
url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"
request = urllib.request.Request(url)
request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
request.add_header("X-NCP-APIGW-API-KEY",client_secret)
response = urllib.request.urlopen(request, data=data.encode('utf-8'))
rescode = response.getcode()

if(rescode==200):
    print("TTS mp3 저장")
    response_body = response.read()
    with open('음성녹음TEST1.mp3', 'wb') as f:
        f.write(response_body)
else:
    print("Error Code:" + rescode)
