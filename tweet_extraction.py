import requests
import os
import datetime

key = os.environ.get('TWITTER_API_KEY')
secret = os.environ.get('TWITTER_API_SECRET')
bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')

twitter_users = tuple(['KevinKenson'])

my_username = 'ornelloiannace'

url_me = f'https://api.twitter.com/2/users/by/username/{my_username}'

headers = {
    "Authorization": "Bearer " + bearer_token
}
my_user = requests.get(url=url_me, headers=headers)
print(my_user.status_code)
my_id = my_user.json()['data']['id']

url_users_following = f'https://api.twitter.com/2/users/{my_id}/following'
users_following = requests.get(url=url_users_following, headers=headers)
print(users_following.status_code)

now = datetime.datetime.now()
current_time_format = str(now.date())+"T"+str(now.hour-3)+":"+str(now.minute)+":"+str(now.second)+"Z"

users_following_ids = [user['id'] for user in users_following.json()['data']]
users_following_tweets = {}
for user_id in users_following_ids:
    url_user_following_tweets = f'https://api.twitter.com/2/users/{user_id}/tweets?start_time={current_time_format}'
    users_following_tweets[user_id]=requests.get(url=url_user_following_tweets, headers=headers)
    
print([users_following_tweets[content].json()['data'] for content in users_following_tweets])

print(str(now.date())+"T"+str(now.hour-6)+":"+str(now.minute)+":"+str(now.second)+"Z")