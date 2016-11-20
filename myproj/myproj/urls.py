from django.conf.urls import include, url
from django.contrib import admin
from msgapi.views import PostMessageView
from msgapi.api import PostMessageAPI, MessageStatusAPI, DummyUserCallbackService

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', PostMessageView.as_view(), name="post-message"),
    url(r'^api/post-message/$', PostMessageAPI.as_view(), name="post-message-api"),
    url(r'^api/get-message-status/$', MessageStatusAPI.as_view(), name="message-status-api"),
    url(r'^api/user-callback-service/$', DummyUserCallbackService.as_view(), name="user-callback-service"),
]
