import pytest
from model_bakery import baker

from django.contrib.auth.models import Permission
from django.core.management import call_command

pytestmark = pytest.mark.django_db


@pytest.fixture
def attribute_schema_without_categories():
    baker.make('attributes.AttributeSchema', schema={
        'type': 'object',
        'properties': {
            'property1': {'type': 'string'},
            'property2': {'type': 'number'},
        }
    })


@pytest.fixture
def attribute_schema_with_categories():
    baker.make('attributes.AttributeSchema', schema={
        'type': 'object',
        'properties': {
            'property1': {'type': 'string'},
            'property2': {'type': 'object', 'properties': {}},
            'property3': {'type': 'number'},
        }
    })


def test_create_no_permissions(attribute_schema_without_categories):
    assert not Permission.objects.filter(codename__contains='_attribute_category_').exists()

    call_command('create_attribute_category_permissions')

    assert not Permission.objects.filter(codename__contains='_attribute_category_').exists()


def test_create_permissions(attribute_schema_with_categories):
    assert not Permission.objects.filter(codename__contains='_attribute_category_').exists()

    print(attribute_schema_with_categories)
    call_command('create_attribute_category_permissions')

    assert 2 == Permission.objects.filter(codename__contains='_attribute_category_').count()
    assert Permission.objects.filter(codename='change_attribute_category_property2').exists()
    assert Permission.objects.filter(codename='view_attribute_category_property2').exists()
