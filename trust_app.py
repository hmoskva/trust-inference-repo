from django.http import request
from flask import Flask, render_template, request
import sql

import graph_setup
from graph_setup import g
from iris_trust import Trust

app = Flask(__name__)
app.database = 'twitter_data.db'
app.secret_key = 'kljhsjkkk[.,]v.jfslvkfsnlvj'

global graph
graph = graph_setup.setup_iris()
global graph_nodes
graph_nodes = list(g.vertices.values())
global t
t = Trust()

@app.route('/')
def index():

    return render_template('index.html', users=graph_nodes, friends=sql.get_friends(452454655))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/iris', methods=['GET', 'POST'])
def iris():
    return
@app.route('/calculate_trust', methods=['GET', 'POST'])
def calculate_trust():
    graph_setup.setup_iris()
    error = None
    if request.method == 'POST':
        ego_user = g.vertices[request.form['drp_ego']]
        drp_other = get_path_nodes(ego_user)

        if request.form['drp_user'] != '0' and request.form['drp_ego'] != '0':
            trust = t.tidal(source=g.vertices[request.form['drp_user']], sink=g.vertices[request.form['drp_ego']])
            recommendations = []
            if type(trust) == float:
                if trust >= 0.5:
                    recommendations.append(g.vertices[request.form['drp_ego']])
                    for friend in g.vertices[request.form['drp_ego']].get_neighbours():
                        friend_trust = t.tidal(
                            source=g.vertices[request.form['drp_ego']],
                            sink=g.vertices[friend.name])
                        if friend_trust >= 0.5 and g.vertices[friend.name] != g.vertices[request.form['drp_user']]:
                            recommendations.append(g.vertices[friend.name])
                # if len(sql.get_friends(g.vertices[request.form['drp_ego']].idd)) != 0:
                #     for friend in g.vertices[request.form['drp_ego']].get_neighbours():
                #         friend_trust = t.tidal(source=g.vertices[request.form['drp_ego']],
                #                             sink=g.vertices[friend.name])
                #         if friend_trust >= trust and g.vertices[friend.name] != g.vertices[request.form['drp_user']]:
                #             recommendations.append(g.vertices[friend.name])

            print(trust)
            return render_template('index.html', trust=trust, users=graph_nodes, friends=sql.get_friends(452454655)
                                    , recommendations=recommendations, source=request.form['drp_user'],
                                    sink=request.form['drp_ego'])
        else:
            error = 'You have to select two(2) users!'

    return render_template('index.html', error=error, users=graph_nodes, friends=sql.get_friends(452454655))

def get_path_nodes(start):
    stack = []
    visited = []
    stack.append(start)
    while len(stack) != 0:
        current = stack.pop()
        visited.append(current)

        if len(current.get_neighbours()) != 0:
            for neighbour in current.get_neighbours():
                if neighbour not in visited and neighbour not in stack:
                    stack.append(neighbour)

        return [node.name for node in visited]

if __name__ == '__main__':
    app.run(debug=True)
