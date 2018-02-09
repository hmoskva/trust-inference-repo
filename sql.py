__author__ = 'Habibd'
import MySQLdb
import classification

db = MySQLdb.connect("localhost", "root", "", "project_repo")
cursor = db.cursor()


def main():

    # print(get_faves(452454655, 3347256251))
    # print(get_no_reactions(875859459674976257))
    print(get_num_all_interactions_by_type(452454655, 'mention', 3347256251))
    # print(get_friends('452454655'))
    # print(test('HabibDee'))
    # db.close()

def get_num_all_interactions_by_type(user, type, friend=None):
    if type not in ['like', 'mention', 'retweet']:
        raise Exception('Invalid type')

    ufriends = get_friends(user)
    ffriends = get_friends(friend)

    if type == 'mention':
        c = 0
        umentions = [get_mentions(user, f['friend_id']) for f in ufriends]
        pos_mentions = []
        for li in umentions:
            for i in li:
                res = classification.sentiment(i[1].strip('@'))
                if res[0] == 'pos' and res[1] >= 0.6:
                    pos_mentions.append(li)

        # for m in pos_mentions:
        #     c += len(m)
        return pos_mentions
    elif type == 'like':
        c = 0
        flikes = [get_faves(friend, f['friend_id']) for f in ffriends]
        for m in flikes:
            c += len(m)
        return c
    c = 0
    frts = [get_retweets(friend, f['friend_id']) for f in ffriends]
    for m in frts:
        c += len(m)
    return c

def get_users(id=None):
    if id:
        query = "SELECT * FROM user  WHERE user_id = %s" % id
    else:
        query = "SELECT * FROM user"

    try:
        # Execute the SQL command
            cursor.execute(query)
            results = cursor.fetchall()
            users = [dict(user_id=row[0], user_handle=row[1], location=row[3]) for row in results]
            return users
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))


def get_friends(user_id, friend_id=None):
    if friend_id:
        query = "SELECT * FROM friends WHERE user_id = " + user_id + " AND friend_id = " + friend_id
    else:
        query = "SELECT * FROM friends WHERE user_id = " + str(user_id)

    try:
        # Execute the SQL command
            cursor.execute(query)
            results = cursor.fetchall()
            friends = [dict(user_id=row[1], friend_id=row[2], friend_name=row[3]) for row in results]
            return friends

    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))


def get_posts(owner_id=None, post_id=None):
    if owner_id and not post_id:
        query = "SELECT * FROM posts  WHERE owner_id = %s" % owner_id
    elif post_id and not owner_id:
        query = "SELECT * FROM posts  WHERE post_id = " + str(post_id)
    else:
        query = "SELECT * FROM posts"

    try:
        # Execute the SQL command
            cursor.execute(query)
            results = cursor.fetchall()
            posts = [dict(post_id=row[0], owner_id=row[1], message=row[2]) for row in results]
            return posts
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))


def get_mentions(user_id, friend_id):

    # Return all posts by user that have friend mentioned in them.
    query = "SELECT post_mention.post_id, posts.message FROM post_mention JOIN posts ON " \
            "posts.post_id = post_mention.post_id WHERE " \
            "posts.owner_id = " + str(user_id) + " AND post_mention.mentionto_id = " +str(friend_id)
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))


def get_retweets(owner_id, friend_id):

    # Return all posts by owner that have been retweeted by friend.
    query = "SELECT post_rt.post_id, posts.message FROM post_rt JOIN posts ON " \
            "posts.post_id = post_rt.post_id WHERE " \
            "posts.owner_id = " + str(owner_id) + " AND post_rt.retweetedby_id = " + str(friend_id)

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))


def get_faves(owner_id, friend_id):
    # Return all posts by owner that have been liked by friend
    query = "SELECT post_fav.post_id, posts.message FROM post_fav JOIN posts ON " \
            "posts.post_id = post_fav.post_id WHERE " \
            "posts.owner_id = " + str(owner_id) + " AND post_fav.favby_id = " + str(friend_id)

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))


def get_no_reactions(post_id):
    # Return the number of reactions for each post
    query = "SELECT count(*) as num_1 FROM post_fav WHERE post_id = " + str(post_id)
    query2 = "SELECT count(*) as num_2 FROM post_rt WHERE post_id = " + str(post_id)
    try:
        cursor.execute(query)
        results1 = cursor.fetchall()
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))

    try:
        cursor.execute(query2)
        results2 = cursor.fetchall()
    except MySQLdb.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))

    no_reactions = results1[0][0] + results2[0][0]
    return no_reactions


if __name__ == "__main__":
    main()
