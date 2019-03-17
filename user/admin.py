from django.contrib import admin
from user.models import User, Article, Review

class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'nicename', 'register_time','article_number')

class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'content', 'pub_data','pub_author', 'looks','author', 'review_number')

class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id','article', 'comment', 'comment_uesr',  'review_data')

admin.site.register(User, UsersAdmin)
admin.site.register(Article, ArticlesAdmin)
admin.site.register(Review, ReviewsAdmin)
