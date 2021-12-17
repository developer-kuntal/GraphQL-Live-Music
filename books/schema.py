import json
import graphene
from graphene_django import DjangoObjectType
from .models import Book


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id","title","excerpt")

class Query(graphene.ObjectType):

    all_books = graphene.List(BookType)
    indivisual_books = graphene.Field(BookType, id=graphene.ID(required=True))

    def resolve_all_books(root,info):
        return Book.objects.all()
        # return Books.objects.filter(title="Java")
    def resolve_indivisual_books(root,info,id):
        return Book.objects.get(pk=id)

class BookInput(graphene.InputObjectType):
        title = graphene.String()
        excerpt = graphene.String()

class AddBookMutation(graphene.Mutation):

        class Arguments:
            book_data = BookInput(required=False)

        book = graphene.Field(BookType)

        # @classmethod
        @staticmethod
        def mutate(root, info, book_data=None):
            # book_instance = Book.objects.create(title=book_data.title,excerpt=book_data.excerpt)
            book_instance = Book.objects.create(title=book_data.title,excerpt=book_data.excerpt)
            print("Colum1: ", book_data.title, book_data.excerpt)
            print("Column2: ", root)
            print("Column3: ", info)
            # book.title = title
            # book = book_data
            if book_instance:
                # book_instance.save()
            # return AddBookMutation(book)
            # return json.dumps(obj=book)
            # json.dumps(obj={"title": book_data.title, "excerpt":book_data.excerpt})
                return AddBookMutation(book=book_instance)
            return AddBookMutation(book=None)
        

class UpdateBookMutation(graphene.Mutation):

        class Arguments:
            id = graphene.ID()
            title = graphene.String()
            excerpt = graphene.String()

        book = graphene.Field(BookType)

        @classmethod
        def mutate(cls, root, info, id, title, excerpt):
            book = Book.objects.get(id=id)
            book.title = title
            book.excerpt = excerpt
            book.save()
            return UpdateBookMutation(book=book)

class DeleteBookMutation(graphene.Mutation):

        class Arguments:
            id = graphene.ID()
            # title = graphene.String()

        book = graphene.Field(BookType)

        @classmethod
        def mutate(cls, root, info, id):
            book = Book.objects.get(id=id)
            book.delete()
            return DeleteBookMutation(book=book)

        # @classmethod
        # def mutate(cls, root, info, title):
        #     book = Book.objects.filter(title=title)
        #     book.delete()
        #     return DeleteBookMutation(book=book)

class Mutation(graphene.ObjectType):
    add_book = AddBookMutation.Field()
    update_book = UpdateBookMutation.Field()
    delete_book = DeleteBookMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
print(schema)