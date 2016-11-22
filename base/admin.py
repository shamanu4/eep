from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from base.models import User, Category, ObjectPurpose, Institution, Building, MeterType, Meter, MeterData, Rate, Receipt, Component, ComponentType, Feature, FeatureType


@admin.register(Building)
class BuildingAdmin(GuardedModelAdmin):
    pass


class BuildingInline(admin.TabularInline):
    model = Building
    extra = 10


@admin.register(Institution)
class InstitutionAdmin(GuardedModelAdmin):
    inlines = [BuildingInline, ]


@admin.register(User)
class UserAdmin(GuardedModelAdmin):
    pass


class ObjectPurposeInline(admin.TabularInline):
    model = ObjectPurpose
    extra = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ObjectPurposeInline]


class MeterInline(admin.TabularInline):
    model = Meter
    extra = 10


@admin.register(MeterType)
class MeterTypeAdmin(admin.ModelAdmin):
    inlines = [MeterInline]


class ComponentInline(admin.TabularInline):
    model = Component
    extra = 10


@admin.register(ComponentType)
class ComponentTypeAdmin(admin.ModelAdmin):
    inlines = [ComponentInline]


class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 10


@admin.register(FeatureType)
class FeatureTypeAdmin(admin.ModelAdmin):
    inlines = [FeatureInline]


admin.site.register(ObjectPurpose)
admin.site.register(MeterData)
admin.site.register(Rate)
admin.site.register(Receipt)
admin.site.register(Feature)
admin.site.register(Component)
admin.site.register(Meter)
