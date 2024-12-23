from django.urls import path

from wildBg.common import views
from wildBg.landmark.views import share_landmark_functionality
from wildBg.post.views import add_comment, share_post_functionality, add_reply

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about-us/', views.AboutUsPageView.as_view(), name='about-us'),
    path('landmark-home/', views.LandmarksHomePageView.as_view(), name='landmark-home'),
    path('comment/<int:pk>/', add_comment, name='post-comment'),
    path('reply-comment/<int:pk>', add_reply, name='add-reply'),
    path('share/<int:pk>/', share_post_functionality, name='share-post'),
    path('share-ladnmarj/<int:pk>/', share_landmark_functionality, name='share-landmark'),
    path('api/landmarks/', views.LandmarkListAPIView.as_view(), name='api-landmarks-list'),
]
