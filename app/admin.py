from django.contrib import admin
from app.models import InstaKiloGramUser, Post, Comment


class InstaKiloGramUserAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['username', 'password', 'slug','avatar', 'about_me']}),
                 ('Info', {'fields': ['last_login', 'date_joined']})]


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'author', 'created', 'edited')
    list_filter = ('created', 'edited')
    search_fields = ['content']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'content', 'author', 'created')
    list_filter = ['created']
    search_fields = ['content']


admin.site.register(InstaKiloGramUser, InstaKiloGramUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
