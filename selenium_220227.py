# 220227
# 자연어 처리(Konlpy), 데이터 시각화(카테고리, wordcloud) 코드 통합 완료
# 불용어사전 정의 완료

# selenium 패키지와 time 모듈
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
# import re
import pandas as pd

# 데이터 시각화 툴
import numpy as np
import matplotlib.pyplot as pyplot
from PIL import Image

# 자연어 처리 및 불용어
import nltk
from konlpy.tag import Kkma
from konlpy.tag import Okt
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# from konlpy.utils import pprint

Kkma = Kkma() # 더 나은 결과를 위해 kkma로 변경

# 한글 폰트 사용 위해서 세팅
from matplotlib import font_manager, rc

font_path = 'C:/Users/(글꼴 경로 설정)/NanumGothic.ttf'  #글씨체
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# WordCloud
from wordcloud import WordCloud
# from wordcloud import STOPWORDS

wc_details = "" # 자연어 처리 이전 코드
kkma_details = "" # 자연어 처리 후 코드

## 크롬드라이버로 원하는 url로 접속(해당 사용자의 url 그때마다 입력)
url = 'https://www.daangn.com/u/(사용자고유번호)'
# 틀린 주소 예
# 'https://www.daangn.com/u/상세주소?install_from=user_profile'
# 맞는 주소 예
# 'https://www.daangn.com/u/상세주소'
driver = webdriver.Chrome(r"C:/Users/(ChromeDriver 경로 설정)/chromedriver.exe") # 실행 안될 시 새로운 chromedriver 버전으로 변경
driver.get(url)
time.sleep(3)

# 유저 닉네임 추출(엑셀 파일 생성에 사용)
user = driver.find_element_by_id("nickname").text
user = user.split(' ', 1)[0]
region_name = driver.find_element_by_id("region_name").text

## 판매 물품 개수 파악
SCROLL_PAUSE_SEC = 2

# 스크롤 높이 가져옴
last_height = driver.execute_script("return document.body.scrollHeight")

# 스크롤 끝까지 내려가는 코드
while True:
    # 끝까지 스크롤 다운
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 1초 대기
    time.sleep(SCROLL_PAUSE_SEC)

    # 스크롤 다운 후 스크롤 높이 다시 가져옴
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 판매 갯수 추출
img = driver.find_elements_by_tag_name("img")
img_nums = len(img) - 9
# print(img_nums)

# y 는 section[숫자], z는 article[숫자]
y = int(img_nums / 18)
z = int(img_nums % 18)
if img_nums % 18 == 0:
    y = y - 1
# print(y + 1)

data = []  # 크롤링한 데이터를 [제목, 본문] 형식으로 저장할 딕셔너리
data.append([user, region_name])

# 숨김 처리된 글 탐지용
hide_article = False

# 현재 페이지 수
current_num = 1

# 카테고리(item_category) 변수
life = 0  # 생활용품
child = 0  # 유아동
female = 0  # 여성의류/잡화
male = 0  # 남성의류/잡화
interest = 0  # 취미/여가
beauty = 0  # 뷰티/미용
pet = 0  # 반려동물용품
etc = 0  # 기타

life_list = ["생활가전", "가구/인테리어"]
child_list = ["유아도서", "유아동"]
female_list = ["여성잡화", "여성의류"]
male_list = ["남성패션/잡화"]
interest_list = ["게임/취미", "스포츠/레저", "도서/티켓/음반", "식물"]
beauty_list = ["뷰티/미용"]
pet_list = ["반려동물용품"]
etc_list = ["기타 중고물품", "삽니다", "디지털기기"]

# 디테일(detail) 변수
strings = []

for n in range(1, y + 2):
    new_link = str(url) + '?page=' + str(n)
    driver.get(new_link)

    for m in range(1, 19): 

        # step3. 클릭
        driver.find_element_by_xpath(
            '//*[@id="user-records"]/section/article[{0}]/a/div[1]/img'.format(m)).click()
        time.sleep(2)

        # step4. 텍스트 추출
        try:
            hide_article = driver.find_element_by_id("no-article").text
        except:
            pass

        if hide_article != 0:
            m = m + 1
            print("현재 상품 : {0} / 총 상품 개수 : {1}\n-----------------------------------".format(current_num, img_nums))
            current_num = current_num + 1
            hide_article = False
        else:
            item_titles = driver.find_element_by_id("article-title").text
            item_category = driver.find_element_by_id("article-category").text
            item_category = item_category.split(' ', 1)[0]
            item_details = driver.find_elements_by_id("article-detail")
            item_links = driver.current_url

            # 리스트 속 리스트로 크롤링한 내용 저장
            for i in item_details:
                i = i.text
            detail = "".join(i)

            if n == 1 and m == 1:
                list1 = [user, region_name, item_titles, item_category, detail]

            else:  # 여기서 임시로 데이터 시각화 및 전처리 진행
                list1 = list1 = ['', '', item_titles, item_category, detail]

                if item_category in life_list:
                    life += 1
                elif item_category in child_list:
                    child += 1
                elif item_category in female_list:
                    female += 1
                elif item_category in male_list:
                    male += 1
                elif item_category in interest_list:
                    interest += 1
                elif item_category in beauty_list:
                    beauty += 1
                elif item_category in pet_list:
                    pet += 1
                elif item_category in etc_list:
                    etc += 1

            # 개인정보 中 전화번호 탐지
            strings = detail.split()
            if "***-****-****" in strings:
                print('개인정보 중 전화번호가 존재합니다.')
            # print(strings)

            ## 불용어 처리
            kkma_details = kkma_details + ' '.join(Kkma.nouns(detail))

            # 사용자가 정의한 불용어 사전 불러오기
            stop_words = []
            f = open('C:/Users/(불용어 사전 경로 설정)/stopwords.txt', 'r', encoding = 'utf-8')
           
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                stop_words.append(line)
            f.close()

            word_tokens = word_tokenize(kkma_details)

            word_result = [w for w in word_tokens if w not in stop_words]
            word_result = ' '.join(word_result)
            # print(word_result)

            wordcloud = WordCloud(width=500, height=500, margin=0, background_color='white', 
                                    font_path = 'C:/Users/j2won/NanumGothic.ttf').generate(word_result) # 글씨체 수정 바람

            data.append(list1)
            # print(detail) # 실행 시간 단축하기 위해 주석 처리
            print("현재 상품 : {0} / 총 상품 개수 : {1}\n-----------------------------------".format(current_num, img_nums))

            current_num = current_num + 1

        if current_num > img_nums:
            break
        driver.back()

## 카테고리 시각화
x = ['생활용품', '유아동', '여성의류/잡화', '남성의류/잡화', '취미/여가', '뷰티/미용', '반려동물용품', '기타']
y = [life, child, female, male, interest, beauty, pet, etc]
title = '{0}_카테고리 시각화'.format(user)
pyplot.title(title)
pyplot.ylabel('개수')
pyplot.xticks(rotation = 45)
# pyplot.xticks(range(5), x)
colors = ['C0','C1','C2','C3','C4','C5','C6','C7']
pyplot.bar(x, y, color = colors) # 막대 그래프
# pyplot.show()
pyplot.savefig('C:/Users/(데이터 전처리 및 가공 결과 경로 설정)/{0}_matplotlib.png'.format(user))
# -> show() 함수 혹은 savefig 함수 둘 중 하나만 사용해야 함

## WordCloud
title = '{0}_WordCloud'.format(user)
pyplot.title(title)
pyplot.imshow(wordcloud, interpolation='bilinear')
pyplot.axis("off")
pyplot.margins(x=0, y=0)
# pyplot.show()
pyplot.savefig('C:/Users/(데이터 전처리 및 가공 결과 경로 설정)/{0}_wordcloud.png'.format(user))
# -> show() 함수 혹은 savefig 함수 둘 중 하나만 사용해야 함

## data 리스트 엑셀 파일로 저장
data = pd.DataFrame(data)  # 데이터 프레임으로 전환
data.to_csv('C:/Users/(excel 저장 경로 설정)/{0}_카테고리추가.csv'.format(user), index = False,
            header = ['닉네임', '사는 동네', '판매 품목', '품목 카테고리', '판매 내용'], encoding = "utf-8-sig")

driver.quit() 
