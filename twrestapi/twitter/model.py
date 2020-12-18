from mongoengine import *


class Twitt(Document):

    id = StringField(primary_key=True)
    text = StringField(required=True)
    created_at = StringField(required=True)
    post_hour = IntField(required=True)
    hashtag = StringField(required=True)
    lang = StringField(required=True)
    author_id = StringField(required=True)
    username = StringField(required=True)
    name = StringField(required=True)
    location = StringField(required=True)
    followers_count = IntField(required=True)


        







    


