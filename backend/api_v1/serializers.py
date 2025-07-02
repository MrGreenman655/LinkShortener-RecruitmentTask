from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class LinkShortenerSerializerRequestSerializer(serializers.Serializer):
    url = serializers.URLField(
        max_length=512,
        label="Original URL",
    )


class LinkShortenerResponseSerializer(serializers.Serializer):
    url = serializers.URLField(
        max_length=512,
        label="Original URL",
    )
    short_url = serializers.URLField(
        max_length=512,
        label="Short URL",
    )


class GetOriginalLinkRequestSerializer(serializers.Serializer):
    short_url = serializers.URLField(
        max_length=512,
        label="Short URL",
    )

    def validate_short_url(self, value):
        if not value.startswith(settings.HOST_ADDR):
            print("here")
            raise ValidationError(f"Url must begin with {settings.HOST_ADDR}")
        return value
