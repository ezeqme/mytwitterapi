import requests
import json
import logging
import datetime
import collections
import time
from functools import wraps
from .model import Twitt
from flask_log_request_id import current_request_id


class TwittCLogic():

    def __init__(self):

        self._applog = logging.getLogger("twitter.app")

    def timed(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            applog.debug("time exec", extra={"level":"debug", "function":func.__name__, "time": round(end - start, 2)})
            return result

    return wrapper

    def _get_user_info(self, list_users, author_id):

        for user in list_users:

            if user['id']==author_id:

                return user

    @timed
    def publish(self, tweets_list):
        
        try:

            for tweet in tweets_list:
            
                twitte = Twitt( id=tweet['id'],
                                    text=tweet['text'],
                                    created_at=tweet['created_at'],
                                    post_hour=tweet['post_hour'],
                                    hashtag=tweet['hashtag'],
                                    lang=tweet['lang'], 
                                    author_id=tweet['author_id'], 
                                    username=tweet['username'], 
                                    name=tweet['name'], 
                                    location=tweet['location'],
                                    followers_count=tweet['followers_count']
                ).save()

                self._applog.debug("Post save in database.", extra={'logger': __name__, 'level': 'debug', 'uuid': current_request_id(), 'post_data': tweet })

        except Exception as e:

            self._applog.error("Error publish post.", extra={'logger': __name__, 'level': 'error', 'uuid': current_request_id() })
            self._applog.debug("Error publish post.", extra={'logger': __name__, 'level': 'debug', 'uuid': current_request_id(), 'post_data': tweet})

            return False

        return True

    @timed
    def list_users_by_followers(self, order='ASC', limit=5):

        list_users = []

        order_query_param = ""

        if order == 'ASC':

            order_query_param='+followers_count'

        elif order == 'DESC':

            order_query_param='-followers_count'

        twitts = Twitt.objects.order_by(order_query_param)[:limit]

        for t in twitts:

            list_users.append("username: %s, followers: %s" % (t.username, t.followers_count))
        
        return list_users
 
    @timed
    def total_posts_by_hour(self):

        list_posts = []

        pipeline = [ { "$group": { "_id": "$post_hour", 'total_post': {'$sum': 1 }}},
                     { "$sort" : { "_id" : 1 } }
                   ]
        self._applog.debug("Exec pipeline in database", extra={'logger': __name__, 'level': 'debug', 'uuid': current_request_id()})
        
        data = Twitt.objects().aggregate(pipeline)

        self._applog.debug("Exec pipeline OK", extra={'logger': __name__, 'level': 'debug', 'uuid': current_request_id()})

        for d in data:  

            list_posts.append(d)
        
        return list_posts

    def _get_list_score_lang(self, usernames):

        pipeline_lang = [{ 
                        "$group": { 
                                    "_id": "$lang", 
                                    "hashtag": { "$push": "$hashtag" }, 
                                    "count": {"$sum": 1} 
                                } 
                    }]

        

        list_score_lang=[]

        for user in usernames:

            for tag in self._get_tag_list():

                self._applog.debug("Exec pipeline in database", extra={'logger': __name__, 'level': 'debug', 'uuid': current_request_id()})
                
                data = Twitt.objects(hashtag=tag,username=user['_id']).aggregate(pipeline_lang)

                self._applog.debug("Exec pipeline OK", extra={'logger': __name__, 'level': 'debug', 'uuid': current_request_id()})

                for d in data:

                    score_lang = {}
                    score_lang["username"]=user["_id"]
                    score_lang["hashtag"]=tag
                    score_lang["lang"]=d['_id']
                    score_lang["count"]=d['count']

                    list_score_lang.append(score_lang)
        
        return list_score_lang

    def _get_list_score_country(self, usernames):

        pipeline_location = [{ 
                            "$group": { 
                                        "_id": "$location", 
                                        "hashtag": { "$push": "$hashtag" }, 
                                        "count": {"$sum": 1} 
                                    } 
                        }]

        list_score_country = []

        for user in usernames:

            for tag in self._get_tag_list():
                
                data_location = Twitt.objects(hashtag=tag,username=user['_id']).aggregate(pipeline_location)

                for d in data_location:

                    score_country = { }
                    score_country["username"]=user["_id"]
                    score_country["hashtag"]=tag
                    score_country["country"]=d['_id']
                    score_country["count"]=d['count']

                    list_score_country.append(score_country)

        return list_score_country


    def _get_tag_list(self):

        pipeline_tags = [{ 
                        "$group": { 
                                    "_id": "$hashtag"
                                } 
                    }]

        data = Twitt.objects().aggregate(pipeline_tags)

        list_tags = []

        for d in data:
            list_tags.append(d['_id'])

        return list_tags

    @timed
    def total_posts_by_tag(self, group_by="location"):

        pipeline_user = [{ 
                            "$group": { "_id": "$username" } 
                        }]

        usernames = Twitt.objects().aggregate(pipeline_user)

        result = []

        if group_by == "location":

            result = self._get_list_score_country(usernames)

        elif  group_by == "lang":
            
            result = self._get_list_score_lang(usernames)
        
        return result