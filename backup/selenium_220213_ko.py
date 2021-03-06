# 220213

# step1.selenium 패키지와 time 모듈 import
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import re
import pandas as pd

import numpy as np  # 데이터 시각화 툴
import matplotlib.pyplot as pyplot  # 데이터 시각화 툴

from konlpy.tag import Kkma
from konlpy.utils import pprint

kkma = Kkma()

# 한글 폰트 사용 위해서 세팅
from matplotlib import font_manager, rc

font_path = 'C:/Windows/Fonts/NanumGothic.ttf'  # 글씨체 수정 바람
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# WordCloud
from wordcloud import WordCloud
from wordcloud import STOPWORDS

wc_details = "" # 이전 코드
ko_details = "" # 전처리 코드

# step2. 크롬드라이버로 원하는 url로 접속(해당 사용자의 url 그때마다 입력)
url = '주소 입력 필요'
# 틀린 주소 예
# 'https://www.daangn.com/u/상세주소?install_from=user_profile'
# 맞는 주소 예
# 'https://www.daangn.com/u/상세주소'
driver = webdriver.Chrome(r"C:\\Users\\chromedriver.exe") # 새 chromedriver로 변경
driver.get(url)
time.sleep(3)

# 유저 닉네임 추출(엑셀 파일 생성에 사용)
user = driver.find_element_by_id("nickname").text
user = user.split(' ', 1)[0]
region_name = driver.find_element_by_id("region_name").text

# 판매 물품 개수 파악 ------------------------------------------------------------------------------ #
# 계속해서 스크롤 다운하면서 데이터를 다 조회하는 코드 : https://hello-bryan.tistory.com/194
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
print(img_nums)

# y 는 section[숫자], z는 article[숫자]
y = int(img_nums / 18)
z = int(img_nums % 18)
if img_nums % 18 == 0:
    y = y - 1
print(y + 1)

data = []  # 크롤링한 데이터를 [제목, 본문] 형식으로 저장할 딕셔너리
data.append([user, region_name])

# 숨김 처리된 글 탐지용
hide_article = False

current_num = 1
# print(driver.current_url)
# str = url + '?page=' + 5

# 카테고리(item_category) 변수
# female = 0  # 카테고리 中 여성의류 개수 변수
# life = 0  # 카테고리 中 생활/가공식품 개수 변수
# child = 0  # 카테고리 中 유아동 개수 변수
# etc = 0  # 카테고리 中 기타 개수 변수

# 디테일(detail) 변수
strings = []

for n in range(1, y + 2):
    new_link = str(url) + '?page=' + str(n)
    driver.get(new_link)

    for m in range(1, 19): 

        # step3. 클릭
        driver.find_element_by_xpath( # 오류 발생
            '//*[@id="user-records"]/section/article[{0}]/a/div[1]/img'.format(m)).click()
        time.sleep(2)

        # step4. 텍스트 추출
        try:
            hide_article = driver.find_element_by_id("no-article").text
        except:
            pass

        if hide_article != 0:
            m = m + 1
            print("({0}/{1})\n--------------------------".format(current_num, img_nums))
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
            # list1 = [item_titles, detail, item_links]
            if n == 1 and m == 1:
                list1 = [user, region_name, item_titles, item_category, detail]
                # print('-> 카테고리는 {0}'.format(item_category))
                # print(type(item_category))

            else:  # 여기서 임시로 데이터 시각화 및 전처리 진행
                list1 = ['', '', item_titles, item_category, detail]
                # print('-> 카테고리는 {0}'.format(item_category))
                # print(type(item_category))
                # if ('여성의류' == item_category):
                #     female += 1
                # elif ('생활/가공식품' == item_category):
                #     life += 1
                # elif ('유아동' == item_category):
                #     child += 1
                # elif ('기타' == item_category):
                #     etc += 1

            strings = detail.split()
            if "***-****-****" in strings:
                print('개인정보 중 전화번호가 존재합니다.')
            print(strings)

            # WordCloud
            sw = set(STOPWORDS)
            sw.add('택배')
            sw.add('가능')
            sw.add('교환')
            sw.add('환불')
            sw.add('불가')
            
            wc_details = wc_details + detail # 예전 코드
            ko_details = ko_details + ' '.join(kkma.nouns(detail))

            type(print(kkma.nouns(detail)))
            #print(kkma.pos(details))

            # wordcloud = WordCloud(width=500, height=500, margin=0, background_color='white',stopwords=sw,
            #                       font_path = 'C:/Windows/Fonts/NanumGothic.ttf').generate(wc_details) # 글씨체 수정 바람

            wordcloud = WordCloud(width=500, height=500, margin=0, background_color='white',stopwords=sw,
                                  font_path = 'C:/Windows/Fonts/NanumGothic.ttf').generate(ko_details)

            data.append(list1)
            # print(detail) # 실행 시간 단축하기 위해 주석 처리
            print("({0}/{1})\n--------------------------".format(current_num, img_nums))
            
            current_num = current_num + 1

        if current_num > img_nums:
            break
        driver.back()

# 카테고리 데이터 시각화
# x = ['여성의류', '생활/가공식품', '유아동', '기타']
# y = [female, life, child, etc]

# title = '{0}_카테고리 시각화'.format(user)
# pyplot.title(title)
# # pyplot.plot(x,y) # 선 그래프
# # pyplot.bar(x,y) # 막대 그래프
# # 원 그래프 : https://diane-space.tistory.com/123 참고
# colors = ["yellowgreen", "gold", "skyblue", "lightcoral"]
# ex = (0, 0, 0, 0) 
#pyplot.pie(y, explode=ex, autopct="%.1f%%", labels=x, colors=colors, shadow=False, startangle=90)
#pyplot.show()
# pyplot.savefig('{0}_matplotlib.png'.format(user))

# WordCloud
pyplot.imshow(wordcloud, interpolation='bilinear')
pyplot.axis("off")
pyplot.margins(x=0, y=0)
pyplot.show()
pyplot.savefig('{0}_wordcloud.png'.format(user)) 

# data 리스트 엑셀 파일로 저장
# data = pd.DataFrame(data)  # 데이터 프레임으로 전환
# data.to_csv('C:/Users/Gram/Desktop/피비엘 csv/{0}_카테고리추가.csv'.format(user), index=False,
#             header=['닉네임', '사는 동네', '판매 품목', '품목 카테고리', '판매 내용'], encoding="utf-8-sig")

driver.quit()
