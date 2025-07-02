from django.conf import settings
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api_v1.serializers import (
    LinkShortenerSerializerRequestSerializer,
    LinkShortenerResponseSerializer,
    GetOriginalLinkRequestSerializer,
)
from link_shortener.services import CreateUrlService, GetUrlService


class LinkApiViewSet(ViewSet):

    @extend_schema(
        request=LinkShortenerSerializerRequestSerializer,
        responses={
            status.HTTP_200_OK: LinkShortenerResponseSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Bad url",
                        value={"url": "Enter a valid URL"},
                    ),
                ],
            ),
        },
    )
    @action(detail=False, methods=["post"])
    def shorten_link(self, request):
        serializer = LinkShortenerSerializerRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        short_url = CreateUrlService.create_short_url(url=serializer.validated_data["url"])
        response_serializer = LinkShortenerResponseSerializer(
            data={"url": serializer.validated_data["url"], "short_url": short_url}
        )
        response_serializer.is_valid()
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=GetOriginalLinkRequestSerializer,
        responses={
            status.HTTP_200_OK: LinkShortenerResponseSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad Request: Invalid input",
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        "Bad short url",
                        value={"short_url": "Enter a valid URL"},
                        status_codes=[status.HTTP_400_BAD_REQUEST],
                    ),
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Original input not found",
                examples=[
                    OpenApiExample(
                        "Original url not found",
                        description="Original url not found",
                        status_codes=[status.HTTP_400_BAD_REQUEST],
                    ),
                ],
            ),
        },
    )
    @action(detail=False, methods=["post"])
    def get_original_link(self, request):
        serializer = GetOriginalLinkRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        short_url_hash = serializer.validated_data["short_url"].replace(f"{settings.HOST_ADDR}/", "")
        original_url = GetUrlService.get_original_url(short_url_hash)
        if not original_url:
            return Response(status=status.HTTP_404_NOT_FOUND)
        response_serializer = LinkShortenerResponseSerializer(
            data={"url": original_url, "short_url": serializer.validated_data["short_url"]}
        )
        response_serializer.is_valid()
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)
