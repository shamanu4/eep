from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from base.models import User, Category, ObjectPurpose, Institution, Building, MeterType, Meter, MeterData, Rate, Receipt, Component, ComponentType, Feature, FeatureType


class InstitutionAdmin(GuardedModelAdmin):
    pass
admin.site.register(Institution, InstitutionAdmin)


class BuildingAdmin(GuardedModelAdmin):
    pass
admin.site.register(Building, BuildingAdmin)


class UserAdmin(GuardedModelAdmin):
    pass
admin.site.register(User, UserAdmin)

admin.site.register(Category)
admin.site.register(ObjectPurpose)
admin.site.register(MeterType)
admin.site.register(Meter)
admin.site.register(MeterData)
admin.site.register(Rate)
admin.site.register(Receipt)
admin.site.register(Component)
admin.site.register(ComponentType)
admin.site.register(Feature)
admin.site.register(FeatureType)