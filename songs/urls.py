from django.urls import path
from graphene_django.views import GraphQLView
from songs.schema import schema
# from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # Only a single URL to access GraphQL
    # url(r"graphql", GraphQLView.as_view(graphiql=True,schema=schema)),
    path("graphql",csrf_exempt(GraphQLView.as_view(graphiql=True,schema=schema))),
    # path("graphql",GraphQLView.as_view(graphiql=True,schema=schema)),
]