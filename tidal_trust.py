__author__ = 'Habibd'
from .iris_trust import Node, Graph
from .iris_trust import Trust as i_Trust



# class Node:
#     def __init__(self, name, idd):
#         # Node Name.
#         self.name = name
#
#         # Node ID
#         self.idd = idd
#
#         # List of nodes adjacent to node.
#         self.neighbours = {}
#
#         # Dict of node's relationships with its neighbours.
#         self.relationships = {}
#
#         # List of nodes that have self as successor.
#         self.predecessors = []
#
#         # Dict of node interactions
#         self.interactions = {}
#
#     def __str__(self):
#         return str(self.name)
#
#     def __repr__(self):
#         return self.__str__()
#
#     def get_rating(self):
#         return str(self.rating)
#
#     def get_name(self):
#         return self.name
#
#     def change_rating(self, value):
#         self.rating = value
#
# # Set the weight
#     def add_neighbour(self, neighbour, weight=None):
#         # add neighbour to neighbour dictionary and add self to neighbours predecessor list
#         self.neighbours[neighbour] = weight
#         neighbour.predecessors.append(self)
#
#     def get_neighbours(self):
#         return self.neighbours.keys()
#
#     def set_weight(self, neighbour, weight):
#         self.neighbours[neighbour] = weight
#
#     def get_weight(self, neighbour):
#         if neighbour in self.get_neighbours():
#             return self.neighbours[neighbour]
#         else:
#             return None
#
#     def set_interaction(self, interaction, neighbour):
#         # set a nodes interactions with another node
#         temp = interaction
#         self.interactions[neighbour] = temp
#
#     def get_interactions(self, neighbour):
#         return self.interactions.get(neighbour)
#
#     def get_predecessor(self):
#         # Return a node's predecessor list
#         if self.predecessors.__len__() != 0:
#             return self.predecessors
#         else:
#             return None
#
#
# class Graph:
#     def __init__(self):
#         self.vertices = {}
#
#     # Here we iterate over all the node objects in the graph
#     def __iter__(self):
#         return iter(self.vertices.values())
#
#     # Adding new nodes to the graph
#     def add_vertex(self, node):
#         # Pass a new node and cast to type Node, name of node class
#         new_vertex = Node(node)
#         self.vertices[node] = new_vertex
#
#     def get_vertex(self, node):
#         if node in self.vertices:
#             return self.vertices[node]
#         else:
#             return None
#
#     def add_edge(self, f_node, s_node, weight=None, interactions=None):
#         # Here, we do the bulk of the graph creation.
#         if f_node not in self.vertices:
#             self.add_vertex(f_node)
#         if s_node not in self.vertices:
#             self.add_vertex(s_node)
#
#         # Append s_node to f_nodes neighbour list
#         self.vertices[f_node].add_neighbour(self.vertices[s_node], weight)
#         # Add Interaction list passed to list of fnodes interactions towards snode
#         self.vertices[f_node].set_interaction(interactions, self.vertices[s_node])
#
#     def get_vertices(self):
#         return self.vertices.keys()


def main():
    g = Graph()
    trust = Trust()
    from . import graph_setup
    graph_setup.setup_iris()
    print(trust.tidal(graph_setup.g.vertices['HabibDee'], graph_setup.g.vertices['iiv_lyn']))
    # print(trust.direct_trust(graph_setup.g.vertices['HabibDee'], graph_setup.g.vertices['iiv_lyn']))



class Trust:
    def direct_trust(self, node, neighbour):
        numerator = 0.0
        if neighbour in node.get_neighbours():
            list_of_interactions = node.get_interactions(neighbour)
            mentions = list_of_interactions['mentions']
            retweets = list_of_interactions['retweets']
            likes = list_of_interactions['likes']
            # print(list_of_interactions)
            # Normalize values to range [0,1] by dividing len(interactions) by 20 and reducing weights by /10
            calc = (len(mentions)/20 * 1.05) + (len(retweets)/20 * 0.525) + (len(likes)/20 * 0.25)
            numerator += calc
            if len(mentions) != 0 and len(retweets) != 0 and len(likes) != 0:
                weight_sum = 1.05 + 0.525 + 0.25
                trust = numerator / weight_sum
                node.set_weight(neighbour, trust)
                return trust
            elif len(mentions) == 0 and len(retweets) != 0 and len(likes) != 0:
                weight_sum = 0.525 + 0.25
                trust = numerator / weight_sum
                node.set_weight(neighbour, trust)
                return trust
            elif len(mentions) != 0 and len(retweets) != 0 and len(likes) == 0:
                weight_sum = 1.05 + 0.525
                trust = numerator / weight_sum
                node.set_weight(neighbour, trust)
                return trust
            elif len(mentions) != 0 and len(retweets) == 0 and len(likes) == 0:
                weight_sum = 1.05
                trust = numerator / weight_sum
                node.set_weight(neighbour, trust)
                return trust
            elif len(mentions) == 0 and len(retweets) == 0 and len(likes) == 0:
                node.set_weight(neighbour, 0)
                return 0
            elif len(mentions) == 0 and len(retweets) != 0 and len(likes) == 0:
                weight_sum = 0.525
                trust = numerator / weight_sum
                node.set_weight(neighbour, trust)
                return trust
            elif len(mentions) == 0 and len(retweets) == 0 and len(likes) != 0:
                weight_sum = 0.25
                trust = numerator / weight_sum
                node.set_weight(neighbour, trust)
                return trust
        else:
            return 0.0

    def get_threshold(self, source, sink):
        t = Trust()
        queue = []
        visited = [source]
        if sink in source.get_neighbours():
            # If sink is a neighbour, calculate direct trust.
            trust = t.direct_trust(source, sink)
            return trust
        else:
            for node in source.get_neighbours():
                # Rate the node.
                if t.direct_trust(source, node):
                    node.rating = t.direct_trust(source, node)
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
                                rating_list.append(min(pred.rating, t.direct_trust(pred, current_node)))

                            else:
                                # If predecessor has no rating use, direct trust to ...
                                # determine current nodes rating
                                rating_list.append(t.direct_trust(pred, current_node))

                        current_node.rating = max(rating_list)
                    else:
                        for pred in current_node.get_predecessor():
                            if pred.rating is not None:
                                current_node.rating = min(pred.rating, t.direct_trust(pred, current_node))
                            else:
                                current_node.rating = t.direct_trust(pred, current_node)

                    visited.append(current_node)

                    if len(current_node.get_neighbours()) != 0:
                        for child in current_node.get_neighbours():
                            if child not in visited and child not in queue:
                                queue.append(child)

        sink_predecessors_ratings = []
        for parent in sink.get_predecessor():
            sink_predecessors_ratings.append(parent.rating)

        threshold = max(sink_predecessors_ratings)
        return threshold

    def tidal(self,source, sink):
        t = Trust()

        queue = []
        visited = []

        # To be used when selecting a path to follow amongst traversable paths.
        selected_neighbours = []
        if i_Trust.check(self, start=source, goal=sink):

            # Return direct trust if sink and source are connected.
            if sink in source.get_neighbours():
                return t.direct_trust(source, sink)

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
                    if i_Trust.check(self, start=neighbour, goal=sink):
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
                                    trust_computation *= t.direct_trust(temp_path[i], temp_path[i+1])

                                # Add current path's Tij*Tjk to numerator summation.
                                numerator += trust_computation

                                # Add current path's Tij to denominator summation.
                                denominator += t.direct_trust(source, temp_path[1])

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
                                    if i_Trust.check(self, start=neighbour, goal=sink):
                                        if neighbour not in visited and neighbour.rating and neighbour.rating >= threshold:
                                            trusts_at_level.append(t.direct_trust(current, neighbour))

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


if __name__ == "__main__":
    main()
