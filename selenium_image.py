# 211018 수정 내용
# 1. colab -> vs code 환경에 맞게 코드 수정
# 2. 필요 없는 코드 삭제
# 3. 추출할 사진 개수 물품 개수만큼 출력하도록 코드 수정

from selenium import webdriver # pip install seleum 설치 필요
#from selenium.webdriver.common.keys import Keys # 현재 필요없다고 나와있는데 일단 보류
import time
import urllib.request # urllib은 이미지 저장을 위해 필요한 라이브러리
# import 관련 오류날 경우 pip install beautifulsoup4 또는 pip install request 설치 필요

# 오류날 경우 참고 : https://emessell.tistory.com/148
# DeprecationWarning: executable_path has been deprecated, please pass in a Service object 이렇게 오류는 나는데 실행하는데에는 지장 없음
# 20211018 모두 같은 경로로 설정 완료!
driver = webdriver.Chrome("C:\\Users\\chromedriver.exe")

# 웹페이지 가져오기(예시 링크는 삭제했습니다.)
driver.get("예시 링크")

# 페이지 로딩이 완료될 때 까지 5초 기다림
driver.implicitly_wait(5)
# 창 최대화
driver.maximize_window()

# --------------------------------------------------------------------------------------- #
# 계속해서 스크롤 다운하면서 데이터를 다 조회하는 코드 : https://hello-bryan.tistory.com/194
SCROLL_PAUSE_SEC = 1

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

# 당근마켓 로고, 사용자 프로필 등 사진을 버리기 위해 -4로 설정
count = -4
# img 태그를 찾음
img = driver.find_elements_by_tag_name("img")
print(len(img))
# --------------------------------------------------------------------------------------- #
# 사진 추출하는 코드 : https://m.blog.naver.com/rhrkdfus/221360694068

for item in img:
    # 페이지 맨 아랫 부분에 필요 없는 사진 4장을 또 버리기 위해 len(img)-8로 설정
    if (count > 0 and count < len(img)-8):
        # C:\Users\jang\Desktop\PBL4 경로에 저장됨
        # jang -> 본인의 계정 이름 변경 필요
        # 바탕화면에 image 폴더 추가 필요 -> 안하시면 바탕화면에 165개의 사진이 업로드 될 수 있습니다..
        full_name = "C:\\Users\\jang\\Desktop\\image\\" + str(count) + ".jpeg"

        try:
            # src를 받는다.
            urllib.request.urlretrieve(item.get_attribute('src'), full_name)
            #print(item.get_attribute('src')[:30] + " : ")

        except:
            # src를 받지 못하는 경우가 간혹 있는데 이런 경우에는 data-src를 받는다.
            urllib.request.urlretrieve(item.get_attribute('data-src'), full_name)
            #print(item.get_attribute('data-src')[:30] + " : ")

        print("{0}. Saving : {1}".format(count, full_name))
    count = count+1

print(len(img))
driver.quit()
print("모두 저장 완료!") # 다 다운받으면 완료 문자열 출력
