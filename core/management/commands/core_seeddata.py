import re
from random import random
from math import floor
from django.db import IntegrityError, transaction
from django.core.management import BaseCommand, call_command
from django.utils.timezone import localtime

from core.models import *

class Command(BaseCommand):
    def seed_tag(self):
        for tag in ['성범죄', '임대차', '계약일반', '손해배상', '노동/인사', '지식재산권', '회생/파산', 'IT/테크', '기업일반', '금융', '행정', '등기/등록', '매매', '세금', '개인정보', '문서위조', '약식명령/즉결심판']:
            Tag.objects.create(name=tag)
   
    def handle(self, **options):   
        self.seed_tag()
