from django.core.management.base import BaseCommand

from huscy.attributes.services import _create_attribute_category_permissions, get_attribute_schema


class Command(BaseCommand):
    help = ('Create attribute category permissions when attribute schema is created via admin'
            'interface instead of REST API.')

    def handle(self, *args, **options):
        attribute_schema = get_attribute_schema()
        _create_attribute_category_permissions(attribute_schema.schema)
