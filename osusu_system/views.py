from rest_framework.authentication import SessionAuthentication
from .models import Tricycle, Garage, Payment, Claim, PartClaim, Part
from rest_framework import viewsets
from .serializers import (
    TricycleReadSerializer,
    TricycleWriteSerializer,
    GarageSerializer,
    PaymentSerializer,
    ClaimReadSerializer,
    ClaimWriteSerializer,
    PartClaimWriteSerializer,
    PartClaimReadSerializer,
    PartSerializer,
)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


# ViewSets define the view behavior.
class TricycleViewSet(viewsets.ModelViewSet):
    queryset = Tricycle.objects.all()
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return TricycleReadSerializer
        return TricycleWriteSerializer


class GarageViewSet(viewsets.ModelViewSet):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    filterset_fields = "__all__"


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    filterset_fields = "__all__"


class ClaimsViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    authentication_classes = [CsrfExemptSessionAuthentication]
    filterset_fields = "__all__"

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return ClaimReadSerializer
        return ClaimWriteSerializer


class PartClaimViewSet(viewsets.ModelViewSet):
    queryset = PartClaim.objects.all()
    authentication_classes = [CsrfExemptSessionAuthentication]
    filterset_fields = "__all__"

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return PartClaimReadSerializer
        return PartClaimWriteSerializer


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    filterset_fields = "__all__"
