from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView

from link_shortener.services import GetUrlService


class HashRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        url = GetUrlService.get_original_url(self.kwargs["hash"])
        if not url:
            return reverse_lazy("hash_not_found")
        return url


class HashNotFoundTemplateView(TemplateView):
    template_name = "hash_not_found.html"
    extra_context = {
        'title': "Short url not found!",
    }