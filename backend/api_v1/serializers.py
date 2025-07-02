from rest_framework import serializers


class LinkShortenerSerializerRequestSerializer(serializers.Serializer):
    url = serializers.URLField(
        max_length=512,
        label="Original URL",
    )


class LinkShortenerSerializerResponseSerializer(serializers.Serializer):
    url = serializers.URLField(
        max_length=512,
        label="Original URL",
    )
    short_url = serializers.URLField(
        max_length=512,
        label="Short URL",
    )
