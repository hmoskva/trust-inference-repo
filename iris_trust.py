__author__ = 'Habibd'
import sql
import math
import classification
global g


class Node:

    def __init__(self, name, idd):
        # Node Name.
        self.name = name

        # Node ID
        self.idd = idd

        # List of nodes adjacent to node.
        self.neighbours = {}

        # Dict of node's relationships with its neighbours.
        self.relationships = {}

        # List of nodes that have self as successor.
        self.predecessors = []

        # Dict of node interactions
        self.interactions = {}

    def __str__(self):
        return str(self.name)

    def add_neighbour(self, neighbour, weight=None):
        # add neighbour to neighbour dictionary and add self to neighbours predecessor list
        self.neighbours[neighbour] = weight

        neighbour.predecessors.append(self)

    def add_relationship(self, neighbour, relationship_type):
        self.relationships[neighbour] = relationship_type

    def add_interactions(self, interactions, neighbour):
        # set a nodes interactions with another node
        self.interactions[neighbour] = interactions

    def get_neighbours(self):
        return self.neighbours.keys()

    def get_predecessor(self):
        if len(self.predecessors) != 0:
            return self.predecessors
        else:
            return None

    def get_weight(self, neighbour):
        if neighbour in self.get_neighbours():
            return self.neighbours[neighbour]
        else:
            return None

    def set_weight(self, neighbour, weight):
        self.neighbours[neighbour] = weight

    def get_relationship_type(self, neighbour):
        if neighbour in self.get_neighbours():
            return self.relationships[neighbour]
        else:
            return None

    def get_interactions(self, neighbour):
        return self.interactions.get(neighbour)


class Graph:
    def __init__(self):
        self.vertices = {}

    def __iter__(self):
        return iter(self.vertices.values())

    def add_vertex(self, node, idd=None):
        # Pass a new node and cast to type Node, name of node class
        new_vertex = Node(node, idd)
        self.vertices[node] = new_vertex

    def get_vertex(self, node):
        if node in self.vertices:
            return self.vertices[node]
        else:
            return None

    def add_edge(self, edge_dict, weight=None):
        # Here, we do the bulk of the graph creation.
        first_node = edge_dict['first_node']
        second_node = edge_dict['second_node']
        interactions = edge_dict['interactions']

        if first_node not in self.vertices:
            self.add_vertex(first_node, edge_dict['first_id'])
        if second_node not in self.vertices:
            self.add_vertex(second_node, edge_dict['second_id'])

        # Append s_node to f_nodes neighbour list
        self.vertices[first_node].add_neighbour(self.vertices[second_node], weight)

        # Add the relationship type between fnode and s_node
        self.vertices[first_node].add_relationship(self.vertices[second_node], edge_dict['relationship_type'])

        # Add Interaction list passed to list of fnodes interactions towards snode
        self.vertices[first_node].add_interactions(interactions, self.vertices[second_node])

    def get_vertices(self):
        return self.vertices.keys()

    # @staticmethod
    # def main():
    #
    #     gr = Graph()
    #     tr = Trust()
    #     import graph_setup
    #     graph_setup.setup_iris()
    #     # print(graph_setup.g.vertices['mtz5prif'].get_predecessor())
    #     # print(tr.check2(graph_setup.g.vertices['Folabz_']))
    #     # print(tr.iris(graph_setup.g.vertices['mtz5prif'], graph_setup.g.vertices['HabibDee']))
    #     # gr.add_edge('Habib', 'Damola', interactions=['Like', 'Comment', 'Tag'], relationship_type= 'close relationship',
    #     #            simcheck_a=['sports', 'csc'], simcheck_b=['csc', 'sports', 'parties'])
    #     # gr.add_edge('Habib', 'Dapo', interactions=['Like', 'Comment', 'Tag'], relationship_type= 'close relationship',
    #     #            simcheck_a=['sports', 'csc'], simcheck_b=['csc', 'sports', 'alcohol'])
    #     # gr.add_edge('Damola', 'Mo', interactions=['Comment', 'Tag'], relationship_type= 'close relationship'
    #     #            , simcheck_b=['csc', 'games'])
    #     # #
    #     # # print(tr.tidal(gr.vertices['Habib'], gr.vertices['Mo']))
    #     print(tr.interaction_trust(gr.vertices['HabibDee'], gr.vertices['mtz5prif']))
        # print(g.iris(g.vertices['Damola'], g.vertices['Mo']))
        # print(g.vertices['Habib'].get_relationship_type(g.vertices['Dapo']))
        # print(g.similarity_trust(g.vertices['Habib'], g.vertices['Damola']))


class Trust:

    def relationship_trust(self, source, neighbour):
        if neighbour in source.get_neighbours():
            relationship_type = source.get_relationship_type(neighbour).upper()
            if relationship_type == 'GRADE A':
                r_trust = 1
            elif relationship_type == 'GRADE B':
                r_trust = 0.75
            elif relationship_type == 'GRADE C':
                r_trust = 0.5
            elif relationship_type == 'GRADE D':
                r_trust = 0.25
            else:
                r_trust = 0

            return r_trust

        else:
            return None

    def interaction_trust(self, source, neighbour):
        itr = 0
        if neighbour in source.get_neighbours():
            pos = 0
            list_of_interactions = source.get_interactions(neighbour)
            # Unpack interaction dict
            mentions = list_of_interactions['mentions']
            retweets = list_of_interactions['retweets']
            likes = list_of_interactions['likes']

            tot_mentions = sql.get_num_all_interactions_by_type(source.idd, 'mention',
                                                                neighbour.idd)
            tot_rts = sql.get_num_all_interactions_by_type(source.idd, 'retweet',
                                                           neighbour.idd)
            tot_likes = sql.get_num_all_interactions_by_type(source.idd, 'like',
                                                             neighbour.idd)
            print(mentions)
            pos_mentions = []
            for m in mentions:
                if m in tot_mentions:
                    pos_mentions.append(m)
                # res = classification.sentiment(m[1].strip('@'))
                # if res[0] == 'pos' and res[1] >= 0.6:
                #     pos_mentions.append(m)

            compt_list = [(pos_mentions, len(tot_mentions)), (retweets, tot_rts), (likes, tot_likes)]

            for i in compt_list:
                if i[1] != 0:
                    itr += ((1/3)*(len(i[0])/i[1]))
        return itr

            # do 3 more checks
        #     if tot_mentions == 0 and tot_rts != 0 and tot_likes != 0:
        #         i_trust = (0.7 * (len(likes) / tot_likes)) + (0.3 * (len(retweets) / tot_rts))
        #     elif tot_mentions != 0 and tot_rts == 0 and tot_likes != 0:
        #         i_trust = (0.6 * (len(likes) / tot_likes)) + (0.4 * (len(mentions) / tot_mentions))
        #     elif tot_mentions != 0 and tot_rts != 0 and tot_likes == 0:
        #         i_trust = (0.4 * (len(retweets) / tot_rts)) + (0.6 * (len(mentions) / tot_mentions))
        #     else:
        #         i_trust = (0.5 * (len(likes)/tot_likes)) + (0.2 *(len(retweets)/tot_rts)) + (0.3*(len(pos_mentions)/tot_mentions))
        # return i_trust



            # Looping through interactions by type
        #     if len(likes) != 0:
        #         for i in range(len(likes)):
        #             # Assume all interactions of type Like are positive
        #             pos += 1
        #     if len(mentions) != 0:
        #         for entry in mentions:
        #             # Compute satisfaction criteria: 1 + Log(r/n)
        #             # r = no of reactions, n = number of friends. Log for limiting.
        #             no_reactions = sql.get_no_reactions(post_id=entry[0])
        #             if no_reactions != 0 and len(source.get_neighbours()) != 0:
        #                 sat_val = 1 + math.log((no_reactions/len(source.get_neighbours())))
        #                 if sat_val >= 0.5:
        #                     pos += 1
        #
        #     if len(retweets) != 0:
        #         for i in range(len(retweets)):
        #             # Assume all interactions of type retweet are positive
        #             pos += 1
        #
        #     tot_interactions = len(mentions) + len(retweets) + len(likes)
        #     print('total--> '+str(tot_interactions)+" "+source.name+"-->"+neighbour.name)
        #     neg = tot_interactions - pos
        #     if pos > neg:
        #         return 1 - (neg / pos)
        #     else:
        #         return 0
        # else:
        #     return None

    def similarity_trust(self, source, neighbour):
        # Using mutual friends to determine similarity
        source_friends = source.get_neighbours()
        neighbour_friends = neighbour.get_neighbours()
        if neighbour in source.get_neighbours():
            mutual_friends = [friend for friend in source_friends if friend in neighbour_friends]
            if len(mutual_friends) != 0:
                return len(mutual_friends) / len(source_friends)
            else:
                return 0
        else:
            return None

    def iris(self, source, neighbour):
        t = Trust()
        if neighbour in source.get_neighbours():
            r_trust = t.relationship_trust(source, neighbour)

            i_trust = t.interaction_trust(source, neighbour)
            s_trust = t.similarity_trust(source, neighbour)

            print("RelationshipTrust-->"+str(r_trust))
            print("InteractionTrust-->"+str(i_trust))
            print("simTrust-->"+str(s_trust))

            if r_trust is not None and s_trust is not None and \
                    i_trust is not None:
                trust = 1/3 * (abs(r_trust) + abs(s_trust) + abs(i_trust))
                source.set_weight(neighbour, trust)
                return trust

            else:
                return None

    def get_threshold(self, source, sink):
        t = Trust()
        queue = []
        visited = [source]
        if sink in source.get_neighbours():
            # If sink is a neighbour, calculate direct trust.
            trust = t.iris(source, sink)
            return trust
        else:
            for node in source.get_neighbours():
                # Rate the node.
                if t.iris(source, node) is not None:
                    node.rating = t.iris(source, node)
                    queue.append(node)
                else:
                    node.rating = 0
                    queue.append(node)

            while len(queue) != 0:
                current_node = queue.pop(0)
                if current_node == sink:
                    break

                # Check to see if current node isn't amongst source's neighbours.
                # If it is, its already been rated.
                if source in current_node.get_predecessor():
                    visited.append(current_node)
                    if len(current_node.get_neighbours()) != 0:
                        for child in current_node.get_neighbours():
                            if child not in visited and child not in queue:
                                queue.append(child)

                else:
                    if len(current_node.get_predecessor()) > 1:
                        rating_list = []
                        for pred in current_node.get_predecessor():
                            # Check if predecessor has already been rated.
                            # If it has, use rating to determine current node's rating
                            if hasattr(pred, 'rating'):
                                rating_list.append(min(pred.rating, t.iris(pred, current_node)))

                            else:
                                # If predecessor has no rating use, direct trust to ...
                                # determine current nodes rating
                                rating_list.append(t.iris(pred, current_node))

                        current_node.rating = max(rating_list)
                    else:
                        for pred in current_node.get_predecessor():
                            if pred.rating is not None:
                                current_node.rating = min(pred.rating, t.iris(pred, current_node))
                            else:
                                current_node.rating = t.iris(pred, current_node)

                    visited.append(current_node)

                    if len(current_node.get_neighbours()) != 0:
                        for child in current_node.get_neighbours():
                            if child not in visited and child not in queue:
                                queue.append(child)

        sink_predecessors_ratings = []
        for parent in sink.get_predecessor():
            if hasattr(parent, 'rating'):
                sink_predecessors_ratings.append(parent.rating)
            else:
                sink_predecessors_ratings.append(t.iris(parent, sink))

        threshold = max(sink_predecessors_ratings)
        return threshold

    def tidal(self,source, sink):
        t = Trust()

        queue = []
        visited = []

        # To be used when selecting a path to follow amongst traversable paths.
        selected_neighbours = []
        if t.check(source, sink):

            # Return direct trust if sink and source are connected.
            if sink in source.get_neighbours():
                return t.iris(source, sink)

            # Obtain threshold to be used to filter nodes to traverse.
            threshold = t.get_threshold(source, sink)

            # Initialize computation variables
            numerator = 0.0
            denominator = 0.0
            trust_computation = 1.0

            visited.append(source)
            while len(queue) == 0:
                for neighbour in source.get_neighbours():
                    # Adding nodes that have sink in their path and meet threshold requirements ...
                    # amongst sources neighbours to queue for part dfs implementation.
                    if t.check(neighbour, sink):
                        if neighbour.rating >= threshold:
                            print(neighbour.name + " meets the threshold requirements so will be processed")
                            print("***************************************************************************")
                            queue.append(neighbour)

                # Adaptation of mine...
                # If queue is empty (none of source's neighbours meets threshold),
                # half the threshold and test condition again.
                # Important because we must have at least one path to follow.
                if len(queue) == 0:
                    threshold /= 2

            while len(queue) != 0:
                # Initialize a list to store path traversed.
                temp_path = [source]
                sink_found = False

                # Obtain item from queue for processing
                current = queue.pop(0)

                # Store current node in path list
                temp_path.append(current)

                visited.append(current)
                # If sink not in current node's path, break from loop
                if current == sink:
                    break

                else:
                    # While sink hasn't been found, keep performing operations below.
                    while not sink_found:
                        # Check if current has neighbours.
                        if len(current.get_neighbours()) != 0:
                            # Check if sink is part of current node's neighbours.
                            if sink in current.get_neighbours():
                                # include sink in path list.
                                temp_path.append(sink)

                                counter = len(temp_path)-1
                                for i in range(counter):
                                    # Tij*Tjk Computation using nodes in path list.
                                    trust_computation *= t.iris(temp_path[i], temp_path[i+1])

                                # Add current path's Tij*Tjk to numerator summation.
                                numerator += trust_computation

                                # Add current path's Tij to denominator summation.
                                denominator += t.iris(source, temp_path[1])

                                print("Summation(Tij*Tjk):-->" + str(numerator))
                                print("Summation(Tij):-->" + str(denominator))
                                sink_found = True

                                # Clear path list for next node to use.
                                temp_path.clear()
                            else:
                                # List to store current node's trust towards its neighbours.
                                # This is to determine path to follow.
                                trusts_at_level = []

                                # Checking if current nodes neighbours meet threshold requirements
                                for neighbour in current.get_neighbours():
                                    # print(neighbour.name)
                                    if t.check(neighbour, sink):
                                        if neighbour not in visited and hasattr(neighbour, 'rating') and neighbour.rating >= threshold:
                                            trusts_at_level.append(t.iris(current, neighbour))

                                if len(trusts_at_level) != 0:

                                    for neighbour in current.get_neighbours():
                                        # Checking for nodes with highest trust rating towards sink.
                                        if current.neighbours[neighbour] == max(trusts_at_level):
                                            selected_neighbours.append(neighbour)

                                    # Add node to path list.
                                    temp_path.append(selected_neighbours[0])
                                    current = selected_neighbours[0]
                                    selected_neighbours.clear()
                                else:
                                    break

                        else:
                            break

            if denominator != 0:
                return numerator/denominator
            else:
                return 0.0
        else:
            return 'No path connecting selected nodes'

    def check(self, start, goal):
        # A DFS to check if goal is in path
        stack = []
        visited = []
        stack.append(start)
        while len(stack) != 0:
            current = stack.pop()
            visited.append(current)
            if current == goal:
                break
            if len(current.get_neighbours()) != 0:
                for neighbour in current.get_neighbours():
                    if neighbour not in visited and neighbour not in stack:
                        stack.append(neighbour)

        if goal in visited:
            message = True
        else:
            message = False

        return message


if __name__ == "__main__":
    gr = Graph()
    tr = Trust()
    import graph_setup
    graph_setup.setup_iris()
    print(gr.vertices)
