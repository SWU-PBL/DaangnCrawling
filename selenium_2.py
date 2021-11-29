# step1.selenium 패키지와 time 모듈 import
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import re
import pandas as pd

# step2.크롬드라이버로 원하는 url로 접속(해당 사용자의 url 그때마다 입력)
url = 'https://www.daangn.com/u/상세주소'
# 틀린 주소 예
# 'https://www.daangn.com/u/상세주소?install_from=user_profile'
# 맞는 주소 예
# 'https://www.daangn.com/u/상세주소'
driver = webdriver.Chrome('C:/Users/chromedriver.exe')
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
print(y + 1)

data = []  # 크롤링한 데이터를 [제목, 본문] 형식으로 저장할 딕셔너리

# 숨김 처리된 글 탐지용
hide_article = False

current_num = 1
# print(driver.current_url)
# str = url + '?page=' + 5

for n in range(1, y + 2):
    new_link = str(url) + '?page=' + str(n)
    driver.get(new_link)

    for m in range(1, 19):

        # step3. 클릭
        driver.find_element_by_xpath(
            '//article[{0}]/a/div[1]/img'.format(m)).click()
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
            else:
                list1 = ['', '', item_titles, item_category, detail]
            data.append(list1)
            print(detail)
            print("({0}/{1})\n--------------------------".format(current_num, img_nums))
            current_num = current_num + 1

        if current_num > img_nums:
            break
        driver.back()

# data 리스트 엑셀 파일로 저장
data = pd.DataFrame(data)  # 데이터 프레임으로 전환
data.to_csv('C:/파일경로/{0}_카테고리추가.csv'.format(user), index=False,
            header=['닉네임', '사는 동네', '판매 품목', '품목 카테고리', '판매 내용'], encoding="utf-8-sig")

driver.quit()
