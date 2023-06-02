"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from website import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.Index.as_view(), name="index"),
    path("gallery/", views.Gallery.as_view(), name="gallery"),
    path(
        "gallery/<int:page>",
        views.Gallery.infinite_scroll,
    ),
    path("game/", views.NewGame.as_view(), name="newgame"),
    path("player/", views.NewPlayer.as_view(), name="newplayer"),
    path("player/<int:id>", views.PlayerView.as_view(), name="player"),
    path("scores/", views.Scores.as_view(), name="scores"),
    path("game-results/<int:id>", views.GameResults.as_view(), name="gameresults"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
