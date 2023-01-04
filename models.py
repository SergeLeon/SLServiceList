from django.db import models


class Redirection(models.Model):
    """Redirect Information"""
    full_link = models.CharField('full link', max_length=255)
    short_link = models.CharField('shortened link', max_length=255)
    created_at = models.DateTimeField('datetime of creation', auto_now_add=True)
    delete_at = models.DateTimeField('datetime to delete')
    redirect_count = models.IntegerField('count of redirects', default=0, )
    redirect_limit = models.IntegerField('redirect limit')
    active = models.BooleanField("activity", default=True)

    class Meta:
        db_table = "redirection"
