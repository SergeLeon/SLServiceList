from django.utils import timezone
from datetime import datetime
from .models import Redirection

NO_LIMIT = -1
NO_DATETIME = datetime(1970, 1, 1, tzinfo=timezone.get_current_timezone())
print(NO_DATETIME)


def create_redirection(full_link: str, short_link: str, delete_at: datetime | None, redirect_limit: int | None):
    try:
        redirection = Redirection.objects.get(short_link=short_link, active=True)
        print(redirection.id)
        return False

    except Redirection.DoesNotExist:
        if delete_at is None:
            delete_at = NO_DATETIME
        if redirect_limit is None:
            redirect_limit = NO_LIMIT
        print(full_link, short_link, delete_at, redirect_limit)
        redirection = Redirection(full_link=full_link, short_link=short_link,
                                  delete_at=delete_at, redirect_limit=redirect_limit)
        redirection.save()
        print(redirection.id, "Created")
        return True


def deactivate_redirection(redirection=None, redirection_id=None, short_link=None):
    assert (redirection, redirection_id, short_link).count(None) != 1, "one argument expected"

    try:
        if redirection_id:
            redirection = Redirection.objects.get(id=redirection_id)
        elif short_link:
            redirection = Redirection.objects.get(short_link=short_link, active=True)
    except Redirection.DoesNotExist:
        return True

    redirection.active = False
    redirection.save()
    print(redirection.id, "Deleted")
    return False


def get_full_link(short_link: str) -> str:
    try:
        redirection = Redirection.objects.get(short_link=short_link, active=True)
        if check_redirection(redirection):
            redirection.redirect_count += 1
            redirection.save()
            return redirection.full_link

        deactivate_redirection(redirection=redirection)
        raise Redirection.DoesNotExist
    except Redirection.DoesNotExist:
        return ""


def check_redirection(redirection: Redirection) -> bool:
    count_unlimited = redirection.redirect_limit == NO_LIMIT
    time_unlimited = redirection.delete_at.timestamp() == NO_DATETIME.timestamp()

    within_count = redirection.redirect_count < redirection.redirect_limit
    within_time = timezone.now().timestamp() < redirection.delete_at.timestamp()

    counter_is_normal = count_unlimited or within_count
    time_is_normal = time_unlimited or within_time

    return counter_is_normal and time_is_normal
