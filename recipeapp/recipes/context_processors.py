from django.db.models import Q
from .models import Notification


def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(is_read=False)
        notifications = notifications.filter(
            Q(comment__recipe__author=request.user)
            | Q(like__recipe__author=request.user)
        )
        return {"notifications": notifications}
    return {}
