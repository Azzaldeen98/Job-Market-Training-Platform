from django.db import models


class BaseModel(models.Model):

    # app_name=""
    # def get_app_url(self, view_name):
    #    return self.get_app_url

    def get_url(self, view_name, args_list=None):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse(view_name, args=args_list)
        except NoReverseMatch:
            # إذا لم يجد الرابط، سيعيد رابطاً وهمياً يوضح لك المشكلة في المتصفح
            return f"/error-not-found-link-named-{view_name}/"
    class Meta:
        abstract = True


class BaseProfile(models.Model):
    # phone_number = models.CharField(max_length=15, blank=True, unique=True, null=True, verbose_name=_("phone number")) #


    class Meta:
        abstract = True