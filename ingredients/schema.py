import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from ingredients.models import Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ['id', 'name', 'ingredients']
        interfaces = (relay.Node, )
        filter_fields = ['name', 'ingredients']


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "notes", "category"]
        # Allow for some more advanced filtering here
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'notes': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    category = relay.Node.Field(CategoryType)
    all_categories = DjangoFilterConnectionField(CategoryType)

    ingredient = relay.Node.Field(IngredientType)
    all_ingredients = DjangoFilterConnectionField(IngredientType)
