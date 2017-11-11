__author__ = 'Habibd'

import tweepy
from tweepy import OAuthHandler
import MySQLdb
import urllib.request
from urllib.request import urlopen
import re
import sql

global db
db = MySQLdb.connect("localhost", "root", "", "project_repo")

global cursor
cursor = db.cursor()

def main():
    # global db
    # db = MySQLdb.connect("localhost", "root", "", "project_repo")
    # db.set_character_set('utf8')
    #
    # global cursor
    # cursor = db.cursor()

    # Consumer values obtained from twitter application
    consumer_key = '1ztqZ6AdMJIknJ1inb3oEQPhN'
    consumer_secret = 'WgULMxzq8m59BaQkymUImMy9xSZCoPMoLtB3e8Ed6zqRB2ThF7'
    access_token = '452454655-2JCF6Z408sdJxr5YZ0MHAftFOtdGRO0wPQBvRgHG'
    access_secret = '4D2dYtDWysVvyVBztwceLp3LD46jP0MWYP8T73ILCMRE9'

    # Setting up OAth
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    global api
    api = tweepy.API(auth)
    global user
    user = api.me()._json

    add_list = ['RedCloakedGirl', 'OlahFemi', 'Miss_Muo']
    # for i in add_list:
    #     save_user(i)
# 446368986, 209298950
    # save_user('RedCloakedGirl')
    # print(len(add_list))
    # save_user('HabibDee')
    posts = sql.get_posts(owner_id=209298950)
    # # # print(posts)
    # # # print(len(posts))
    for i in range(len(posts)):
        save_post_mentions(posts[i]['post_id'])
    #     save_postrts(posts[i]['post_id'])
    #     save_postfaves(posts[i]['post_id'])

    # save_post_mentions(910110470895529984)
    # save_postrts(910110470895529984)
    # save_postfaves(910110470895529984)

    # print(api.get_user('RedCloakedGirl')._json)
    # save_posts('mtz5prif')
    # 873531625602240512
    # save_all_post_data(896534512896663552)
    # save_postrts(894990263151718400)
    # save_post_mentions(894752080379826182)
    # save_postfaves(894990263151718400)
    # save_posts('ted_lade')
    db.close()


def commit(query):
    try:
        # Execute the SQL command
        cursor.execute(query)
        # Commit your changes in the database
        db.commit()
    except tweepy.TweepError as e:
        print(e.response[0]['code'])
        # Rollback in case there is any error
        db.rollback()


def save_user(name=None):
    if name is None:
        query = "INSERT INTO user(user_id, user_handle, description, location) \
                VALUES ('%d', '%s', '%s', '%s')" % \
               (user['id'], str(user['screen_name']), str(user['description']), str(user['location']))

        commit(query)
        # try:
        #     # Execute the SQL command
        #     cursor.execute(query)
        #     # Commit your changes in the database
        #     db.commit()
        # except:
        #     # Rollback in case there is any error
        #     db.rollback()
    else:
        other_user = api.get_user(name)._json
        query = "INSERT INTO user(user_id, user_handle, description, location) \
                  VALUES('%d', '%s', '%s', '%s')" % \
            (other_user['id'], str(other_user['screen_name']), str(other_user['description']),
             str(other_user['location']))
        commit(query)

        # try:
        #     # Execute the SQL command
        #     cursor.execute(query)
        #     # Commit your changes in the database
        #     db.commit()
        # except:
        #     # Rollback in case there is any error
        #     db.rollback()

    # db.close()




def save_friends(name):
        tweep = api.get_user(name)._json
        for friend in tweepy.Cursor(api.friends,name).items(50):
            query = "INSERT INTO friends(user_id, \
                    friend_id, friend_name) \
                    VALUES ('%d', '%d', '%s' )" % \
                   (tweep['id'], friend._json['id'], str(friend._json['screen_name']))
        commit(query)
        # try:
        #     # Execute the SQL command
        #     cursor.execute(query)
        #     # Commit your changes in the database
        #     db.commit()
        # except:
        #     # Rollback in case there is any error
        #     db.rollback()

    # db.close()

def save_all_post_data(post_id):
    status = api.get_status(post_id)._json
    mentions = status['entities']['user_mentions']
    retweet_count = status['retweet_count']
    fav_count = status['favorite_count']
    try:
        save_single_post(post_id)
        if len(mentions) != 0:
            save_post_mentions(post_id)
        if retweet_count != 0:
            save_postrts(post_id)
        if fav_count:
            save_postfaves(post_id)

    except:
        print("Unable to get this shit done")

def save_single_post(post_id):
    post = api.get_status(post_id)._json
    query = "INSERT INTO posts(post_id, owner_id, message) VALUES ('%d', '%d', '%s')" % \
            (post['id'], post['user']['id'], str(post['text'].replace("'", "\\'")))
    commit(query)
    # try:
    #     cursor.execute(query)
    #     db.commit()
    # except tweepy.TweepError as e:
    #     print(e.response[0]['code'])
    #     db.rollback()

def save_posts(name):
    owner = api.get_user(name)._json
    for tweet in tweepy.Cursor(api.user_timeline, name, include_rts=False).items(50):
        post_query = "INSERT INTO posts(post_id, owner_id, message) VALUES ('%d', '%d', '%s')" %\
                     (tweet._json['id'], owner['id'], str(tweet._json['text'].replace("'", "\\'")))
        commit(post_query)
        # try:
        #     cursor.execute(post_query)
        #     db.commit()
        # except tweepy.TweepError as e:
        #     print(e.response[0]['code'])
        #     db.rollback()

def save_post_mentions(post_id):
    mentions = api.get_status(post_id)._json['entities']['user_mentions']
    if len(mentions) != 0:
        for item in mentions:
            men_query = "INSERT INTO post_mention(post_id, mentionto_id, mentionto_name)\
                          VALUES ('%d', '%d', '%s')" % \
                        (post_id, item['id'], item['name'].replace("_","\_"))
            commit(men_query)
            # try:
            #     cursor.execute(men_query)
            #     db.commit()
            # except tweepy.TweepError as e:
            #         print(e.response[0]['code'])
            #         db.rollback()

    else:
        print("PostID: " + str(post_id) + " has no mentions")


def save_postrts(post_id):
    retweeters = api.retweeters(post_id)
    retweet_count = api.get_status(post_id)._json['retweet_count']
    if retweet_count != 0:
        for retweeter in retweeters:
            rt_query = "INSERT INTO post_rt(post_id, retweetedby_id, retweetedby_name)\
                          VALUES ('%d', '%d', '%s')" % \
                        (post_id, int(api.get_user(retweeter)._json['id']), api.get_user(retweeter)._json['name'])
            commit(rt_query)
            # try:
            #     cursor.execute(rt_query)
            #     db.commit()
            # except tweepy.TweepError as e:
            #         print(e.response[0]['code'])
            #         db.rollback()

    else:
        print("PostID: " + str(post_id) + " has no retweets")

def save_postfaves(post_id):
    likers = get_user_ids_of_post_likes(post_id)
    fav_count = api.get_status(post_id)._json['favorite_count']
    if fav_count != 0:
        for liker in likers:
            fav_query = "INSERT INTO post_fav(post_id, favby_id, favby_name)\
                          VALUES ('%d', '%d', '%s')" % \
                        (post_id, int(api.get_user(liker)._json['id']), api.get_user(liker)._json['name'])
            commit(fav_query)
            # try:
            #     cursor.execute(fav_query)
            #     db.commit()
            # except tweepy.TweepError as e:
            #         print(e.response[0]['code'])
            #         db.rollback()

    else:
        print("PostID: " + str(post_id) + " has no favourites")

def get_user_ids_of_post_likes(post_id):
    try:
        json_data = urlopen('https://twitter.com/i/activity/favorited_popup?id=' + str(post_id)).read()
        data = json_data.decode("utf-8")
        found_ids = re.findall(r'data-user-id=\\"+\d+', data)

        unique_ids = list(set([re.findall(r'\d+', match)[0] for match in found_ids]))
        return unique_ids
    except urllib.error.HTTPError:
        return False


if __name__ == "__main__":
    main()
