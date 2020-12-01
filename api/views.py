from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from api.documentation.documentclassification import *
from api.berts.USE import *

from core.models import *
from core.utils import generate_random_string

from bs4 import BeautifulSoup
import json
import yaml


class BaseViewMixin:
    @staticmethod
    def ok_response(message='', results=None, status=200):
        if results is None:
            results = {}
        return Response({
            'success': True,
            'message': message,
            'results': results,
        }, status=status)

    @staticmethod
    def err_response(message='', results=None, code='NOPE', status=400):
        if results is None:
            results = {}
        return Response({
            'success': False,
            'code': code,
            'message': message,
            'results': results,
        }, status=status)

# Create your views here.


class BaseAPIView(BaseViewMixin, GenericAPIView):
    pass

# 127.0.0.1:8000/api/tag/?text="친구에게 돈을 빌려줬는데 갚지 않아요"


class BaseModelViewSet(BaseViewMixin, ModelViewSet):
    allow_any_actions = []


class RecommendTagView(BaseAPIView):
    def get(self, request, *args, **kwargs):
        text = request.GET.get('text')
        results = get_tag(text)
        return Response(results)


class TagView(BaseAPIView):
    def get(self, request, *args, **kwargs):
        result = []
        tags = Tag.objects.all()
        for tag in tags:
            result.append(tag.name)
        return Response(result)


def get_invitation_code():
    code = generate_random_string(5)
    code = f'barlaw{code}'
    while 1:
        if Event.objects.filter(code=code).exists():
            code = generate_random_string(5)
            code = f'barlaw{code}'
        else:
            break
    return code


def send_msg(contact, code):
    send_url = 'https://apis.aligo.in/send/'
    sms_data = {
        'key': '0pjgxbzo98ga7rzxk5o7qgc9l6uwq3o7',  # api key
        'userid': 'aisoftkorea',  # 알리고 사이트 아이디
        'sender': '010-3565-7852',  # 발신번호
        # f'{contact}',  # 수신번호 (,활용하여 1000명까지 추가 가능)
        'receiver': f'{contact}',
        # 문자 내용
        'msg': f'바로: 바로 보는 법률 서비스\n\n안녕하세요. 인공지능 법률상담 플랫폼 바로(BarLaw)입니다. 변호사 답변 확인을 위한 코드를 보내드립니다.\n\n쿠폰번호: {code}',
        'msg_type': 'LMS',  # 메세지 타입 (SMS, LMS)
        # 'testmode_yn': 'y'  # 테스트모드 적용 여부 Y/N
    }
    requests.post(send_url, data=sms_data)


class QuestionView(BaseAPIView):
    def post(self, request, *args, **kwargs):
        try:
            title = request.data.get('title')
            description = request.data.get('description')
            question = Question.objects.create(
                title=title, description=description)
            tags = request.data.get('tags')
            for tag in tags:
                tag_obj = Tag.objects.get(name=tag)
                if tag_obj:
                    question.tags.add(tag_obj)
            question.save()

            if request.data.get('phonenumber'):
                phonenumber = request.data.get('phonenumber')
                code = get_invitation_code()
                Event.objects.create(
                    question=question, phonenumber=phonenumber, code=code, answer='')
                send_msg(phonenumber, code)

            if len(tags) == 1:
                results_dict = recommend(title, description, tags[0])
            elif len(tags) == 2:
                results_dict = recommend(title, description, tags[0], tags[1])
            elif len(tags) == 3:
                results_dict = recommend(
                    title, description, tags[0], tags[1], tags[2])

            results_dict = json.dumps(results_dict)
            results_dict = results_dict.encode("utf-8")
            results_dict = yaml.safe_load(results_dict)

            Answer.objects.create(question=question, answer=results_dict)

            return Response({'id': question.id})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        try:
            q_id = request.GET.get('id')
            question = Question.objects.get(id=q_id)
            answers = Answer.objects.get(question=question)
            response = {'question': {
                'id': question.id,
                'title': question.title,
                'content': question.description
            }, 'answers': answers.answer
            }
            event = Event.objects.filter(question=question).count()
            if event:
                response['code'] = Event.objects.get(question=question).code
            else:
                response['code'] = ''
            return Response(response)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class EventView(BaseAPIView):
    def get(self, request, *args, **kwargs):
        try:
            code = request.GET.get('code')
            event = Event.objects.get(code=code)
            question = event.question
            answers = Answer.objects.get(question=question)
            response = {'question': {
                'id': question.id,
                'title': question.title,
                'content': question.description
            }, 'answers': answers.answer,
                'code': code
            }
            if event.answer:
                response['answer'] = event.answer
            else:
                response['answer'] = ''
            return Response(response)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class EventCompView(BaseAPIView):
    def post(self, request, *args, **kwargs):
        try:
            name = request.data.get('name')
            manager = request.data.get('manager')
            comp_number = request.data.get('number')
            email = request.data.get('email')
            EventComp.objects.create(
                name=name, manager=manager, comp_number=comp_number, email=email)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PanryeDataView(BaseAPIView):
    def get(self, request, *args, **kwargs):
        try:
            code = request.GET.get('code')
            if PanryeData.objects.filter(code=code).count():
                result = PanryeData.objects.get(code=code).jurisdiction
                return Response({'results': result})
            response = requests.get(f'https://casenote.kr/search/?q={code}')
            soup = BeautifulSoup(response.text, 'html.parser')
            if(soup.select('.panel-heading')):
                result = ''
                texts = soup.select('.panel > .issue > p')
                for text in texts:
                    result += text.text
                PanryeData.objects.create(code=code, jurisdiction=result)
                return Response({'results': result})
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AIAnswerView(BaseAPIView):
    def post(self, request, *args, **kwargs):
        try:
            q_id = request.data.get('id')
            question = Question.objects.get(id=q_id)
            answer = request.data.get('answer')
            title = request.data.get('title')
            content = request.data.get('content')
            satisfaction = request.data.get('satisfaction')
            AIAnswer.objects.create(
                question=question, answer=answer, title=title, content=content, satisfaction=satisfaction)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
