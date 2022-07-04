
import django_filters
from .models import Question
from taggit.forms import TagField

class TagFilter(django_filters.CharFilter):
    field_class = TagField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('lookup_expr', 'in')
        super().__init__(*args, **kwargs)

class QuestionFilter(django_filters.FilterSet, TagFilter):
    tags = TagFilter(field_name='tags__name')
    order_by = django_filters.OrderingFilter(
        fields =(
            ('created','created'),
        )
    )
    class Meta:
        model = Question
        fields = ['order_by','tags']