from rest_framework.authentication import SessionAuthentication
from .models import Tricycle, Garage, Payment, Claim, PartClaim, Part, Fund
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
    FundReadSerializer,
    FundWriteSerializer,
)
from django_filters import rest_framework as df_filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
import rest_framework_filters as rf_filters
from rest_framework_filters.backends import RestFrameworkFilterBackend


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


class GarageFilter(df_filters.FilterSet):
    name = df_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Garage
        fields = ["name"]


class GarageViewSet(viewsets.ModelViewSet):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    filter_backends = [df_filters.DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = "__all__"
    filterset_class = GarageFilter


class PaymentFilter(df_filters.FilterSet):
    tricycle__full_name = df_filters.CharFilter(
        field_name="tricycle__full_name", lookup_expr="icontains"
    )

    tricycle = df_filters.CharFilter(field_name="tricycle__id", lookup_expr="exact")

    class Meta:
        model = Payment
        fields = ["tricycle__full_name", "tricycle"]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    authentication_classes = [CsrfExemptSessionAuthentication]
    filter_backends = [df_filters.DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = "__all__"
    filterset_class = PaymentFilter

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return PaymentReadSerializer
        return PaymentWriteSerializer


class ClaimTricycleFilter(rf_filters.FilterSet):
    class Meta:
        model = Tricycle
        fields = {"full_name": ["icontains"]}


class ClaimGarageFilter(rf_filters.FilterSet):
    class Meta:
        model = Garage
        fields = {"name": ["icontains"]}


class ClaimFilter(rf_filters.FilterSet):
    tricycle = rf_filters.RelatedFilter(
        ClaimTricycleFilter, field_name="tricycle", queryset=Tricycle.objects.all()
    )
    garage = rf_filters.RelatedFilter(
        ClaimGarageFilter, field_name="garage", queryset=Garage.objects.all()
    )

    class Meta:
        model = Claim
        fields = ("status",)


class ClaimsViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    authentication_classes = [CsrfExemptSessionAuthentication]
    filter_backends = [RestFrameworkFilterBackend, filters.OrderingFilter]
    ordering_fields = "__all__"
    filter_class = ClaimFilter

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return ClaimReadSerializer
        return ClaimWriteSerializer


class PartClaimViewSet(viewsets.ModelViewSet):
    queryset = PartClaim.objects.all()
    authentication_classes = [CsrfExemptSessionAuthentication]
    filter_backends = [df_filters.DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = "__all__"
    filterset_fields = "__all__"

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return PartClaimReadSerializer
        return PartClaimWriteSerializer


class FundViewSet(viewsets.ModelViewSet):
    queryset = Fund.objects.all()
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return FundReadSerializer
        return FundWriteSerializer


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"


@api_view(["GET"])
def get_fund_data(self):
    fund = Fund.objects.first()
    return Response(
        {
            "actual_amount": fund.actual_amount,
            "required_amount": fund.required_amount,
            "total_available_amount_month": fund.total_available_amount_month,
            "remaining_available_amount_month": fund.remaining_available_amount_month,
        }
    )


@api_view(["GET"])
def get_claims_data(self):
    open_claims = 0
    approved_claims = 0
    for claim in Claim.objects.filter(status="Open"):
        open_claims += claim.total_value
    for claim in Claim.objects.filter(status="Approved"):
        approved_claims += claim.total_value
    return Response({"open_claims": open_claims, "approved_claims": approved_claims})
