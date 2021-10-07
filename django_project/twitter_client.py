import os
import requests
import json


class TwitterClient:
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

    def get_tweet_meta(self, tweet_id):
        # Example return: {'retweet_count': 254, 'reply_count': 164, 'like_count': 4286, 'quote_count': 104} 
        tweet_id = self.parse_tweet_id(tweet_id)
        if tweet_id == -1:
            return 'Tweet id parsing failed'
        url = f'https://api.twitter.com/2/tweets?ids={tweet_id}'
        query_params = {'tweet.fields': 'public_metrics'}
        json_response = self.connect_to_endpoint(url, query_params)
        return json_response['data'][0]['public_metrics']

    def get_tweet(self, tweet_id):
        tweet_id = self.parse_tweet_id(tweet_id)
        if tweet_id == -1:
            return 'Tweet id parsing failed'
        url = f'https://api.twitter.com/2/tweets?ids={tweet_id}'
        query_params = {'tweet.fields': 'author_id'}

        json_response = self.connect_to_endpoint(url, query_params)
        return json_response['data'][0]['text']

    def get_comments(self, tweet_id):
        tweet_id = self.parse_tweet_id(tweet_id)
        if tweet_id == -1:
            return 'Tweet id parsing failed'
        url = f'https://api.twitter.com/2/tweets/search/recent?query=conversation_id:{tweet_id}'
        query_params = {'tweet.fields': 'in_reply_to_user_id'}

        json_response = self.connect_to_endpoint(url, query_params)
        if json_response['meta']['result_count'] == 0:
            return []

        comment_items = json_response['data']
        comments = []
        for item in comment_items:
            comments.append(item['text'])
        return comments

    @staticmethod
    def parse_tweet_id(text):
        try:
            return int(text)
        except ValueError:
            try:
                return int(text.split('/')[-1])
            except ValueError:
                return -1

    def bearer_oauth(self, r):
        r.headers['Authorization'] = f'Bearer {self.bearer_token}'
        r.headers['User-Agent'] = 'v2RecentSearchPython'
        return r

    def connect_to_endpoint(self, url, params):
        response = requests.get(url, auth=self.bearer_oauth, params=params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()
