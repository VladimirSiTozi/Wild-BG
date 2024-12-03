from django.urls import path, include

from wildBg.post import views
from wildBg.post.views import like_post_func

urlpatterns = [
    path('<int:pk>/', include([
        path('', views.PostDetailView.as_view(), name='post-detail'),
        path('like/', like_post_func, name='post-like'),
    ])),
]
