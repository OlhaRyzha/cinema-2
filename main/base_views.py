from django.views.generic import TemplateView
from main.models import Movie, SiteReview


class BaseView(TemplateView):
    def _get_page_name(self, **kwargs):
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_name"] = self._get_page_name(**kwargs)
        context["years"] = (
            Movie.objects.all()
            .values_list("release_date__year", flat=True)
            .distinct()
            .order_by("-release_date__year")
        )
        context['site_reviews'] = SiteReview.objects.all()
        return context
