from rest_framework.authentication import SessionAuthentication
from .models import Tricycle, Garage, Payment
from rest_framework import viewsets
from .serializers import TricycleSerializer, GarageSerializer, PaymentSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


# ViewSets define the view behavior.
class TricycleViewset(viewsets.ModelViewSet):
    queryset = Tricycle.objects.all()
    serializer_class = TricycleSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]


class GarageViewset(viewsets.ModelViewSet):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]


class PaymentViewset(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
