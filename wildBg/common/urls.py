from django.urls import path

from wildBg.common import views

urlpatterns = [
    path('', views.test_home, name='test-home')
]