from celery import Celery

from core.utils import generate_random_string
from core.models import *


import requests
import json

app = Celery('tasks', broker='pyamqp://guest@localhost//')

def get_invitation_code():
    code = generate_random_string(5)
    code = f'barlaw{code}'
    if Event.objects.filter(code=code).exists():
        code = f'barlaw{code}'
    return code

def send_msg(contact, code):
    send_url = 'https://apis.aligo.in/send/'
    code = get_invitation_code()
    sms_data = {
        'key': '0pjgxbzo98ga7rzxk5o7qgc9l6uwq3o7',  # api key
        'userid': 'aisoftkorea',  # 알리고 사이트 아이디
        'sender': '010-3565-7852',  # 발신번호
        # f'{contact}',  # 수신번호 (,활용하여 1000명까지 추가 가능)
        'receiver': '010-2801-0792',
        'msg': f'바로: 바로 보는 법률 서비스\n\n쿠폰번호: {code}',  # 문자 내용
        'msg_type': 'LMS',  # 메세지 타입 (SMS, LMS)
        # f'쿠폰번호: {code}\n\n발급 받으신 쿠폰은 12월 학쫑 자사몰 오픈 이후 사용하실 수 있습니다.\n자사몰 오픈 일정은 추후 다시 한 번 안내드리도록 하겠습니다.\n\n궁금하신 사항은 카카오톡 플러스친구 "학쫑"으로 문의주시기 바랍니다.',
        # 'testmode_yn': 'y'  # 테스트모드 적용 여부 Y/N
    }
    requests.post(send_url, data=sms_data)
