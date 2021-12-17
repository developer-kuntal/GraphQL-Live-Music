from django.db import models
import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.fields import DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
# from graphql_relay import from_global_id
from .models import Song

class SongType(DjangoObjectType):
    class Meta:
        model = Song
        # _id field must be added as a primary key(name must be: <_id>)
        # fields = ("_id","title","artist", "album", "year", "duration_in_sec",
        #                     "bitrate", "lyric", "updated_at")
        filter_fields = ['_id', 'name', 'title', 'artist', 'album', 'year', 'duration_in_sec', 
                                'bitrate', 'lyric', 'updated_at']
        # # exclude = ("id",)
        interfaces = (graphene.Node, ) # ,relay.Node
        # fields = ("id","title")
        # possible_types = (Song, )

class SongConnection(relay.Connection):
    class Meta:
        node = SongType

class Query(graphene.ObjectType):

    # song = relay.Node.Field(SongType)
    # song = relay.ConnectionField(SongConnection)
    song = DjangoFilterConnectionField(SongType)
    all_songs = relay.ConnectionField(SongConnection)
    # all_songs = DjangoFilterConnectionField(SongType)
    # search_songs_by_album_name = DjangoListField(SongType,album=graphene.String())
    search_songs_by_album_name = DjangoFilterConnectionField(SongType)
    search_songs_by_artist_name = DjangoFilterConnectionField(SongType)
    # search_songs_by_album_name = graphene.List(SongType,album=graphene.String())
    # album = relay.Node.Field(AlbumType)
    #by default it takes id as a parameter
    # search_songs_by_album_name = relay.Node.Field(SongType,album=graphene.String())

    def resolve_all_songs(root,info):
        return Song.objects.all()
        # return Books.objects.filter(title="Java")
    def resolve_song(root,info,_id):
        # return Song.objects.get(pk=_id)
        return Song.objects.all()

    def resolve_search_songs_by_album_name(root,info,album):
        # Song.objects.get(album=album)
        return Song.objects.all()
        # Song.objects.
    def resolve_search_songs_by_artist_name(root,info,artist):
        # Song.objects.get(album=album)
        return Song.objects.all()
    
class AddSongMutation(graphene.Mutation):

        class Input:
            name = graphene.String()
            title = graphene.String()
            artist = graphene.String()
            album = graphene.String()
            year = graphene.String()
            duration_in_sec = graphene.Int()
            bitrate = graphene.Int()
            lyric = graphene.String()

        # from_erros = graphene.String()
        song = graphene.Field(SongType,
                        name = graphene.String(),
                        title = graphene.String(),
                        artist = graphene.String(), 
                        album = graphene.String(), 
                        year = graphene.String(), 
                        duration_in_sec = graphene.Int(), 
                        bitrate = graphene.Int(),
                        lyric = graphene.String()
                    )
        # song = graphene.Field(lambda: SongType)
        # song = DjangoConnectionField(SongType)
        # song = DjangoFilterConnectionField(SongType)
        # song = relay.ConnectionField(SongConnection)

        # @staticmethod
        @classmethod
        def mutate(cls, root, args, name=None, title=None, artist=None, album=None, year=None, 
                    duration_in_sec=None, bitrate=None, lyric=None):
            # print(song) 
            print(title)
            print("C: ",cls)
            print("D: ",root)
            print("E: ",args)
            song = Song.objects.create(
                name=name, title=title, artist=artist, album=album, year=year, 
                            duration_in_sec=duration_in_sec, bitrate=bitrate, lyric=lyric
            )
            # song.save()
            return AddSongMutation(song)

class UpdateSongMutation(graphene.Mutation):

        class Arguments:
            _id = graphene.ID()
            title = graphene.String()
            artist = graphene.String()
            album = graphene.String()
            year = graphene.String()
            duration_in_sec = graphene.Int()
            bitrate = graphene.Int()
            lyric = graphene.String()
            updated_at = graphene.DateTime()

        song = graphene.Field(SongType)
        # song = DjangoConnectionField(SongType)
        # song = DjangoFilterConnectionField(SongType)

        @classmethod
        def mutate(cls, root, info, model, _id, title, artist, album, year, duration_in_sec, bitrate, lyric):
            song = Song.objects.filter(_id=_id)
            # print(song.values_list)
            # song.count
            song.title = title
            song.artist = artist
            song.album = album
            song.year = year
            song.duration_in_sec = duration_in_sec
            song.bitrate = bitrate
            song.lyric = lyric
            song.update()
            # print(song)
            return UpdateSongMutation(song=song)

class DeleteSongMutation(graphene.Mutation):

        class Arguments:
            # _id = graphene.ID()
            _id = graphene.ID()
            # title = graphene.String()

        
        song = graphene.Field(SongType)
        # song = DjangoConnectionField(SongType)
        # song = DjangoFilterConnectionField(SongType)
        # song = relay.Node.Field(SongType)

        @classmethod
        def mutate(cls, root, info, _id):
            song = Song.objects.get(_id=_id)
            # s = DeleteSongMutation(song=song)
            song.delete()
            return DeleteSongMutation(song=song)

        # @classmethod
        # def mutate(cls, root, info, title):
        #     book = Book.objects.filter(title=title)
        #     book.delete()
        #     return DeleteBookMutation(book=book)

class Mutation(graphene.ObjectType):
    add_song = AddSongMutation.Field()
    update_song = UpdateSongMutation.Field()
    delete_song = DeleteSongMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
# schema = graphene.Schema(mutation=Mutation)