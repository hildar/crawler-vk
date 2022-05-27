# Web crawler for parsing vk.com
# Parse social net vk.com. Get information about posts who liked and reposted this.
# Code name: **BIG BRO**.
# Target: Social research. Research trends.


from time import sleep
import requests
from pymongo import MongoClient


# connect to MongoDB
def client_mongodb(db_name: str, collection_name: str):
    client = MongoClient('mongodb://127.0.0.1:27017')
    data_base = client[db_name]  # db name
    collect_name = data_base[collection_name]  # collection name
    return collect_name


# save users or clubs to MongoDB
def save_to_mongodb(list_to_save_db: list, unique_key: str, db_name: str, collection_name: str):
    collection = client_mongodb(db_name, collection_name)
    count = 0
    for item in list_to_save_db:
        collection.update_one({unique_key: item[unique_key]}, {'$set': item}, upsert=True)
        count += 1
    print(f'Added {count} records. Collection "{collection.name}" has {collection.count_documents({})} items.')


# get posts, likes, comments from API vk.com
def get_data(method, params_method, offset=0, count=100, koeficient=1):
    max_value = 100
    params = {
        # unique token is valid for a day
        'access_token': 'de8f9c35b71563ce39ca12c75301aa7ccdf3ba5ead6bfa15aca87e143da550bfbdee1d1962d4eceda272c',
        'v': 5.101,
        'count': count,
        'offset': offset,
    }
    for key, item in params_method.items():
        params[key] = item
    data = []
    while offset < count:
        params['offset'] = offset
        response = requests.get(f'https://api.vk.com/method/{method}', params=params)
        try:
            response_data = response.json()['response']['items']
            data.extend(response_data)
        except KeyError:
            pass  # KeyError from response (Access is denied)
        offset += max_value * koeficient  # some requests has more than 100 max value
        sleep(0.5)
    if method == 'wall.get':
        print(f'Log: Get info from owner_id: {params["owner_id"]}. He has {len(data)} posts on a wall')
    return data


# web crawler
def parse_vk():
    id_badcomedian = -25557243
    params_badcomedian = {'owner_id': id_badcomedian}
    posts = get_data('wall.get', params_badcomedian, count=3)

    # Get likes and comments. Write this.
    for i, post in enumerate(posts):
        post_owner_id = post['owner_id']
        post_id = post['id']
        # get likes
        params_get_likes = {
            'type': 'post',
            'owner_id': post_owner_id,
            'item_id': post_id
        }
        ids_likes = get_data('likes.getList', params_get_likes, count=300, koeficient=3)
        posts[i]['likes']['ids_likes'] = ids_likes
        # get comments
        params_get_comments = {
            'owner_id': post_owner_id,
            'post_id': post_id,
            'need_likes': 1,
            'preview_length': 0
        }
        comments = get_data('wall.getComments', params_get_comments, count=100)
        posts[i]['comments']['content'] = comments

    badcomedian = {
        'id_club': id_badcomedian,
        'posts': posts
    }
    save_to_mongodb([badcomedian], 'id_club', 'vk', 'clubs')

    # Get posts who is liked badcomedian posts
    users = []
    ids_likes = []
    for post in posts:
        ids = post['likes']['ids_likes']
        ids_likes.extend(ids)
    ids_likes = set(ids_likes)
    for who in ids_likes:
        params_who = {'owner_id': who}
        who_posts = get_data('wall.get', params_who)
        users.append({
            'id_user': who,
            'posts': who_posts
        })
    save_to_mongodb(users, 'id_user', 'vk', 'users')


# add users to DB who has reposted BadComedian
def add_repost_users():
    clubs = client_mongodb('vk', 'clubs')
    cursor = clubs.find({})
    bad_posts = []

    for item in cursor:
        bad_posts = item['posts']
        break
    users = client_mongodb('vk', 'users')

    for i, post in enumerate(bad_posts):
        post_id = post['id']
        post_owner_id = post['owner_id']
        # Get all users who is liked post
        ids_likes = post['likes']['ids_likes']
        cursor = users.find({'id_user': {'$in': ids_likes}})
        repost_users = []
        for item in cursor:
            user_id = item['id_user']
            user_posts = item['posts']
            # Check even repost on a wall user
            for user_post in user_posts:
                # Check and add reposted user
                try:
                    repost_own = user_post['copy_history'][0]['owner_id']
                    repost_id = user_post['copy_history'][0]['id']
                    if repost_own == post_owner_id and repost_id == post_id:
                        repost_users.append(user_id)
                except KeyError:
                    pass  # KeyError (Not posts this user)
        bad_posts[i]['reposts']['ids_reposts'] = repost_users
        print(f'Log: The post "wall{post_owner_id}_{post_id}" is reposted next users: {repost_users}')

    id_badcomedian = -25557243
    badcomedian = {
        'id_club': id_badcomedian,
        'posts': bad_posts
    }
    save_to_mongodb([badcomedian], 'id_club', 'vk', 'clubs')


# parse
parse_vk()
print()
add_repost_users()
