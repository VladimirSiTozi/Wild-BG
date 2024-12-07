from django.urls import path, include

from wildBg.post import views
from wildBg.post.views import like_post_func

urlpatterns = [
    path('add/', views.PostAddView.as_view(), name='post-add'),
    path('<int:pk>/', include([
        path('', views.PostDetailView.as_view(), name='post-detail'),
        path('edit/', views.PostEditView.as_view(), name='post-edit'),
        path('delete/', views.delete_post, name='delete-edit'),
        path('like/', like_post_func, name='post-like'),
    ])),
]
