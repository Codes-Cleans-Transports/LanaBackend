from django.test import TestCase
from core.models import *

class CoreTestCase(TestCase):

    def test_Example(self):
        """Mongodb saves"""
        e = Entry()
        e.blog = {
            'name': 'Djongo'
        }
        e.headline = 'The Django MongoDB connector'
        e.save()

        post = Entry.objects.all()
        print(post)