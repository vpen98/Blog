from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url
from user.views import login, register,homepage,postarticle,showpage,article_review


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', homepage, name="index"),
    url(r'^login/$',login, name="login"),
    url(r'^login/register/$', register, name="register"),
    url(r'^postarticle/$', postarticle, name='postarticle'),
    url(r'^(?P<id>[0-9]+)/$', showpage, name="showpage"),
    url(r'^(?P<id>[0-9]+)/(?P<pk>[0-9]+)/$', article_review, name="article_review"),
]

