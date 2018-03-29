from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^category$', views.category, name='category'),
    url(r'^search$', views.MySearchView(), name='haystack_search'),
    url(r'^editor$', views.editor, name='editor')
]