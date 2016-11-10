from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class User(MPTTModel, AbstractBaseUser):
    post = models.CharField('Посада', max_length=250)
    last_name = models.CharField('Прізвище', max_length=50)
    first_name = models.CharField("Ім'я", max_length=50)
    middle_name = models.CharField('По-батькові', max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, verbose_name='Керівник')
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    e_mail = models.EmailField()

    def __str__(self):
        return "%s %s %s. %s." % (self.post, self.last_name, self.first_name[0], self.middle_name[0])