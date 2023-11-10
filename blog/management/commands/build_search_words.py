from django.core.management.base import BaseCommand


from blog.models import Tag, Category


class Command(BaseCommand):
    help = 'build search words'

    def handle(self, *args, **options):
        datas = set(
            [t.name for t in Tag.objects.all()] + 
            [t.name for t in Category.objects.all()]
            )
        print('\n'.join(datas))