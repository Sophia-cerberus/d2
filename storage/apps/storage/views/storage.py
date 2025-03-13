import os
import shutil
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from apps.storage.serializers import (
    ImageStorageListOrRetrieveSerializer, ImageStorageCreateOrUpdateSerializer
)
from apps.storage.models import ImageStorage
from utils.viewsets import ModelViewSet
from utils.response import SuccessResponse, ErrorResponse
from rest_framework import status


def delete_instance_files(path):
    # 获取 media 目录路径
    media_root = os.path.join(settings.MEDIA_ROOT, str(path))
    
    # 判断文件夹是否存在，如果存在则删除
    if os.path.exists(media_root) and os.path.isdir(media_root):
        shutil.rmtree(media_root)  # 删除整个目录及其内容
        

class ImageStorageViewSet(ModelViewSet):

    queryset = ImageStorage.objects.filter()
    serializer_class = ImageStorageListOrRetrieveSerializer
    create_serializer_class = ImageStorageCreateOrUpdateSerializer
    update_serializer_class = ImageStorageCreateOrUpdateSerializer
    partial_update_serializer_class = ImageStorageCreateOrUpdateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            delete_instance_files(instance.pk)  # 删除与实例相关的文件夹及文件
            self.perform_destroy(instance)
        except ObjectDoesNotExist:
            return ErrorResponse(data={'detail': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)

        return SuccessResponse(status=status.HTTP_204_NO_CONTENT)

