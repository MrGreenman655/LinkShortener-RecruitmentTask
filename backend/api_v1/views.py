from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v1.serializers import LinkShortenerSerializerRequestSerializer, LinkShortenerSerializerResponseSerializer
from link_shortener.services import CreateUrlService


class LinkShortenerApiView(APIView):

    @extend_schema(
        request=LinkShortenerSerializerRequestSerializer,
        responses={
            status.HTTP_200_OK: LinkShortenerSerializerResponseSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Bad Request: Invalid input",
                examples=[
                    OpenApiExample(
                        "Bad url",
                        value={"url": "Enter a valid URL"},
                        request_only=True,
                        status_codes=[status.HTTP_400_BAD_REQUEST],
                    ),
                ],
            ),
        },
    )
    def post(self, request):
        serializer = LinkShortenerSerializerRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        short_url = CreateUrlService.create_short_url(url=serializer.validated_data["url"])
        response_serializer = LinkShortenerSerializerResponseSerializer(
            data={"url": serializer.validated_data["url"], "short_url": short_url}
        )
        response_serializer.is_valid()
        return Response(data=response_serializer.data)
