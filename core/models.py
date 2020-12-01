# from django.db import models
from django.db import models
from django.conf import settings
from django.utils.timezone import now
import requests

from datetime import timezone
import time

# # Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=20, blank=True,
                            default='', verbose_name='태그')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'
        verbose_name = '태그'
        verbose_name_plural = '태그'


class Question(models.Model):
    title = models.TextField(verbose_name='제목', null=True, blank=True)
    description = models.TextField(verbose_name='설명', null=True, blank=True,)
    tags = models.ManyToManyField('core.Tag', blank=True, verbose_name='태그')
    inserted_time = models.DateTimeField(auto_now_add=True, verbose_name='등록 시간')
    updated_time = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return f'{self.title} {self.inserted_time.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%y/%m/%d %H:%M")}'

    class Meta:
        db_table = 'questions'
        verbose_name = '변호사_질문'
        verbose_name_plural = '변호사_질문'


class Answer(models.Model):
    answer = models.JSONField(default=list)
    question = models.ForeignKey('core.Question', related_name='law_question',
                                 on_delete=models.CASCADE, null=True, verbose_name='변호사_질문')
    inserted_time = models.DateTimeField(auto_now_add=True, verbose_name='등록 시간')
    updated_time = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return f'{self.question.title} {self.inserted_time.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%y/%m/%d %H:%M")}'

    class Meta:
        db_table = 'answers'
        verbose_name = 'AI_응답'
        verbose_name_plural = 'AI_응답'


class Event(models.Model):
    answer = models.TextField(blank=True, default='', verbose_name='변호사_응답')
    question = models.ForeignKey('core.Question', related_name='event_question',
                                 on_delete=models.CASCADE, null=True, verbose_name='변호사_질문')
    phonenumber = models.CharField(
        max_length=11, blank=True, null=True, default='', verbose_name='연락처')
    code = models.CharField(max_length=12, null=True,
                            blank=True, verbose_name='코드')
    inserted_time = models.DateTimeField(auto_now_add=True, verbose_name='등록 시간')
    updated_time = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        if self.answer:
            return f'완료 ---------- {self.phonenumber} {self.inserted_time.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%y/%m/%d %H:%M")}'
        else:
            return f'응답 대기중 ----- {self.phonenumber} {self.inserted_time.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%y/%m/%d %H:%M")}'

    class Meta:
        db_table = 'events'
        verbose_name = '이벤트'
        verbose_name_plural = '이벤트'


class EventComp(models.Model):
    name = models.CharField(max_length=30, null=True,
                            blank=True, verbose_name='기업명')
    manager = models.CharField(max_length=30, null=True,
                            blank=True, verbose_name='담당자')
    comp_number = models.CharField(max_length=15, null=True,
                                   blank=True, verbose_name='사업자등록번호')
    email = models.CharField(max_length=100, unique=True, verbose_name='이메일')
    inserted_time = models.DateTimeField(auto_now_add=True, verbose_name='등록 시간')
    updated_time = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return f'{self.name} : {self.email}'

    class Meta:
        db_table = 'event_comps'
        verbose_name = '이벤트:사전예약등록기업'
        verbose_name_plural = '이벤트:사전예약등록기업'


class AIAnswer(models.Model):
    answer = models.TextField(verbose_name='AI검색_결과', default='')
    title = models.TextField(verbose_name='AI검색_제목', null=True, blank=True)
    content = models.TextField(verbose_name='AI검색_설명', null=True, blank=True,)
    question = models.ForeignKey('core.Question', related_name='ai_question',
                                 on_delete=models.CASCADE, null=True, verbose_name='AI검색_질문')
    satisfaction = models.BooleanField(
        null=True, blank=True, verbose_name='AI응답_만족')
    inserted_time = models.DateTimeField(auto_now_add=True, verbose_name='등록 시간')
    updated_time = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return f'{self.question.title} : {self.satisfaction}'

    class Meta:
        db_table = 'ai_answers'
        verbose_name = 'AI검색_만족도'
        verbose_name_plural = 'AI검색_만족도'


class PanryeData(models.Model):
    code = models.CharField(max_length=50, null=True,
                            blank=True, verbose_name='판례코드')
    jurisdiction = models.TextField(verbose_name='판시사항', null=True, blank=True)

    def __str__(self):
        return f'{self.code}'

    class Meta:
        db_table = 'panryes'
        verbose_name = '판시사항'
        verbose_name_plural = '판시사항'
