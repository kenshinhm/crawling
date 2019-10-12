# selenium 임포트
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

# webdriver 설정(Chrome, Firefox 등)
chrome_options = Options()
# chrome_options.add_argument("--headless")
browser = webdriver.Chrome('./chromedriver', options=chrome_options)

# 크롬 브라우저 내부 대기
browser.implicitly_wait(3)

# 브라우저 사이즈
browser.set_window_size(1920, 1280)  # maximize_window(), minimize_window()

# 페이지 이동
# 서울: https://www.airbnb.co.kr/s/%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C/homes?refinement_paths%5B%5D=%2Fhomes&click_referer=t%3ASEE_ALL%7Csid%3A746e450a-e139-4615-b349-e3b0d57a680e%7Cst%3AMAGAZINE_HOMES&map_toggle=false&query=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C&place_id=ChIJzWXFYYuifDUR64Pq5LTtioU&search_type=AUTOCOMPLETE_CLICK&s_tag=TP433NEm
# 부산: https://www.airbnb.co.kr/s/%EB%B6%80%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C/homes?refinement_paths%5B%5D=%2Fhomes&click_referer=t%3ASEE_ALL%7Csid%3A746e450a-e139-4615-b349-e3b0d57a680e%7Cst%3AMAGAZINE_HOMES&map_toggle=false&query=%EB%B6%80%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C&place_id=ChIJNc0j6G3raDURpwhxJHTL2DU&search_type=AUTOCOMPLETE_CLICK&s_tag=3thrG_ph
# 대전: https://www.airbnb.co.kr/s/%EB%8C%80%EC%A0%84%EA%B4%91%EC%97%AD%EC%8B%9C/homes?refinement_paths%5B%5D=%2Fhomes&click_referer=t%3ASEE_ALL%7Csid%3A746e450a-e139-4615-b349-e3b0d57a680e%7Cst%3AMAGAZINE_HOMES&map_toggle=false&query=%EB%8C%80%EC%A0%84%EA%B4%91%EC%97%AD%EC%8B%9C&place_id=ChIJAWZKutdIZTURtdOKmJ3WltE&search_type=AUTOCOMPLETE_CLICK&s_tag=6ALJwXJa
# 인천: https://www.airbnb.co.kr/s/%EC%9D%B8%EC%B2%9C%EA%B4%91%EC%97%AD%EC%8B%9C/homes?refinement_paths%5B%5D=%2Fhomes&click_referer=t%3ASEE_ALL%7Csid%3A746e450a-e139-4615-b349-e3b0d57a680e%7Cst%3AMAGAZINE_HOMES&map_toggle=false&query=%EC%9D%B8%EC%B2%9C%EA%B4%91%EC%97%AD%EC%8B%9C&place_id=ChIJR4ITliVveTURQmG3LJD9N30&search_type=AUTOCOMPLETE_CLICK&s_tag=2sh-0TDi
# 거제: https://www.airbnb.co.kr/s/%EA%B1%B0%EC%A0%9C%EC%8B%9C--%EA%B2%BD%EC%83%81%EB%82%A8%EB%8F%84--%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD/homes?refinement_paths%5B%5D=%2Fhomes&click_referer=t%3ASEE_ALL%7Csid%3A746e450a-e139-4615-b349-e3b0d57a680e%7Cst%3AMAGAZINE_HOMES&map_toggle=false&query=%EA%B1%B0%EC%A0%9C%EC%8B%9C%2C%20%EA%B2%BD%EC%83%81%EB%82%A8%EB%8F%84%2C%20%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD&place_id=ChIJxxFq8fnMbjURKX-pJeQ7xDw&search_type=AUTOCOMPLETE_CLICK
# 광주: https://www.airbnb.co.kr/s/%EA%B4%91%EC%A3%BC%EA%B4%91%EC%97%AD%EC%8B%9C/homes?refinement_paths%5B%5D=%2Fhomes&click_referer=t%3ASEE_ALL%7Csid%3A746e450a-e139-4615-b349-e3b0d57a680e%7Cst%3AMAGAZINE_HOMES&map_toggle=false&query=%EA%B4%91%EC%A3%BC%EA%B4%91%EC%97%AD%EC%8B%9C&place_id=ChIJr6f1ASOJcTURSPUlAe3S9AU&search_type=AUTOCOMPLETE_CLICK&s_tag=vZ6VaetY
# 속초: https://www.airbnb.co.kr/s/%EC%86%8D%EC%B4%88%EC%8B%9C--%EA%B0%95%EC%9B%90%EB%8F%84--%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD/homes?refinement_paths%5B%5D=%2Fhomes&click_referer=t%3ASEE_ALL%7Csid%3A746e450a-e139-4615-b349-e3b0d57a680e%7Cst%3AMAGAZINE_HOMES&map_toggle=false&query=%EC%86%8D%EC%B4%88%EC%8B%9C%2C%20%EA%B0%95%EC%9B%90%EB%8F%84%2C%20%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD&place_id=ChIJsT1we_S82F8RyD8ltFjA9Ho&search_type=AUTOCOMPLETE_CLICK&s_tag=KZy2Uiiw
# 수원: https://www.airbnb.co.kr/s/%EC%88%98%EC%9B%90%EC%8B%9C--%EA%B2%BD%EA%B8%B0%EB%8F%84--%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD/homes?refinement_paths%5B%5D=%2Fhomes&click_referer=t%3ASEE_ALL%7Csid%3A746e450a-e139-4615-b349-e3b0d57a680e%7Cst%3AMAGAZINE_HOMES&map_toggle=false&query=%EC%88%98%EC%9B%90%EC%8B%9C%2C%20%EA%B2%BD%EA%B8%B0%EB%8F%84%2C%20%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD&place_id=ChIJEUZ2IApDezURybRd7gIwN_E&search_type=AUTOCOMPLETE_CLICK&s_tag=pNJpt1mv
# 울산: https://www.airbnb.co.kr/s/%EC%9A%B8%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C/homes?refinement_paths%5B%5D=%2Fhomes&click_referer=t%3ASEE_ALL%7Csid%3A746e450a-e139-4615-b349-e3b0d57a680e%7Cst%3AMAGAZINE_HOMES&map_toggle=false&query=%EC%9A%B8%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C&place_id=ChIJgd6y4osuZjURATHZM3P6g3A&search_type=AUTOCOMPLETE_CLICK&s_tag=Q2NtMntB

browser.get('https://www.airbnb.co.kr/s/%EC%9A%B8%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C/homes?refinement_paths%5B%5D=%2Fhomes&click_referer=t%3ASEE_ALL%7Csid%3A746e450a-e139-4615-b349-e3b0d57a680e%7Cst%3AMAGAZINE_HOMES&map_toggle=false&query=%EC%9A%B8%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C&place_id=ChIJgd6y4osuZjURATHZM3P6g3A&search_type=AUTOCOMPLETE_CLICK&s_tag=Q2NtMntB')
browser.implicitly_wait(3)

# Scroll 하는 부분
SCROLL_PAUSE_TIME = 2.0

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")

while True:
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

# 소스코드 정리
# print(soup.prettify())

rooms = soup.select("._14csrlku")
# lists = browser.find_elements_by_class_name('_14csrlku')

# print(lists[0].prettify())

room_urls = []

for room in rooms:
    room_url = room.select('meta')[2]['content']
    print(room_url)
    room_urls.append(room_url)

with open('rooms-crawl.txt', 'w+') as file:
    for room_url in room_urls:
        file.write('https://'+room_url+'\n')

browser.implicitly_wait(3)

# 브라우저 종료
browser.quit()
