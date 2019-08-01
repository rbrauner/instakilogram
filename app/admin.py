from django.contrib import admin
from app.models import TwitterUser, Tweet, Comment


class TwitterUserAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['username', 'password', 'slug','avatar', 'about_me']}),
                 ('Info', {'fields': ['last_login', 'date_joined']})]


class TweetAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'author', 'created', 'edited')
    list_filter = ('created', 'edited')
    search_fields = ['content']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'tweet', 'content', 'author', 'created')
    list_filter = ['created']
    search_fields = ['content']


admin.site.register(TwitterUser, TwitterUserAdmin)
admin.site.register(Tweet, TweetAdmin)
admin.site.register(Comment, CommentAdmin)
