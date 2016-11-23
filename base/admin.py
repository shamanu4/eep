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


class MeterDataInline(admin.TabularInline):
    model = MeterData
    extra = 10
    exclude = ['manager']


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.manager = request.user
            instance.save()
        formset.save_m2m()
    inlines = [MeterDataInline]


admin.site.register(ObjectPurpose)


@admin.register(MeterData)
class MeterDataAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.manager = request.user
        obj.save()

    exclude = ['manager']

admin.site.register(Rate)
admin.site.register(Receipt)
admin.site.register(Feature)
admin.site.register(Component)
