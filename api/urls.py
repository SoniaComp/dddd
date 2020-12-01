from rest_framework import routers
from django.urls import path, include
from api.views import *

# router = routers.SimpleRouter()

urlpatterns = [
    # path('', include(router.urls)),
    path('tag/', RecommendTagView.as_view(), name='tag'),
    path('tags/', TagView.as_view(), name='tag_list'),
    path('question/', QuestionView.as_view(), name='question'),
    path('event/', EventView.as_view(), name='event'),
    path('event/comp/', EventCompView.as_view(), name='event_comp'),
    path('panrye/', PanryeDataView.as_view(), name='panrye'),
    path('ai/', AIAnswerView.as_view(), name='ai_train')
]
