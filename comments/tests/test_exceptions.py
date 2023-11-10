import sys

from unittest.mock import patch
from rest_framework import status



from core.exceptions import BadRequest
from django.test import TestCase
from core.messages import ExceptionError

