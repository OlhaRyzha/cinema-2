from django.urls import path
from main.views import HomePageView, MovieTypeView, YearsView, GenreView, CreateSiteReviewView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('type/<int:type_num>/', MovieTypeView.as_view(), name="type_view"),
    path("years/<int:year>/", YearsView.as_view(), name="year_view"),
    path('genre/<int:genre_id>/', GenreView.as_view(), name="genre_view"),
    path('create_review/', CreateSiteReviewView.as_view(), name="create_review"),
]