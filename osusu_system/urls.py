from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from .models import Tricycle
from rest_framework.authentication import SessionAuthentication
from . import views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"tricycles", views.TricycleViewSet)
router.register(r"garages", views.GarageViewSet)
router.register(r"payments", views.PaymentViewSet)
router.register(r"claims", views.ClaimsViewSet)
router.register(r"partclaims", views.PartClaimViewSet)
router.register(r"parts", views.PartViewSet)


urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
