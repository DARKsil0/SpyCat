from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpyCatViewSet, MissionViewSet, TargetViewSet

router = DefaultRouter()
router.register(r"cats", SpyCatViewSet, basename="cat")
router.register(r"missions", MissionViewSet, basename="mission")
router.register(r"targets", TargetViewSet, basename="target")

urlpatterns = [
    path("", include(router.urls)),

]