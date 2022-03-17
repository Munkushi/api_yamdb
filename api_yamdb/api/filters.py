from django_filters import rest_framework
from reviews.models import Titles


class TitleFilters(rest_framework.FilterSet):
    """Класс для фильтра модели Title."""
    category = rest_framework.CharFilter(field_name="category__slug")
    genre = rest_framework.CharFilter(field_name="genre__slug")
    name = rest_framework.CharFilter(field_name="name")
    year = rest_framework.NumberFilter(field_name="year")

    class Meta:
        model = Titles
        fields = ("category", "genre", "name", "year")