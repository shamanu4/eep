from django.contrib import admin
from base.models import User, Institution, Building, MeterType, Meter, MeterData


admin.site.register(User)
admin.site.register(Institution)
admin.site.register(Building)
admin.site.register(MeterType)
admin.site.register(Meter)
admin.site.register(MeterData)
