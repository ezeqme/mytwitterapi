#!/usr/bin/python3
import fire
import json
import requests
import datetime
import logging
import os.path

logging.basicConfig(level=logging.INFO)

class TwitterApi():
    
    _endpoint_twitter_search="https://api.twitter.com/2/tweets/search/recent"

    def __init__(self, bearer_token):
        
        self._headers = {"Authorization": "Bearer %s" % bearer_token}

    def search_twittes(self, hashtag, max_results='100'):

        logging.info("Buscando tweets pela tag: %s" % hashtag)

        params = {"query": "%s -is:retweet" % hashtag, "expansions": "author_id", "user.fields": "name,username,location,public_metrics", "tweet.fields": "created_at,entities,lang", "max_results": max_results}

        result = None

        try:

            r = requests.get(self._endpoint_twitter_search, headers=self._headers, params=params)

            if r.status_code == 200:

                result = r.json()

            elif r.status_code == 401:

                logging.info("Access denied: %s" % r.json())

                exit(0)

            else:

                logging.info("Erro: status: %s - %s" % (r.status_code, r.json()))

                exit(0)                

        except ValueError as e:
            logging.info("Invalid Bearer Token:  %s" % e)
            exit(0)

        return result
        

class TwittCtl():

    def __init__(self):

        self._endpoint_twitter_api = "http://localhost/twitter/api/v1/publish/posts"
        self._headers = { "Content-Type": "application/json" }

    def _get_user_info(self, list_users, author_id):

        for user in list_users:

            if user['id']==author_id:

                return user

    def _publish(self, list_tweets):

        logging.info("Publicando tweets...")

        try:

            r = requests.post(self._endpoint_twitter_api, headers=self._headers, data=json.dumps(list_tweets))

            if r.status_code == 200:

                logging.info("Sucesso ao publicar %s tweets" % len(list_tweets))

        except Exception as e:

            logging.error("Erro ao publicar tweet: %s" % e)



    def search(self, token, tags, limit=100):

        self._api = TwitterApi(token)
        
        list_tags = tags.split(',')

        for tag in list_tags:

            result = self._api.search_twittes(tag, max_results=limit)

            tweets_list = []

            if result["meta"]['result_count'] == 0 :

                logging.warning("Busca para tag %s retornou %s tweets." % (tag, result["meta"]['result_count']))

            else:

                logging.info("Busca para tag %s retornou %s tweets." % (tag, result["meta"]['result_count']))

                for data in result['data']:

                    user = self._get_user_info(result['includes']['users'], data['author_id'])

                    location = ""

                    if 'location' in user:

                        location = user['location']

                    else:

                        location = 'undefined'

                    post_date = datetime.datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')

                    post_hour = post_date.hour
                    
                    twitte = { 'id': data['id'],
                                'text': data['text'],
                                'created_at': data['created_at'],
                                'post_hour': post_hour,
                                'hashtag': tag,
                                'lang': data['lang'], 
                                'author_id': data['author_id'], 
                                'username': user['username'], 
                                'name': user['name'], 
                                'location': location,
                                'followers_count': user['public_metrics']['followers_count']
                    }

                    tweets_list.append(twitte)

                self._publish(tweets_list)

if __name__=='__main__':  

    fire.Fire(TwittCtl())

   
