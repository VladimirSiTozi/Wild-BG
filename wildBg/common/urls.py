from django.urls import path

from wildBg.common import views
from wildBg.post.views import add_comment

urlpatterns = [
    # path('', views.test_home, name='test-home')
    path('', views.HomePageView.as_view(), name='home'),
    path('about-us/', views.AboutUsPageView.as_view(), name='about-us'),
    path('landmark-home/', views.LandmarksHomePageView.as_view(), name='landmark-home'),
    path('comment/<int:pk>/', add_comment, name='post-comment'),
]
