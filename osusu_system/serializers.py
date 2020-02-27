from rest_framework import serializers
from .models import Tricycle, Garage, Payment, Claim, PartClaim, Part

# Serializers define the API representation.
class TricycleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tricycle
        fields = "__all__"


class TricycleReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tricycle
        fields = [field.name for field in model._meta.fields]
        fields.append("waiting_period")
        fields.append("number_payments_made")
        fields.append("total_value_of_payments_made")
        fields.append("payments_up_to_date")
        fields.append("outstanding_payments")
        fields.append("tot_claims")
        fields.append("total_value_claims")
        fields.append("total_num_approved_claims")
        fields.append("total_val_approved_claims")
        fields.append("tot_claims_6_months")
        fields.append("total_value_claims_6_months")
        fields.append("total_num_approved_claims_6_months")
        fields.append("total_val_approved_claims_6_months")


class GarageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garage
        fields = [field.name for field in model._meta.fields]
        fields.append("total_no_claims")
        fields.append("total_val_claims")
        fields.append("total_num_approved_claims")
        fields.append("total_val_approved_claims")
        fields.append("total_num_open_claims")
        fields.append("total_val_open_claims")
        fields.append("total_num_approved_not_paid_claims")
        fields.append("total_val_approved_not_paid_claims")


class PaymentReadSerializer(serializers.ModelSerializer):
    tricycle = TricycleReadSerializer(many=False, read_only=True)

    class Meta:
        model = Payment
        fields = [field.name for field in model._meta.fields]


class PaymentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = [field.name for field in model._meta.fields]


class PartClaimWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartClaim
        fields = "__all__"


class PartClaimReadSerializer(serializers.ModelSerializer):
    part = PartSerializer(many=False)

    class Meta:
        model = PartClaim
        fields = [field.name for field in model._meta.fields]
        fields.append("value")


class ClaimReadSerializer(serializers.ModelSerializer):
    tricycle = TricycleReadSerializer(many=False, read_only=True)
    garage = GarageSerializer(many=False, read_only=True)
    partclaims = PartClaimReadSerializer(many=True, source="partclaim_set")

    class Meta:
        model = Claim
        fields = [field.name for field in model._meta.fields]
        fields.append("id")
        fields.append("total_value")
        fields.append("partclaims")


class ClaimWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = "__all__"
