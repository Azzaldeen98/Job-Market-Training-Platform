from django.db import models

from core.helpers import get_url_view


class BaseModel(models.Model):

    # app_name=""
    # def get_app_url(self, view_name):
    #    return self.get_app_url

    def get_url(self, view_name, args_list=None):
        return  get_url_view(view_name,args_list)


    class Meta:
        abstract = True


class BaseProfile(models.Model):
    # phone_number = models.CharField(max_length=15, blank=True, unique=True, null=True, verbose_name=_("phone number")) #


    class Meta:
        abstract = True