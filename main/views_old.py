from main.base_views import BaseView
from main.models import Genre, Movie, SiteReview
from main.forms import SiteReviewForm
from django.http import HttpRequest

class HomePageView(BaseView):
    template_name = "main/index.html"

    def _get_page_name(self, **kwargs):
        return "Головна"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_five_movies'] = Movie.objects.filter(is_top_five=True)
        context['ganres'] = Genre.objects.all()
        context['site_reviews'] = SiteReview.objects.all()
        # form = kwargs.get("form")
        # if not form:
        #     context['form'] = SiteReviewForm()
        # else:
        #     context['form'] = form
        context['error_message'] = kwargs.get("error_message")
        return context
    
    # def post(self, request: HttpRequest, *args, **kwargs):
    #     form = SiteReviewForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #     else:
    #         kwargs['form'] = form
    #     return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request: HttpRequest, *args, **kwargs):
        data = request.POST
        form = SiteReviewForm(data)
        if form.is_valid():
            form.save()
        # name = data.get("user_name")
        # mark = int(data.get("mark"))
        # text = data.get("text")

        # error_message = None

        # if name and mark and text:
        #     if len(name) > 100:
        #         error_message = "Enter valid name"
        #     elif 1 < mark or mark > 10:
        #         error_message = "Enter valid mark"
        #     else:
        #         SiteReview.objects.create(
        #             name=name,
        #             mark=mark,
        #             text=text
        #         )
        # kwargs['error_message'] = error_message
        return self.render_to_response(self.get_context_data(**kwargs))

class MovieTypeView(BaseView):
    template_name = "main/catalog.html"

    def _get_page_name(self, **kwargs):
        return dict(Movie.TYPES).get(kwargs['type_num'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = Movie.objects.filter(type=kwargs['type_num'])
        return context
    
class YearsView(BaseView):
    template_name = "main/catalog.html"

    def _get_page_name(self, **kwargs):
        year = kwargs.get("year")
        return f"Фільми {year} року"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = Movie.objects.filter(release_date__year=kwargs.get("year"))
        return context
    
class GenreView(BaseView):
    template_name = "main/catalog.html"

    def _get_page_name(self, **kwargs):
        genre_name = kwargs.get("genre_name")
        return f"Фільми {genre_name}"
    
    def get_context_data(self, **kwargs):
        genre_id = kwargs.get("genre_id")
        genre = Genre.objects.get(id=genre_id)
        kwargs['genre_name'] = genre.name

        context = super().get_context_data(**kwargs)
        
        context['movies'] = genre.movies.all()
        return context