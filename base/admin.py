from django.contrib import admin
from base.models import User, Category, ObjectPurpose, Institution, Building, MeterType, Meter, MeterData


admin.site.register(User)
admin.site.register(Category)
admin.site.register(ObjectPurpose)
admin.site.register(Institution)
admin.site.register(Building)
admin.site.register(MeterType)
admin.site.register(Meter)
admin.site.register(MeterData)
