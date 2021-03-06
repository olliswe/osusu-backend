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
router.register(r"funds", views.FundViewSet)


urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^rest-auth/", include("rest_auth.urls")),
    url(r"^fund-data/", views.get_fund_data),
    url(r"^claims-data/", views.get_claims_data),
]
