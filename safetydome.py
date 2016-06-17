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
def combatant(name = None):
    con, cursor = connect()
#    TODO

@app.route('/battle')
def battle(name = None):
    con, cursor = connect()
    
    class fight():
        one_id = None
        one_name = None
        two_id = None
        two_name = None
        winner = None
    querry = 'SELECT ' +\
        'fight.winner, ' +\
        'combatant_one, ' +\
        'combatant_two, ' +\
        '(SELECT name FROM combatant ' +\
        'WHERE fight.combatant_one = combatant.id), ' +\
        '(SELECT name FROM combatant ' +\
        'WHERE fight.combatant_two = combatant.id) ' +\
        'FROM ' +\
        'fight, '+\
        'combatant;'
    cursor.execute(querry)
    results = cursor.fetchall()
    battle_list = []
    print(results)
    
    for battle in results:
        new_fight = fight()
        if str(battle[0]) == 'One':
            new_fight.winner = battle[3]
        elif str(battle[0]) == 'Two':
            new_fight.winner = battle[4]
        else:
            new_fight.winner = 'Tie'
        new_fight.one_id = battle[1]
        new_fight.two_id = battle[2]
        new_fight.one_name = battle[3]
        new_fight.two_name = battle[4]
        battle_list.append(new_fight)
    print (battle_list)
    con.commit()
    con.close()
    return render_template('battle.html', fights=battle_list)
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
#    print(combatant_list)
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
