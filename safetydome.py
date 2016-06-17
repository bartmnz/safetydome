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

@app.route('/results/')
def results():
    con, cursor = connect()
    
    class result():
        def __init__(self, rank, args):
            self.rank = rank
            self.name = args[0]
            self.id = args[1]
            self.wins = args[2]
    querry = 'SELECT ' +\
        'combatant.name, ' +\
        'combatant.id, ' +\
        'count(fight.combatant_one) ' +\
        'FROM ' +\
        ' (SELECT ' +\
        '   fight.combatant_one '+\
        '  FROM ' +\
        '   public.fight ' +\
        '  WHERE ' +\
        "   fight.winner = 'One' " +\
        '  Union ALL ' +\
        '  SELECT ' +\
        '   fight.combatant_two ' +\
        '  FROM ' +\
        '   public.fight '+\
        '  WHERE ' +\
        "   fight.winner = 'Two') as fight, " +\
        ' combatant ' +\
        'WHERE ' +\
        ' fight.combatant_one = combatant.id ' +\
        'GROUP BY ' +\
        ' combatant.name, ' +\
        ' combatant.id ' +\
        'ORDER BY ' +\
        ' count(fight.combatant_one) DESC;'
    
    cursor.execute(querry)
    results = cursor.fetchall()
    output = []
    rank = 1
    print( results )
    for data in results:
        info = result(str(rank), data)
        output.append(info)
        rank += 1
    print (output)
    con.commit()
    con.close()
    return render_template('results.html', combatants=output)
    
    
#    TODO

@app.route('/battle/<battle_id>')
def battles(battle_id = None):
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
            self.fight_id = args[5]
            self.start = args[6]
            self.end = args[7]
    querry = 'SELECT ' +\
        'fight.winner, ' +\
        'combatant_one, ' +\
        'combatant_two, ' +\
        '(SELECT name FROM combatant ' +\
        'WHERE fight.combatant_one = combatant.id), ' +\
        '(SELECT name FROM combatant ' +\
        'WHERE fight.combatant_two = combatant.id), ' +\
        'fight.id, ' +\
        'fight.start, ' +\
        'fight.finish ' +\
        'FROM ' +\
        'fight '+\
        'WHERE ' +\
        'fight.id = ' + str(battle_id) + ';'
    cursor.execute(querry)
    results = cursor.fetchall()
    info = fight(results[0])
    fights = [info]
            
    con.commit()
    con.close()
    return render_template('battle_id.html', fights=fights)

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
            self.fight_id = args[5]
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
