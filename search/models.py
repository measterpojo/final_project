from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User

from django.conf import settings

from django.db import connections

class SearchManager(models.Manager):

    def search(self, search_query):
        pass