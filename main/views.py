from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl

from main.base_views import BaseView
from main.models import Genre, Movie
from main.forms import SiteReviewForm
from django.http import HttpRequest
from django.views.generic import View
from django.shortcuts import redirect
from django.db.models import Q

class PerformSearchMixin:
    
    def filter_movies_by_search(self,request:HttpRequest, qs):
        search_query = request.GET.get("search", "").strip()
        min_duration = request.GET.get("min_duration")
        max_duration = request.GET.get("max_duration")
        if search_query:
            qs = qs.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
        if min_duration:
            qs = qs.filter(duration__gte=min_duration)
        if max_duration:
            qs = qs.filter(duration__lte=max_duration)
        return qs

class HomePageView(BaseView):
    template_name = "main/index.html"

    def _get_page_name(self, **kwargs):
        return "Головна"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_five_movies'] = Movie.objects.filter(is_top_five=True)
        context['ganres'] = Genre.objects.all()
        return context



class MovieTypeView(BaseView, PerformSearchMixin):
    template_name = "main/catalog.html"

    def _get_page_name(self, **kwargs):
        return dict(Movie.TYPES).get(kwargs['type_num'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movies = Movie.objects.filter(type=kwargs['type_num'])
        context['movies'] = self.filter_movies_by_search(self.request, movies)
        return context
    
class YearsView(BaseView, PerformSearchMixin):
    template_name = "main/catalog.html"

    def _get_page_name(self, **kwargs):
        year = kwargs.get("year")
        return f"Фільми {year} року"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movies = Movie.objects.filter(release_date__year=kwargs.get("year"))
        context['movies'] = self.filter_movies_by_search(self.request, movies)
        return context
    
class GenreView(BaseView, PerformSearchMixin):
    template_name = "main/catalog.html"

    def _get_page_name(self, **kwargs):
        genre_name = kwargs.get("genre_name")
        return f"Фільми {genre_name}"
    
    def get_context_data(self, **kwargs):
        genre_id = kwargs.get("genre_id")
        genre = Genre.objects.get(id=genre_id)
        kwargs['genre_name'] = genre.name

        context = super().get_context_data(**kwargs)
        
        movies = genre.movies.all()
        context['movies'] = self.filter_movies_by_search(self.request, movies)
        return context
    
class CreateSiteReviewView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        referer = request.headers.get("Referer") or "/"
        referer_parts = urlsplit(referer)
        referer_path = referer_parts.path or "/"
        referer_query = dict(parse_qsl(referer_parts.query, keep_blank_values=True))
        form = SiteReviewForm(request.POST)

        if form.is_valid():
            form.save()
            referer_query.pop("error_message", None)
            cleaned_query = urlencode(referer_query, doseq=True)
            return redirect(urlunsplit(("", "", referer_path, cleaned_query, "")))

        error_text = "; ".join(
            error for errors in form.errors.values() for error in errors
        ) or "Invalid data"
        referer_query["error_message"] = error_text
        error_query = urlencode(referer_query, doseq=True)
        return redirect(urlunsplit(("", "", referer_path, error_query, "")))
