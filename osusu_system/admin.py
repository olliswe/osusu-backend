from django.contrib import admin
from .models import Claim, Garage, Tricycle, Fund, Part, PartClaim, Payment


admin.site.register(Claim)
admin.site.register(Garage)
admin.site.register(Tricycle)
admin.site.register(Fund)
admin.site.register(Part)
admin.site.register(PartClaim)
admin.site.register(Payment)
