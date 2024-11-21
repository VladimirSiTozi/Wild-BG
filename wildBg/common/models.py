from django.contrib.auth import get_user_model
from django.db import models

from wildBg.post.models import Post


UserModel = get_user_model()


class PostLike(models.Model):
    to_post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
