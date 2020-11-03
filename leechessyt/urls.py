"""carpinteriaramirez URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from sistema.views import *
from django.conf.urls import url, include
from sistema import views
from rest_framework.routers import DefaultRouter
from django.contrib.staticfiles.urls import static
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'responses', views.ResponseViewSet)
router.register(r'users', views.UserViewSet)
urlpatterns = [
    url(r'^api/rest/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/rest/', include(router.urls)),
    url(r'^backend/', admin.site.urls),
    url(r'^api/login/$', views.Login.as_view()),
    url(r'^api/newpost/$', views.post),
    url(r'^api/allposts/$', views.allposts),
    #url(r'^api/allcomments/$', views.allcomments),
    #url(r'^api/allservices/$', views.services),
url(r'^api/rest/posts/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/image/$', views.image),
url(r'^api/rest/posts/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/addimages/$', views.addimages),
    url(r'^api/rest/posts/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/data/$', views.singlepost),
    url(r'^api/home/$', views.home),
    url(r'^api/about/$', views.about),
    url(r'^api/contact/$', views.contact),
    url(r'^api/logout/$', views.LogoutView.as_view()),
    #url(r'^api/user/', views.CustomRegisterView.as_view()),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)