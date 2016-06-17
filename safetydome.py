'''
Created on Jun 17, 2016

@author: sbartholomew
'''

import psycopg2
from flask import Flask, abort, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hi there '

@app.route('/combatant/<name>')
@app.route('/combatant/')
def combatants(name = None):
    con, cursor = connect()
#    TODO

@app.route('/battle')
def battle(name = None):
    con, cursor = connect()
#    TODO


@app.route('/combatants')
def combatants():
    con, cursor = connect()
    

    class combatant():
        id = None
        name = None
        species = None
    querry = 'SELECT ' +\
        'combatant.id, combatant.name, species.name ' +\
        'FROM ' +\
        'combatant, ' +\
        'species ' +\
        'WHERE ' +\
        'combatant.species_id = species_id;'
    cursor.execute(querry)
    results = cursor.fetchall()
    combatant_list = []
    
    for guy in results:
        new_guy = combatant()
        new_guy.id=guy[0]
        new_guy.name = guy[1]
        new_guy.species=guy[2]
        combatant_list.append(new_guy)
    print(combatant_list)
    con.commit()
    con.close()
    return render_template('combatants.html', combatants=combatant_list)


def connect():
    connect_line = "dbname=safetydome user=sbartholomew"
    con = psycopg2.connect(connect_line)
    cursor = con.cursor()
    return con, cursor

if __name__ == '__main__':
    app.run(debug=True, port=8058)
