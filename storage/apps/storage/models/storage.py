import os
from django.utils.translation import gettext_lazy as _
from django.db import models
from utils.fields import IdField
from utils.string_utils import uuid_8


def upload_origin_file(instance, file_name):
    name, suffix = os.path.splitext(file_name)
    remote_path = "{name}_{secret}{suffix}".format(name=name, secret=instance.pk, suffix=suffix)
    return '/'.join([instance.pk, 'origin', remote_path])


def upload_thumb_file(instance, file_name):
    name, suffix = os.path.splitext(file_name)
    remote_path = "{name}_{secret}{suffix}".format(name=name, secret=instance.pk, suffix=suffix)
    return '/'.join([instance.pk, 'thumb', remote_path])


class ImageStorage(models.Model):

    id = IdField()
    name = models.CharField(verbose_name=_("名称"), help_text=_("名称"), max_length=32)
    thumb = models.FileField(verbose_name=_('缩略图'), help_text=_('缩略图'), upload_to=upload_thumb_file, null=False)
    file = models.FileField(verbose_name=_('文件'), help_text=_('文件'), upload_to=upload_origin_file, null=False)
    size = models.PositiveIntegerField(verbose_name=_("文件大小"), help_text=_('文件大小'), null=False)
    width = models.PositiveIntegerField(verbose_name=_("图片宽度"), help_text=_("图片宽度"), null=False)
    height = models.PositiveIntegerField(verbose_name=_("图片高度"), help_text=_("图片高度"), null=False)

    class Meta:
        verbose_name = '文件存储'
        verbose_name_plural = verbose_name
        app_label = 'storage'
        db_table = 'e2_storage'

    def __str__(self):
        return f"{self.name}"
