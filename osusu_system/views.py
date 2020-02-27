from rest_framework.authentication import SessionAuthentication
from .models import Tricycle, Garage, Payment, Claim, PartClaim, Part
from rest_framework import viewsets, filters
from .serializers import (
    TricycleReadSerializer,
    TricycleWriteSerializer,
    GarageSerializer,
    PaymentReadSerializer,
    PaymentWriteSerializer,
    ClaimReadSerializer,
    ClaimWriteSerializer,
    PartClaimWriteSerializer,
    PartClaimReadSerializer,
    PartSerializer,
)
from django_filters import rest_framework as df_filters


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class TricycleFilter(df_filters.FilterSet):
    full_name = df_filters.CharFilter(field_name="full_name", lookup_expr="icontains")

    class Meta:
        model = Tricycle
        fields = ["full_name"]


# ViewSets define the view behavior.
class TricycleViewSet(viewsets.ModelViewSet):
    queryset = Tricycle.objects.all()
    serializer_class = TricycleReadSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    filter_backends = [df_filters.DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = "__all__"
    filterset_class = TricycleFilter

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return TricycleReadSerializer
        return TricycleWriteSerializer


class GarageViewSet(viewsets.ModelViewSet):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    authentication_classes = [CsrfExemptSessionAuthentication]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return PaymentReadSerializer
        return PaymentWriteSerializer


class ClaimsViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    authentication_classes = [CsrfExemptSessionAuthentication]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return ClaimReadSerializer
        return ClaimWriteSerializer


class PartClaimViewSet(viewsets.ModelViewSet):
    queryset = PartClaim.objects.all()
    authentication_classes = [CsrfExemptSessionAuthentication]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return PartClaimReadSerializer
        return PartClaimWriteSerializer


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"
