from django.conf.urls import include, url
from django.contrib import admin
from msgapi.views import PostMessageView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', PostMessageView.as_view(), name="post-message"),
]
