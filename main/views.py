from main.base_views import BaseView
from main.models import Genre, Movie
from main.forms import SiteReviewForm
from django.http import HttpRequest
from django.views.generic import View
from django.http import HttpResponse
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
        
        context['error_message'] = kwargs.get("error_message")
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
        data = request.POST
        form = SiteReviewForm(data)
        if form.is_valid():
            form.save()
        return redirect(request.headers.get("Referer") + f'?error_message={error_text}')