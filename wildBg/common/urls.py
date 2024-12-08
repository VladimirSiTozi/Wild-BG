from django.urls import path

from wildBg.common import views
from wildBg.landmark.views import share_landmark_functionality
from wildBg.post.views import add_comment, share_post_functionality

urlpatterns = [
    # path('', views.test_home, name='test-home')
    path('', views.HomePageView.as_view(), name='home'),
    path('about-us/', views.AboutUsPageView.as_view(), name='about-us'),
    path('landmark-home/', views.LandmarksHomePageView.as_view(), name='landmark-home'),
    path('comment/<int:pk>/', add_comment, name='post-comment'),
    path('share/<int:pk>/', share_post_functionality, name='share-post'),
    path('share-ladnmarj/<int:pk>/', share_landmark_functionality, name='share-landmark'),
]
