__author__ = 'Habibd'
import sql
from iris_trust import Graph
global g
g = Graph()


def main():
    # 0
    setup_iris()
    # print(g.vertices['mtz5prif'].get_predecessor())
    print(g.vertices['HabibDee'].get_relationship_type(g.vertices['Oluso_LA']))
    # print()
    # print(get_relationship_type(3347256251,293779614))


def setup_iris():
    # g = Graph()
    # g = iris_trust.Graph()
    users = sql.get_users()
    # print(users)
    if len(users) != 0:
        for user in users:
            friends = sql.get_friends(user['user_id'])
            if len(friends) != 0:
                for friend in friends:
                    relationship_type = get_relationship_type(user['user_id'], friend['friend_id'])
                    interactions = process_interactions(user['user_id'], friend['friend_id'])

                    edge_dict = {
                        'first_node': user['user_handle'],
                        'first_id': user['user_id'],
                        'second_node': friend['friend_name'],
                        'second_id': friend['friend_id'],
                        'interactions': interactions,
                        'relationship_type': relationship_type,

                    }
                    g.add_edge(edge_dict)


def get_relationship_type(user, friend):
    # Check frequency of interactions to determine relationship type.
    total_interactions = 0
    friends = sql.get_friends(user)
    # Get total number of interactions
    for i in friends:
        temp_total = len(sql.get_mentions(user, i['friend_id'])) + len(sql.get_retweets(i['friend_id'], user))\
                     + len(sql.get_faves(i['friend_id'], user))

        total_interactions += temp_total

    mentions = len(sql.get_mentions(user, friend))
    retweets = len(sql.get_retweets(friend, user))
    likes = len(sql.get_faves(friend, user))
    total = mentions + likes + retweets

    # Set interaction frequency value as number of interactions
    #  between user and friend / total number of interactions
    if total_interactions != 0:
        rel_check = total / total_interactions
    else:
        rel_check = 0
    # Set relationship type with neighbour
    if rel_check >= 0.75:
        relationship_type = 'GRADE A'
    elif 0.5 <= rel_check < 0.75:
        relationship_type = 'GRADE B'
    elif 0.25 <= rel_check < 0.5:
        relationship_type = 'GRADE C'
    elif 0.1 <= rel_check < 0.25:
        relationship_type = 'GRADE D'
    else:
        relationship_type = 'GRADE E'

    return relationship_type


def process_interactions(user, friend):
    mentions = sql.get_mentions(user, friend)
    retweets = sql.get_retweets(friend, user)
    likes = sql.get_faves(friend, user)
    return dict(mentions=mentions, retweets=retweets, likes=likes)


if __name__ == "__main__":
    main()