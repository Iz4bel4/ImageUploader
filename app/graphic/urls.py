"""
URL mappings for the graphic app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from graphic import views


router = DefaultRouter()
router.register("graphics", views.GraphicViewSet)

app_name = "graphic"

urlpatterns = [
    path("", include(router.urls)),
]
