from django.contrib.auth.models import AbstractUser
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class User(AbstractUser, MPTTModel):
    email = models.EmailField('Електронна пошта', unique=True)
    post = models.CharField('Посада', max_length=250)
    last_name = models.CharField('Прізвище', max_length=50)
    first_name = models.CharField("Ім'я", max_length=50)
    middle_name = models.CharField('По-батькові', max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, verbose_name='Керівник')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "%s %s. %s." % (self.last_name, self.first_name[0], self.middle_name[0])

    def get_full_name(self):
        return "%s %s. %s." % (self.last_name, self.first_name, self.middle_name)

    def get_short_name(self):
        return self.first_name