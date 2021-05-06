from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from tkcalendar import *
from tkinter import *
import time
import json
import requests
try:
    from PIL import Image
    from PIL import ImageTk
except ImportError:
    import Image

from bs4 import BeautifulSoup


root = Tk()
root.attributes('-fullscreen', True)
root.configure(background='black')

bgcolor = 'black'

###------------------------------------------------------------------------------ time
now = time.localtime(time.time())
year = now.tm_year
month = now.tm_mon
day = now.tm_mday
hour = now.tm_hour
minute = str(now.tm_min)
if(len(minute) == 1):
    minute = '0'+ minute

t= ['월','화','수','목','금','토','일']
r = now.tm_wday
week = t[r]


# 화면 높이, 너비

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

## 위치 배치는 항상 screen_height width 이용해서 하기
## width는 나누는 수가 클수록 왼쪽 height는 나누는 수가 클수록 위로
# textLabel 1,2 배치

textLabel1=Label(root, text="Microcontroller Study Team",font=('tahoma',20,'bold'),fg='white',bg=bgcolor)
textLabel2=Label(root, text="Smart Front Door",font=('tahoma',40,'bold'),fg='white',bg=bgcolor)

textLabel1.place(x=screen_width/2.8,y=screen_height/1.3)
textLabel2.place(x=screen_width/3.1,y=screen_height/1.5)

# 현재 날짜,시간 배치
date = str(year) +'년 '+ str(month) + '월 ' + str(day) + '일 ' + str(week) + '요일'
if(hour>=13):
    hour = hour-12
    pmam = 'PM'
else:
    pmam = 'AM'

time =  str(hour) +':' +  str(minute) + ' ' + pmam 

date_label = Label(root, text=date,font=('tahoma',20,'bold'),fg='white',bg=bgcolor)

time_label = Label(root, text=time,font=('tahoma',50,'bold'),fg='white',bg=bgcolor)

date_label.place(x=screen_width/25,y=screen_height/4.5)
time_label.place(x=screen_width/25,y=screen_height/10)

###-----------------------------------------------------------------------------날씨API

# 날씨 아이콘 설정 함수
def checking_weather(w):
    
    if '맑' in w:
        answer = 'sun.png'
    elif '비' in w:
        answer = 'rain.png'
    else:
        answer = 'cloudy.png'

    return answer

def checking_weather_mini(w):
    if '맑' in w:
        answer = 'minisun.png'
    elif '비' in w:
        answer = 'minirain.png'
    else:
        answer = 'minicloudy.png'
    return answer

def setting_mini(w):
    if '맑' in w:
        width = 70
        height = 50
    elif '비' in w:
        width = 70
        height = 50
    else:
        width = 70
        height = 50

    return width, height

city = '서울'
country = '강남구'
village = '압구정동'

if(city == '서울'):
    display_city = 'Seoul'

#요청 url, 필수 파라미터, 필수 헤더값 설정
url = "	https://api2.sktelecom.com/weather/current/minutely"
params = {'version':'1','city':city,'county':country,'village':village}
headers= {"appKey":""}

#get방식으로 요청보낸 후 응답받음
response = requests.get(url, params = params,headers = headers)
#print("상태코드: ",response.status_code)

data = response.json()
#print(type(data))
#print(json.dumps(data, indent = 2, ensure_ascii=False))

data = data['weather']["minutely"][0]
weather_status = data["sky"]["name"]

tem_now = str(int(float(data['temperature']['tc'])))+'°C '

# 배치
city_label = Label(root, text=display_city,font=('tahoma',20,'bold'),fg='white',bg=bgcolor)
tem_now_label = Label(root, text=tem_now,font=('tahoma',40),fg='white',bg=bgcolor)

city_label.place(x=screen_width/1.15,y=screen_height/4.4)
tem_now_label.place(x=screen_width/1.15,y=screen_height/7.3)

photo = PhotoImage(file = checking_weather(weather_status))     # png 파일로 그림 저장
photo_label = Label(root, image = photo, bd = 0, bg = bgcolor, width = 150, height= 100)
photo_label.place(x=screen_width/1.35,y=screen_height/7)


#### ---------------------------------------------------------------------------네이버 날씨 크롤링

url = "https://weather.naver.com/rgn/cityWetrCity.nhn?naverRgnCd=09140104"

response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
tem = soup.find_all("div", {"class" : "cell"})

###오늘
def Parsing_tem(tem):
    tem = tem.find('span' , {"class" : "temp"}).text
    tem = str(int(float(tem)))
    tem = tem +'°C '
    return tem

def Parsing_ws(tem):
    status = tem.find('li' , {"class" : "info"}).text
    status = status.split('강')[0]
    return status

# 기온 파싱
tem_tm = '오전 ' + Parsing_tem(tem[0])       #오늘 오전 기온 today morning temperature
tem_ta = '오후 ' + Parsing_tem(tem[1])       #오늘 오후 기온 today afternoon temperature


# 날씨 상태 , 강수량 파싱 
ws_tm = Parsing_ws(tem[0])
rp_tm = tem[0].find('span' , {"class" : "rain"}).text

ws_ta = Parsing_ws(tem[1])
rp_ta = tem[1].find('span' , {"class" : "rain"}).text

###내일 
# 기온 파싱
tem_om = '오전 ' + Parsing_tem(tem[2])          # 내일 오전 
tem_oa = '오후 ' +  Parsing_tem(tem[3])          # 내일 오후

# 날씨 상태 , 강수량 파싱
ws_om = Parsing_ws(tem[2])
rp_om = tem[2].find('span' , {"class" : "rain"}).text

ws_oa = Parsing_ws(tem[3])
rp_oa = tem[3].find('span' , {"class" : "rain"}).text

### 배치
# 날씨 아이콘    
file = checking_weather_mini(ws_tm)
width, height = setting_mini(ws_tm)
ws_tm = PhotoImage(file = file)     # png 파일로 그림 저장
ws_tm_label = Label(root, image = ws_tm, bd = 0, bg = bgcolor, width = width, height= height)
ws_tm_label.place(x=screen_width/1.29,y=screen_height/2.5)

file = checking_weather_mini(ws_ta)
width, height = setting_mini(ws_ta)
ws_ta = PhotoImage(file = file)     # png 파일로 그림 저장
ws_ta_label = Label(root, image = ws_ta, bd = 0, bg = bgcolor, width = width, height= height)
ws_ta_label.place(x=screen_width/1.12,y=screen_height/2.5)

file = checking_weather_mini(ws_om)
width, height = setting_mini(ws_om)
ws_om = PhotoImage(file = file)     # png 파일로 그림 저장
ws_om_label = Label(root, image = ws_om, bd = 0, bg = bgcolor, width = width, height= height)
ws_om_label.place(x=screen_width/1.29,y=screen_height/1.57)

file = checking_weather_mini(ws_oa)
width, height = setting_mini(ws_oa)
ws_oa = PhotoImage(file = file)     # png 파일로 그림 저장
ws_oa_label = Label(root, image = ws_oa, bd = 0, bg = bgcolor, width = width, height= height)
ws_oa_label.place(x=screen_width/1.12,y=screen_height/1.57)


# 날짜 + 오늘 내일 아이콘

to_date = str(month) + '.' + str(day) + ' 오늘'

tem_tm_label = Label(root, text=to_date, font=('tahoma',15,'bold'),fg='white',bg=bgcolor)            # 오늘 날짜 - 오늘
tem_tm_label.place(x=screen_width/1.21,y=screen_height/3)

if(month == 7 and day == 31) or (month == 8 and day == 31):
    tm_month = month + 1
    tm_day = 1
else:
    tm_month = month
    tm_day = day+1
    
tm_date = str(tm_month) + '.' + str(tm_day) + ' 내일'
tem_tm_label = Label(root, text=tm_date, font=('tahoma',15,'bold'),fg='white',bg=bgcolor)            # 오늘 날짜 - 오늘
tem_tm_label.place(x=screen_width/1.21,y=screen_height/1.73)

# 기온 
tem_tm_label = Label(root, text=tem_tm, font=('tahoma',10,'bold'),fg='white',bg=bgcolor)
tem_tm_label.place(x=screen_width/1.29,y=screen_height/2.1)

tem_ta_label = Label(root, text=tem_ta, font=('tahoma',10,'bold'),fg='white',bg=bgcolor)
tem_ta_label.place(x=screen_width/1.12,y=screen_height/2.1)


tem_om_label = Label(root, text=tem_om, font=('tahoma',10,'bold'),fg='white',bg=bgcolor)
tem_om_label.place(x=screen_width/1.29,y=screen_height/1.4)

tem_oa_label = Label(root, text=tem_oa, font=('tahoma',10,'bold'),fg='white',bg=bgcolor)
tem_oa_label.place(x=screen_width/1.12,y=screen_height/1.4)

#----------------------------------------------------------------------------------------- 구글 캘린더 API

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    space = 0
    cnt = 0
    now = time.localtime(time.time())
    month = now.tm_mon
    day = now.tm_mday
    height_step = 1.7
        
    if not events:
        print('No upcoming events found.')
        textLabel1=Label(root, text="일정없음")
        textLabel1.pack(side=LEFT)
        textLabel1=Label(root, text=event['summary'],font=('tahoma',20,'bold'),fg='white',bg='black')
        textLabel1.place(x=0 ,y=750)
        textLabel3.place(x=400,y=40)
        textLabel4.place(x=670,y=150)
        
        f2=Frame(root,width=100,height=0,bg='black')
        f2.pack(side=LEFT)
        #Creating the date column
        l4=Label(f2,text='Date',font=('tahoma',70,'bold'),fg='white',bg='black')
        l4.grid(row=0,column=0)
        cal=DateEntry(f2,dateformat=3,width=50,background='black',
                    foreground='whtie', Calendar = 2019)
        cal=DateEntry(f2,selectbackground='lightgreen',
                 selectforeground='red',
                 normalbackground='black',
                 normalforeground='white',
                 background='black',
                 foreground='white',
                 bordercolor='black',
                 othermonthforeground='gray50',
                 othermonthbackground='black',
                 othermonthweforeground='gray50',
                 othermonthwebackground='black',
                 weekendbackground='black',
                 weekendforeground='white',
                 headersbackground='black',
                 headersforeground='gray30')
        cal.grid(row=1,column=0,sticky='nsew')
        
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))

##     -----------------------------------------달력   
        
##        f2=Frame(root,width=100,height=100,bg='black')
##        f2.pack(side=LEFT)
##        #Creating the date column
##        l4=Label(f2,text='Date',font=('tahoma',20,'bold'),fg='white',bg='black')
##        l4.place(x=screen_width/27,y=screen_height/2)
##        
##        
##        cal=DateEntry(f2,dateformat=3,width=50,background='black',
##                    foreground='whtie', Calendar = 2019)
##        cal=DateEntry(f2,selectbackground='lightgreen',
##                 selectforeground='red',
##                 normalbackground='black',
##                 normalforeground='white',
##                 background='black',
##                 foreground='white',
##                 bordercolor='black',
##                 othermonthforeground='gray50',
##                 othermonthbackground='black',
##                 othermonthweforeground='gray50',
##                 othermonthwebackground='black',
##                 weekendbackground='black',
##                 weekendforeground='white',
##                 headersbackground='black',
##                 headersforeground='gray30')
##        cal.grid(row=1,column=0,sticky='nsew')


##        --------------------------------------일정 나열
        
        event_date = start[0:10]

        print("11")
        if (int(event_date[-2:]) == day+1 and cnt == 1):
            cnt = 2
        elif int(event_date[-2:]) > day+1 or int(event_date[5:7]) is not month :    # 날수가 현재 날짜보다 2일 이상 차이나거나 다른 달이면 이벤트 출력 X
            break
        
        print("1")

        event_time = start[11:16]
        print("2")
        event_hour = int(event_time[0:2])
        print("3")
        
        pmam = 'AM'

        event_time = list(event_time)
        
        print("5")
        
        if int(event_hour) >= 13:
            event_hour -= 12
            event_hour = str(event_hour)
            if(len(event_hour) == 1):
                event_hour = '0' + event_hour
                event_time[0] = event_hour[0]
                event_time[1] = event_hour[1]
            else:
                event_time[0] = event_hour[0]
                event_time[1] = event_hour[1]
            pmam = 'PM'
            
            
        if(cnt == 0 or cnt == 2):
            print('\n',event_date)
            event_date_label = Label(root, text=event_date, font=('tahoma',10,'bold'),fg='yellow',bg='black')
            event_date_label.place(x=screen_width/27,y=screen_height/height_step)
            height_step -= 0.07
            cnt += 1

        event_time = ''.join(event_time)

        
        
        event_time_label = Label(root, text=(event_time+' '+ pmam), font=('tahoma',10,'bold'),fg='white',bg='black')
        textLabel1=Label(root, text=event['summary'],font=('tahoma',10,'bold'),fg='white',bg='black')
        
        event_time_label.place(x=screen_width/27,y=screen_height/height_step)
        textLabel1.place(x=screen_width/10,y=screen_height/height_step)

        height_step -= 0.07

        

        
        
        print(event_time,pmam, event['summary'])
        
if __name__ == '__main__':
    main()
    


 












