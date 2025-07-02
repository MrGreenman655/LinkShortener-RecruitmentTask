from django.conf import settings
from django.core.cache import cache

from common.services import Base62
from link_shortener.models import Link


class UrlCacheManager:
    SHORT_LINK_PREFIX = "short_link"
    LONG_LINK_PREFIX = "long_link"

    @classmethod
    def get_short_url_from_cache(cls, url: str) -> str | None:
        """Return short url from cache based on url."""
        return cache.get(f"{cls.LONG_LINK_PREFIX}_{url}")

    @classmethod
    def get_original_url_from_cache(cls, short_url_hash: str) -> str | None:
        """Return original from cache based on short url."""
        return cache.get(f"{cls.SHORT_LINK_PREFIX}_{short_url_hash}")

    @classmethod
    def set_short_url_hash_in_cache(cls, url: str, short_url_hash: str) -> None:
        """Set short_url_hash with url as key."""
        cache.set(
            f"{cls.LONG_LINK_PREFIX}_{url}",
            short_url_hash,
        )

    @classmethod
    def set_original_url_hash_in_cache(cls, url: str, short_url_hash: str) -> None:
        """Set url with short_url_hash as key."""
        cache.set(
            f"{cls.SHORT_LINK_PREFIX}_{short_url_hash}",
            url,
        )


class GetUrlService:

    @classmethod
    def get_short_url(cls, url: str) -> str | None:
        short_url_hash = UrlCacheManager.get_short_url_from_cache(url)
        if not short_url_hash:
            url_obj = Link.objects.filter(url=url, short_url_hash__isnull=False).first()
            if url_obj:
                short_url_hash = url_obj.short_url_hash
                UrlCacheManager.set_short_url_hash_in_cache(url, url_obj.short_url_hash)
        if short_url_hash:
            return cls._build_url(short_url_hash)
        return None

    @classmethod
    def get_original_url(cls, short_url_hash: str) -> str | None:
        url = UrlCacheManager.get_original_url_from_cache(short_url_hash)
        if not url:
            url_obj = Link.objects.filter(
                short_url_hash=short_url_hash,
            ).first()
            if url_obj:
                url = url_obj.url
                UrlCacheManager.set_original_url_hash_in_cache(url, url_obj.short_url_hash)
        return url

    @classmethod
    def _build_url(cls, short_url_hash: str) -> str:
        return f"{settings.HOST_ADDR}/{short_url_hash}"


class CreateUrlService:

    @classmethod
    def create_short_url(cls, url: str) -> str:
        """If there is a shortened link it returns it. Otherwise, it creates it."""
        short_url = GetUrlService.get_short_url(url)
        if not short_url:
            cls._create_short_hash(url)
        return GetUrlService.get_short_url(url)

    @classmethod
    def _create_short_hash(cls, url) -> None:
        obj = Link.objects.create(url=url)
        url_hash = Base62.encode(obj.id + 10000)
        obj.short_url_hash = url_hash
        obj.save()
