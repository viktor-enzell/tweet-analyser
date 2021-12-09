import os
import requests


class TwitterClient:
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

    def get_user_id(self, username):
        url = f'https://api.twitter.com/2/users/by/username/{username}'
        query_params = {'tweet.fields': 'public_metrics'}
        json_response = self.connect_to_endpoint(url, query_params)
        return json_response["data"]["id"]
    
    def get_user_tweets(self, username):
        userid = self.get_user_id(username)
        """
        Returns list of objects like below
        {'id': '1468928909626515460', 
        'public_metrics': {'retweet_count': 0, 'reply_count': 0, 'like_count': 0, 'quote_count': 0},
        'text': '@maybe__pirog Hahahahhaa'}
        """
        url = f'https://api.twitter.com/2/users/{userid}/tweets'
        query_params = {
            'tweet.fields': 'public_metrics', 
            'exclude': 'retweets,replies'}

        json_response = self.connect_to_endpoint(url, query_params)
        if not json_response["meta"]["result_count"] > 0:
            print("Not enough tweets from provided user")
            return []
        return json_response["data"]

    def get_tweet(self, tweet_id):
        url = f'https://api.twitter.com/2/tweets?ids={tweet_id}'
        query_params = {'tweet.fields': 'public_metrics', 
                        "user.fields": 'name,username',
                        "expansions": 'entities.mentions.username,author_id'}

        json_response = self.connect_to_endpoint(url, query_params)
        return {
            "username": json_response['includes']['users'][0]["username"],
            "name": json_response['includes']['users'][0]["name"],
            "text":json_response['data'][0]['text'],
            "meta":json_response['data'][0]['public_metrics']
        }

    def get_comments(self, tweet_id):
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

    # scale of 0-2 of meta_data sentiment. 0 is not positive, 2 is positive
    def how_good(self,meta_data):
        count = 0
        retweet_count = meta_data['retweet_count']
        like_count = meta_data['like_count']
        reply_count = meta_data['reply_count']
        quote_count = meta_data['quote_count']

        if retweet_count > reply_count:
            count = count + 1
        if quote_count > reply_count:
            count = count + 1
        return count

    @staticmethod
    def parse_id_or_username(text):
        return text.split('/')[-1]

    def bearer_oauth(self, r):
        r.headers['Authorization'] = f'Bearer {self.bearer_token}'
        r.headers['User-Agent'] = 'v2RecentSearchPython'
        return r

    def connect_to_endpoint(self, url, params):
        response = requests.get(url, auth=self.bearer_oauth, params=params)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()
