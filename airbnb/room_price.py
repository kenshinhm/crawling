# selenium 임포트
import random
import django
import os
from django.core.files.uploadedfile import SimpleUploadedFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from airbnb.rooms.models import Room

city_list = ['서울특별시',
             '부산광역시',
             '대전광역시',
             '인천광역시',
             '거제시',
             '광주광역시',
             '속초시',
             '수원시',
             '울산광역시']

city = '울산광역시'
min_price = 10
max_price = 60

city_rooms = Room.objects.filter(city=city)

for room in city_rooms:
    room.price = random.randrange(min_price, max_price)*1000
    room.save()

print('가격 Update 완료: {}'.format(city))

