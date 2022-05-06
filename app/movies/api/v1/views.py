from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork, PersonFilmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)

    def get_queryset(self):
        return super().get_queryset().values(
                'id', 'title', 'description', 'creation_date', 'rating', 'type',
        ).annotate(
                genres=ArrayAgg('genres__name', distinct=True),
                actors=self._aggregate_person(PersonFilmwork.Role.ACTOR),
                directors=self._aggregate_person(PersonFilmwork.Role.DIRECTOR),
                writers=self._aggregate_person(PersonFilmwork.Role.SCREENWRITER),
        )

    def _aggregate_person(self, role: str) -> ArrayAgg:
        return ArrayAgg('persons__full_name', distinct=True, filter=Q(persons__personfilmwork__role=role))


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        paginator, page, queryset, _ = self.paginate_queryset(
                self.get_queryset(),
                self.paginate_by,
        )
        context = {
                'count': paginator.count,
                'total_pages': paginator.num_pages,
                'prev': page.previous_page_number() if page.has_previous() else None,
                'next': page.next_page_number() if page.has_next() else None,
                'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return self.get_object()
