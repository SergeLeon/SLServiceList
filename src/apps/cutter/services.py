from django.utils import timezone
from datetime import datetime
from .models import Redirection

from string import ascii_letters, digits
from random import sample

NO_LIMIT = -1
NO_DATETIME = datetime(1970, 1, 1, tzinfo=timezone.get_current_timezone())

URL_CHARACTERS = ascii_letters + digits
BASE_LINK_LEN = 4


def create_redirection(full_link: str, short_link: str, delete_at: datetime | str, redirect_limit: int | str) -> dict:
    if not full_link:
        return {"title": "Cannot create",
                "description": "Link must be provided for shortening."}

    if delete_at:
        if isinstance(delete_at, str):
            delete_at = datetime.fromisoformat(delete_at)

        if delete_at.timestamp() <= timezone.now().timestamp():
            return {"title": "Cannot create",
                    "description": "The specified time cannot be earlier than the current time."}

    if not short_link:
        short_link = random_str(BASE_LINK_LEN)

    if Redirection.objects.filter(short_link=short_link, active=True).exists():
        return {"title": "Cannot create",
                "description": "The shortened link is already taken"}

    if not delete_at:
        delete_at = NO_DATETIME

    if not redirect_limit:
        redirect_limit = NO_LIMIT

    elif redirect_limit.isdigit() and int(redirect_limit) <= 0:
        return {"title": "Cannot create",
                "description": "Redirect limit cannot be less than 1"}

    redirection = Redirection(full_link=full_link, short_link=short_link,
                              delete_at=delete_at, redirect_limit=redirect_limit)
    redirection.save()
    return {"title": "Successfully created",
            "description": f"{full_link=};\n{short_link=};\n{delete_at=};\n{redirect_limit=};"}


def deactivate_redirection(redirection=None, redirection_id=None, short_link=None) -> dict:
    assert (redirection, redirection_id, short_link).count(None) != 1, "one argument expected"

    try:
        if redirection_id:
            redirection = Redirection.objects.get(id=redirection_id)
        elif short_link:
            redirection = Redirection.objects.get(short_link=short_link, active=True)
    except Redirection.DoesNotExist:
        return {"title": "Cannot delete",
                "description": "Can't remove link"}

    redirection.active = False
    redirection.save()

    return {"title": "Successfully removed",
            "description": "Shortened link removed successfully"}


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


def random_str(length, characters=URL_CHARACTERS):
    return "".join(sample(characters, length))
