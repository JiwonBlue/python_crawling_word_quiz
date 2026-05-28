from math import trunc
import requests
from bs4 import BeautifulSoup
import re ##정규식 라이브러리
import os
import json
import random
import csv

from requests.api import get 

##사이트를 파싱해오기 
url = "https://www.usatoday.com"
r = requests.get(url)
bs = BeautifulSoup(r.text, "lxml")
lists = bs.select(".gnt_m_th_a") #부분의 기사

##뉴스기사 읽어오기 
def get_news():
    for li in lists:
        href = url + li["href"]
        r = requests.get(href)
        bs = BeautifulSoup(r.text, "lxml")
        texts = bs.select("div.gnt_ar_b > p.gnt_ar_b_p")
        
        contents = [p.text for p in texts]
        contents = " ".join(contents)
        ##for문 종료해주기 단어게임을 위해 소문자로 전환
        return contents.lower()
    ##오류로인해서 리스트를 못구해올 경우 None 리턴 
    return None
    

# 뜻 하나만 뽑아오게 함
# def naver_translate(word):
#     try:
#         url = "https://ac-dict.naver.com/enko/ac?st=11&r_lt=11&q={}".format(word)
#         r = requests.get(url)
#         j = json.loads(r.text)
#         # print(j["items"][0][0][2][0])
#         #print(j)
        
#         j = j["items"][0][0][2][0].split(',')
#         j = j[0]
#         # print(j)
#         # j = j[0]
        
#         # return (j["items"][0][0][2][0]) #뜻만 뽑아냄
#         return j
#     except:
#         return None

# 네이버 사전 크롤링 Tip
# 사전에 표시되는 단어 내용은 서버에서 데이터를 불러오는 형식이기에 HTML상에 적어둔 것을 크롤링하는 BeautifulSoup으로는 크롤링할 수 없습니다. 
# 이 때는 Network(GET, POST 등)을 이용해 크롤링할 수 있습니다.
# 그래서 저는 아래와 같은 방식으로 크롤링을 하였습니다.
# 결과는 JSON 형식의 stdout.json이라는 파일이 만들어지면서 출력됩니다.

def naver_translate(word):
    try:
        url = "https://ac-dict.naver.com/enko/ac?st=11&r_lt=11&q={}".format(word)
        r = requests.get(url)
        j = json.loads(r.text)
        return (j["items"][0][0][2][0])
        #return (j["items"][0][0][2][0].split(',')[0]) 이렇게하면 뜻 하나만 뽑을 수 있음
    except:
        return None
    
#인터넷으로 얻은 이 파일을 읽어 파이썬에서 처리할 수 있도록 딕셔너리 자료형으로 만들려면 어떻게 해야 할까?
#JSON 파일을 읽어 딕셔너리로 변환하려면 다음처럼 json 모듈을 사용하면 된다.
#JSON 파일을 읽을 때는 이 예처럼 json.load(파일 객체)를 사용한다. 
#이렇게 load() 함수는 읽은 데이터를 딕셔너리 자료형으로 반환한다. 
#반대로 딕셔너리 자료형을 JSON 파일로 생성할 때는 다음처럼 json.dump(딕셔너리, 파일 객체)를 사용한다.


def make_quize(news):
    ##\b는 경계를 의미 
    ##이건 \역슬래쉬를 무시하고 a~z까지 중에 4자리에서 15자리까지만 뽑아와라 왜냐면 of the 이런건 단어게임에 의미가 없음
    match_pattern=re.findall(r'\b[a-z]{4,15}\b',news) ##정규식은 패턴을 뽑아오기 위해 사용한다 Parsing 테크닉에 날개를 달아주는 라이브러리

    frequency = {} #위에서 얻은 단어를 단어 : count 로 숫자를 알기 위해 딕셔너리 생성
    quize_list = [] #얻은 값들을 한국어로 변환시키기 위한 리스트

    for word in match_pattern:
        count = frequency.get(word, 0) ##없는 경우에 default 값이 0으로 설정함
        frequency[word]  = count +1


    ##딕셔너
    for word, count in frequency.items():
        if count > 1:
            kor = naver_translate(word) ##번역을 해야함 API를 쓸 수도 있음 하지만 네이버의 영어사전을 크롤링해서 만들자
            
            if kor is not None:
                quize_list.append([kor , word])
                print(quize_list)
            
            f = open('out2.csv', 'w',  newline='', encoding="utf-8")
            data = quize_list
            writer = csv.writer(f)
            writer.writerows(data)
            f.close()

    return quize_list

def quize():
    make_quize(get_news())
    
quize()