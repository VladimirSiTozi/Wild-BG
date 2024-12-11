from django.contrib import admin
from .models import Post, PostComment, ReplyPostComment, PostLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author_email', 'location', 'created_at')
    list_display_links = ('author_email',)
    search_fields = ('author__email', 'description', 'location__name')
    list_filter = ('created_at', 'location')
    readonly_fields = ('created_at',)
    filter_horizontal = ('tagged_people',)
    fieldsets = (
        ('Post Details', {
            'fields': ('author', 'location', 'post_image', 'description', 'created_at')
        }),
        ('Tagged Users', {
            'fields': ('tagged_people',)
        }),
    )

    def author_email(self, obj):
        return obj.author.email
    author_email.short_description = 'Author Email'

    def location_name(self, obj):
        return obj.location.name if obj.location else "No Location"
    location_name.short_description = 'Location'


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author_email', 'post_id', 'created_at')
    list_display_links = ('author_email',)
    search_fields = ('author__email', 'content', 'post__description')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Comment Details', {
            'fields': ('post', 'author', 'content', 'created_at')
        }),
    )

    def post_id(self, obj):
        return obj.post.id
    post_id.short_description = 'Post ID'

    def author_email(self, obj):
        return obj.author.email
    author_email.short_description = 'Author Email'


@admin.register(ReplyPostComment)
class ReplyPostCommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author_email', 'comment_id', 'comment_post_id', 'created_at')
    list_display_links = ('author_email',)
    search_fields = ('author__email', 'content', 'comment__content')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Reply Details', {
            'fields': ('comment', 'author', 'content', 'created_at')
        }),
    )

    def comment_id(self, obj):
        return obj.comment.id
    comment_id.short_description = 'Comment ID'

    def author_email(self, obj):
        return obj.author.email
    author_email.short_description = 'Author Email'

    def comment_post_id(self, obj):
        """Returns the ID of the post related to the comment."""
        if obj.comment and obj.comment.post:
            return obj.comment.post.id
        return None  # Handles cases where post or comment might not exist
    comment_post_id.short_description = 'Post ID'


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('pk',  'user_email', 'post_id',)
    list_display_links = ('user_email',)
    search_fields = ('to_post__description', 'user__email')
    fieldsets = (
        ('Like Details', {
            'fields': ('to_post', 'user')
        }),
    )

    def post_id(self, obj):
        return obj.to_post.id
    post_id.short_description = 'Post ID'

    def user_email(self, obj):
        return f'{obj.user.email}'
    user_email.short_description = 'User Email'
