from rest_framework import serializers
from .models import Tricycle, Garage, Payment, Claim

# Serializers define the API representation.
class TricycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tricycle
        fields = "__all__"


class GarageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garage
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = "__all__"
