# selenium 임포트
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import time
from bs4 import BeautifulSoup
import os
import urllib.request as req
import urllib

start_idx = 0

# Header 정보 초기화
opener = req.build_opener()
# Header 정보 삽입
req.install_opener(opener)

# webdriver 설정(Chrome, Firefox 등)
chrome_options = Options()
# chrome_options.add_argument("--headless")
browser = webdriver.Chrome('./chromedriver', options=chrome_options)

# 크롬 브라우저 내부 대기
browser.implicitly_wait(5)

# 브라우저 사이즈
browser.set_window_size(1920, 1280)  # maximize_window(), minimize_window()

# 페이지 이동
browser.get('https://www.google.com/search?biw=1920&bih=959&tbm=isch&sxsrf=ACYBGNQYzoJIpNTcNFH0ypzZvFrN3ASdPg%3A1570880454466&sa=1&ei=xruhXYmGHI2Xr7wP4Yei2Ac&q=hands+on+face&oq=hands+on+face&gs_l=img.3..0i19l10.9555.10826..10932...0.0..0.108.1188.7j5......0....1..gws-wiz-img.......35i39j0j0i30.yaKsP5zOrlI&ved=0ahUKEwiJgeTb0ZblAhWNy4sBHeGDCHsQ4dUDCAc&uact=5')
browser.implicitly_wait(5)

# Scroll 하는 부분
SCROLL_PAUSE_TIME = 5.0

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")

for i in range(5):
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    browser.implicitly_wait(SCROLL_PAUSE_TIME)
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


# bs4 초기화
soup = BeautifulSoup(browser.page_source, "html.parser")

images = soup.select("img")

for i, image in enumerate(images):
    # 이미지 번호를 붙여주면서 다운로드
    # 속성 확인
    # print(img_list['data-source'])

    # 저장 파일명 및 경로
    idx = start_idx + i
    jpg_filename = os.path.join(os.getcwd(), 'tmp', '{}.jpg'.format(idx))
    png_filename = os.path.join(os.getcwd(), 'tmp', '{}.png'.format(idx))
    # 파일명 출력
    # print('full name : {}'.format(fullFileName))

    # 다운로드 요청(URL, 저장경로)
    url = ''
    if 'data-src' in image.attrs:
        url = image['data-src']
    elif 'src' in image.attrs:
        url = image['src']

    try:
        if 'png' in url:
            req.urlretrieve(url, png_filename)
        else:
            req.urlretrieve(url, jpg_filename)
    except Exception as e:
        print(e)
    print("{}th image, url: {}".format(i, url))

# 다운로드 완료 시 출력
print("download succeeded!")

# 브라우저 종료
browser.quit()
