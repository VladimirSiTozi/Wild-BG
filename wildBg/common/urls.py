from django.urls import path

from wildBg.common import views
from wildBg.post.views import toggle_like, add_comment

urlpatterns = [
    # path('', views.test_home, name='test-home')
    path('', views.HomePageView.as_view(), name='home'),
    path('like/<int:pk>/', toggle_like, name='post-like'),
    path('comment/<int:pk>/', add_comment, name='post-comment'),
]
