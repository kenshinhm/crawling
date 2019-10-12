# selenium 임포트
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import django
import os
import urllib.request
from django.core.files.uploadedfile import SimpleUploadedFile
import requests
import imghdr

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from airbnb.rooms.models import Room, RoomPhoto
from airbnb.users.models import User

city_urls = {}
city_list = ['서울특별시',
             '부산광역시',
             '대전광역시',
             '인천광역시',
             '거제시',
             '광주광역시',
             '속초시',
             '수원시',
             '울산광역시']

with open('rooms_100.txt', 'r') as file:
    lines = file.readlines()
    city = ''

    for line in lines:
        if line[:-1] in city_list:
            city = line[:-1]
            city_urls[city] = []
        else:
            city_urls[city].append(line)

# webdriver 설정(Chrome, Firefox 등)
chrome_options = Options()
# chrome_options.add_argument("--headless")
browser = webdriver.Chrome('./chromedriver', options=chrome_options)

# 크롬 브라우저 내부 대기
browser.implicitly_wait(3)
time.sleep(3)

# 브라우저 사이즈
browser.set_window_size(1920, 1280)  # maximize_window(), minimize_window()

for city, urls in city_urls.items():

    '''
    도시 설정
    '''
    db_city = city
    print(city)
    print()

    target_city = "울산광역시"
    if city != target_city:
        continue

    for url in urls:
        print(url)
        print()

        room_id_start_idx = url.find('rooms/') + len('rooms/')
        room_id_end_idx = url.find('?location')
        room_id = url[room_id_start_idx: room_id_end_idx]

        # 페이지 이동
        try:
            browser.get(url)
            browser.implicitly_wait(2)
            time.sleep(2)

            # 버튼 누르기
            browser.implicitly_wait(2)
            # browser.find_element_by_id('details').find_element_by_class_name('_1dv8bs9v').click()
            browser.find_element_by_id('details').find_element_by_class_name('_1dv8bs9v').send_keys(Keys.ENTER)
            browser.implicitly_wait(2)

            # bs4 초기화
            soup = BeautifulSoup(browser.page_source, "html.parser")

            # 소스코드 정리
            # print(soup.prettify())
        except Exception as err:
            print()
            print(err)

        '''
        이미지 가져오기
        '''
        time.sleep(2)

        try:
            db_room_photo_urls = []
            room_photos = soup.select_one("._167bw5o").select("img._uttz43")
            for room_photo in room_photos:
                db_room_photo_urls.append(room_photo['src'])
        except Exception as err:
            print()
            print(err)
        finally:
            for idx, db_room_photo in enumerate(db_room_photo_urls):
                print('{}번째 Image URL: {}'.format(idx, db_room_photo))

        '''
        방 제목 가져오기
        '''
        time.sleep(1)
        try:
            db_name = soup.select_one("div#summary").select_one("span._18hrqvin").text
            db_location = soup.select_one("div#summary").select_one("div._1hpgssa1").select_one("div._czm8crp").text
        except Exception as err:
            print()
            print(err)
        finally:
            print()
            print('title: {}'.format(db_name))
            print('location: {}'.format(db_location))

        '''  
        방 정보 가져오기
        '''
        time.sleep(1)

        db_capacity = 1
        db_bedroom = 1
        db_bed = 1
        db_bathroom = 1

        try:
            db_type = soup.select_one("div#summary").next_sibling.select_one("div._hgs47m").select_one(
                "div._1p3joamp").text

            room_infos = soup.select_one("div#summary").next_sibling.select_one("div._hgs47m").select("div._czm8crp")
            db_capacity = room_infos[0].text[-2]
            db_bedroom = 1 if room_infos[1].text == '원룸' else room_infos[1].text[-2]
            db_bed = room_infos[2].text[-2]
            db_bathroom = room_infos[3].text[-2]

        except Exception as err:
            print()
            print(err)

        finally:
            print()
            print('room_type: {}'.format(db_type))
            print()
            print('capacity_cnt: {}'.format(db_capacity))
            print('bedroom_cnt: {}'.format(db_bedroom))
            print('bed_cnt: {}'.format(db_bed))
            print('bathroom_cnt: {}'.format(db_bathroom))

        '''  
        방 소개 가져오기
        '''
        time.sleep(1)
        try:
            test_tag = soup.select_one("div#details > div").contents[0]
            if not test_tag.attrs:
                start_idx = 0
            else:
                start_idx = 1

            room_summary = soup.select_one("div#details > div").contents[start_idx]
            spans_root = room_summary.select('span._czm8crp')
            db_summary = ''

            for span_root in spans_root:
                spans = span_root.select('span')

                for span in spans:
                    db_summary += str(span.text)
                    db_summary += '\n'

                db_summary += '\n'

            db_summary = db_summary[:-2]

            db_room_infos = ['', '', '', '']
            room_detail_tag = soup.select_one("div#details > div").contents[start_idx+1]
            room_detail_tag = room_detail_tag.select_one("div._kj7i925 > div")

            for i, content in enumerate(room_detail_tag.contents):

                title = content.select_one("div._1p3joamp").text
                room_detail = str(title) + '\n\n'
                spans_root = content.select('span._czm8crp')

                for span_root in spans_root:
                    spans = span_root.select('span')

                    for span in spans:
                        room_detail += str(span.text)
                        room_detail += '\n'

                    room_detail += '\n'

                db_room_infos[i] = room_detail[:-2]

        except Exception as err:
            print()
            print(err)

        finally:
            print()
            print(db_summary)
            print()
            for db_room_info in db_room_infos:
                print(db_room_info)

        '''
        방 lat, lng 가져오기
        '''
        time.sleep(1)

        try:

            script_tag = soup.select_one("script[data-state=true]")
            lat_start_idx = script_tag.text.find('"lat"') + len('"lat":')
            lng_start_idx = script_tag.text.find('"lng"') + len('"lng":')

            db_lat = script_tag.text[lat_start_idx:lat_start_idx + 11].split(',')[0]
            db_lng = script_tag.text[lng_start_idx:lng_start_idx + 13].split(',')[0]

            if db_lat == 'null':
                google_map_src = soup.select_one("._1fmyluo4 > img")['src']
                cut_word_from = 'center='
                cut_word_to = '&scale'
                cut_index_from = google_map_src.find(cut_word_from) + len(cut_word_from)
                cut_index_to = google_map_src.find(cut_word_to)

                latlng = google_map_src[cut_index_from:cut_index_to]
                db_lat = latlng.split(',')[0]
                db_lng = latlng.split(',')[1]
                print('lat: {}, lng: {}'.format(db_lat, db_lng))
            else:
                print()
                print('lat: {}, lng: {}'.format(db_lat, db_lng))

        except Exception as err:
            print()
            print(err)

        browser.implicitly_wait(1)

        # DB create
        db_host = User.objects.get(username='admin')

        room = Room.objects.create(name=db_name,
                                   city=db_city,
                                   location=db_location,
                                   type=db_type,
                                   capacity=db_capacity,
                                   bedroom=db_bedroom,
                                   bathroom=db_bathroom,
                                   bed=db_bed,
                                   summary=db_summary,
                                   room_info_0=db_room_infos[0],
                                   room_info_1=db_room_infos[1],
                                   room_info_2=db_room_infos[2],
                                   room_info_3=db_room_infos[3],
                                   price=30000,
                                   host=db_host,
                                   lat=db_lat,
                                   lng=db_lng,
                                   )

        print('Room DB 저장 성공')

        count = 0
        for db_room_photo_url in db_room_photo_urls:
            count += 1
            img_data = requests.get(db_room_photo_url).content
            ext = imghdr.what('', h=img_data)
            db_room_photo = SimpleUploadedFile(f'{room_id}-{count}.{ext}', img_data)
            RoomPhoto.objects.create(room=room, photo=db_room_photo)
            # img_url = urllib.request.urlretrieve(db_room_photo, f'{room_id}-{count}.jpg')

        print('RoomPhoto DB 저장 성공')

        time.sleep(5)


# 브라우저 종료
browser.quit()

