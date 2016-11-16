from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.datetime_safe import date
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser, MPTTModel):
    email = models.EmailField('Електронна пошта', unique=True)
    post = models.CharField('Посада', max_length=250)
    last_name = models.CharField('Прізвище', max_length=50)
    first_name = models.CharField("Ім'я", max_length=50)
    middle_name = models.CharField('По-батькові', max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, verbose_name='Керівник')
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return "%s %s %s" % (self.last_name, self.first_name, self.middle_name)

    def get_short_name(self):
        return self.first_name


class Category(models.Model):
    name = models.CharField('Назва категорії', max_length=100)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name


class ObjectPurpose(models.Model):
    name = models.CharField("Призначення об'єкту", max_length=100)
    category = models.ForeignKey(Category, verbose_name='Категорія')

    class Meta:
        verbose_name = "Призначення об'єкта"
        verbose_name_plural = "Призначення об'єктів"

    def __str__(self):
        return "%s: %s" % (self.category, self.name)


class Institution(models.Model):
    name = models.CharField('Назва закладу', max_length=500)

    class Meta:
        permissions = (
            ('view_institution', 'Переглядати заклади'),
            ('lead_institution', 'Керувати закладами'),
            ('create_institution', 'Створювати заклади'),
        )
        verbose_name = 'Заклад, установа'
        verbose_name_plural = 'Заклади, установи'

    def __str__(self):
        return self.name


class Building(MPTTModel):
    name = models.CharField('Будівля', max_length=500)
    institution = models.ForeignKey(Institution, verbose_name='Заклад')
    square = models.IntegerField('Площа')
    category = models.ForeignKey(Category, verbose_name='Категорія')
    purpose = models.ManyToManyField(ObjectPurpose, verbose_name="Призначення об'єкта")
    date_from = models.DateField('Дата здачі в експлуатацію', default=date.today)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            verbose_name='Орендодавець')

    class Meta:
        permissions = (
            ('view_building', 'Переглядати будівлі'),
            ('lead_building', 'Керувати будівлями'),
            ('create_building', 'Створювати будівлі'),
        )
        verbose_name = 'Будівля'
        verbose_name_plural = 'Будівлі'

    def __str__(self):
        return "%s %s" % (self.name, self.institution)


class MeterType(models.Model):
    name = models.CharField('Тип лічильника', max_length=200)
    unit = models.CharField('Одиниця виміру', max_length=50)

    class Meta:
        verbose_name = 'Тип лічильника'
        verbose_name_plural = 'Типи лічильників'

    def __str__(self):
        return self.name


class Meter(MPTTModel):
    name = models.CharField('Iдентифікатор лічильника', max_length=200)
    institution = models.ForeignKey(Institution, verbose_name='Заклад')
    building = models.ForeignKey(Building, verbose_name='Будівля')
    meter_type = models.ForeignKey(MeterType, verbose_name='Тип лічильника')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            verbose_name='Орендодавець')

    class Meta:
        verbose_name = 'Лічильник'
        verbose_name_plural = 'Лічильники'

    def __str__(self):
        return "%s %s" % (self.meter_type, self.name)


class MeterData(models.Model):
    meter = models.ForeignKey(Meter, verbose_name='Лічильник')
    prev_data = models.DecimalField('Попередні дані', max_digits=9, decimal_places=3)
    cur_data = models.DecimalField('Поточні дані', max_digits=9, decimal_places=3)
    timestamp = models.DateTimeField(auto_now_add=True)
    manager = models.ForeignKey(User, verbose_name='Відповідальна особа')

    class Meta:
        verbose_name = 'Показник лічильника'
        verbose_name_plural = 'Показники лічильників'

    def __str__(self):
        return "%s %s" % (self.meter, self.timestamp)


class Rate(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категорія', blank=True, null=True)
    meter_type = models.ForeignKey(MeterType, verbose_name='Тип лічильника')
    price = models.DecimalField('Тариф', max_digits=6, decimal_places=2)
    date_from = models.DateField('Тариф дійсний з')
    date_until = models.DateField('Тариф дійсний до', blank=True, null=True)

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифи'

    def __str__(self):
        return "%s %s грн." % (self.meter_type, self.price)


class Receipt(models.Model):
    meter_type = models.ForeignKey(MeterType, verbose_name='Тип лічильника')
    institution = models.ForeignKey(Institution, verbose_name='Заклад')
    building = models.ForeignKey(Building, verbose_name='Будівля')
    date_from = models.DateField('Від')
    date_until = models.DateField('До')
    quantity = models.DecimalField('Кількість використаних одиниць', max_digits=9, decimal_places=3)
    price = models.DecimalField('Вартість', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Рахунок'
        verbose_name_plural = 'Рахунки'

    def __str__(self):
        return "%s %s %s грн." % (self.institution, self. meter_type, self.price)


class ComponentType(models.Model):
    name = models.CharField('Назва', max_length=250)
    unit = models.CharField('Одиниця виміру', max_length=100)

    class Meta:
        verbose_name = 'Тип компоненту'
        verbose_name_plural = 'Типи компонентів'

    def __str__(self):
        return self.name


class Component(models.Model):
    building = models.ForeignKey(Building, verbose_name='Заклад')
    type = models.ForeignKey(ComponentType, verbose_name='Тип')
    quantity = models.DecimalField('Кількість', max_digits=1000, decimal_places=2)

    class Meta:
        verbose_name = 'Компонент'
        verbose_name_plural = 'Компоненти'

    def __str__(self):
        return "%s %s %s" % (self.building, self.type, self.quantity)


class FeatureType(models.Model):
    component_type = models.ForeignKey(ComponentType, verbose_name='Тип компоненту')
    name = models.CharField('Назва', max_length=250)

    class Meta:
        verbose_name = 'Тип Характеристики'
        verbose_name_plural = 'Типи характеристик'

    def __str__(self):
        return self.name


class Feature(models.Model):
    component = models.ForeignKey(Component, verbose_name='Компонент')
    feature_type = models.ForeignKey(FeatureType, verbose_name='Тип характеристики')
    percentage = models.DecimalField('Відсоток від загальної кількості', max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    date_from = models.DateField('Від', blank=True, null=True)
    date_until = models.DateField('До', blank=True, null=True)

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return "%s %s %s грн." % (self.component, self.feature_type, self.percentage)

    def clean(self):
        current_day = date.today()
        if self.date_until > current_day:
            raise ValidationError({
                'date_until': _("Поле не може бути більшим поточної дати")
            })

    def full_clean(self, *args, **kwargs):
        return self.clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        comp = Component.objects.get(pk=self.component_id)
        build = Building.objects.get(pk=comp.building_id)
        self.date_from = build.date_from
        super(Feature, self).save(*args, **kwargs)
