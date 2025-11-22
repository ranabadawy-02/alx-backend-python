import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter messages sent within time range
    start_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')

    # Filter by sender user_id
    sender_id = django_filters.NumberFilter(field_name="sender__user_id", lookup_expr='exact')

    # Filter by conversation_id
    conversation_id = django_filters.NumberFilter(field_name="conversation__conversation_id", lookup_expr='exact')

    class Meta:
        model = Message
        fields = ['sender_id', 'conversation_id', 'start_date', 'end_date']
