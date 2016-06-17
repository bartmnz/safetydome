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
        def __init__(self, args):
            self.one_id = args[1]
            self.two_id = args[2]
            self.one_name = args[3]
            self.two_name = args[4]
            self.winner = 'Tie'
            if str(args[0]) == 'One':
                self.winner = self.one_name
            elif str(args[0]) == 'Two':
                self.winner = self.two_name
            fight_id = args[5]
    querry = 'SELECT ' +\
        'fight.winner, ' +\
        'combatant_one, ' +\
        'combatant_two, ' +\
        '(SELECT name FROM combatant ' +\
        'WHERE fight.combatant_one = combatant.id), ' +\
        '(SELECT name FROM combatant ' +\
        'WHERE fight.combatant_two = combatant.id), ' +\
        'fight.id ' +\
        'FROM ' +\
        'fight, '+\
        'combatant;'
    cursor.execute(querry)
    results = cursor.fetchall()
    battle_list = []
    
    for battle in results:
        new_fight = fight(battle)
        battle_list.append(new_fight)
    con.commit()
    con.close()
    return render_template('battle.html', fights=battle_list)
#    TODO


@app.route('/combatants')
def combatants():
    con, cursor = connect()
    

    class combatant():
        def __init__(self, args):
            self.id = args[0]
            self.name = args[1]
            self.species = args[2]
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
        new_guy = combatant(guy)
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
