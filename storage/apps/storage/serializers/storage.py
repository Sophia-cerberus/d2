from rest_framework import serializers
from apps.storage.models import ImageStorage
from django.core.files.base import ContentFile
from PIL import Image
import io

class ImageStorageListOrRetrieveSerializer(serializers.ModelSerializer):

    file = serializers.CharField(source='file.url', read_only=True)
    thumb = serializers.CharField(source='thumb.url', read_only=True)

    class Meta:
        model = ImageStorage
        fields = '__all__'


class ImageStorageCreateOrUpdateSerializer(serializers.ModelSerializer):

    width = serializers.IntegerField(read_only=True)
    height = serializers.IntegerField(read_only=True)
    size = serializers.IntegerField(read_only=True)
    thumb = serializers.ImageField(read_only=True)

    class Meta:
        model = ImageStorage
        fields = ('file', 'width', 'height', 'size', 'thumb')

    def validate_file(self, value):
        """验证上传文件的格式，仅允许 jpg、jpeg、png 格式"""
        allowed_extensions = ['jpg', 'png', 'jpeg']
        max_size = 5 * 1024 * 1024  # 限制最大文件大小为 5MB

        filename: str = value.name.lower()
        if not any(filename.endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError("仅支持 jpg、jpeg、png 格式的图片")
        
        if value.size > max_size:
            raise serializers.ValidationError("文件大小不能超过 5MB")

        return value

    def create(self, validated_data) -> ImageStorage:
        # 获取上传的文件对象
        file_obj = validated_data.get('file')
        try:
            image = Image.open(file_obj)
        except Exception:
            raise serializers.ValidationError("无法打开图片文件，请确认文件格式有效")
        
        width, height = image.size

        thumb_size = (200, 200)
        # thumb_size = image.size
        image_copy = image.copy()
        image_copy.thumbnail(thumb_size, Image.LANCZOS)

        # 将缩略图保存到内存中
        thumb_io = io.BytesIO()
        # 若图片格式不确定，可以统一保存为 JPEG
        image_copy.save(thumb_io, format='JPEG')
        thumb_file = ContentFile(thumb_io.getvalue(), name=f"{file_obj.name}")

        # 创建模型实例，同时保存额外计算的属性
        instance = ImageStorage.objects.create(
            file=file_obj,
            width=width,
            height=height,
            size=file_obj.size,
            thumb=thumb_file
        )
        return instance