#!/usr/bin/python3
'''
Created on Jun 17, 2016

@author: sbartholomew
'''

import psycopg2
from flask import Flask, abort, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/combatant/<int:combatant_id>')
def combatant(combatant_id=None):
    output = []
    try:
        con, cursor = connect()

        class combatant():
            def __init__(self, args):
                self.name = args[0]
                self.species = args[1]
                self.attack = args[2]
                self.defense = args[3]
                self.health = args[4]
        querry = 'SELECT ' +\
            ' combatant.name, ' +\
            ' species.name, ' +\
            ' combatant.plus_atk + ' +\
            '  (SELECT ' +\
            '   species.base_atk ' +\
            '  FROM ' +\
            '   species ' +\
            '  WHERE ' +\
            '   species.id = combatant.species_id), ' +\
            ' combatant.plus_dfn + ' +\
            '  (SELECT ' +\
            '   species.base_dfn ' +\
            '  FROM ' +\
            '   species ' +\
            '  WHERE ' +\
            '   species.id = combatant.species_id), ' +\
            ' combatant.plus_hp + ' +\
            '  (SELECT ' +\
            '   species.base_hp ' +\
            '  FROM ' +\
            '   species ' +\
            '  WHERE ' +\
            '   species.id = combatant.species_id) ' +\
            'FROM ' +\
            ' combatant, ' +\
            ' species ' +\
            'WHERE ' +\
            " combatant.id = '" + str(combatant_id) + "' AND " +\
            ' species.id = combatant.species_id;'
        cursor.execute(querry)  # flask type coversion avoid SQL injection
        results = cursor.fetchall()
        if results:
            for data in results:
                info = combatant(data)
                output.append(info)
        con.commit()
        con.close()
        return render_template('combatant.html', combatants=output)
    except:
        return "ERROR happened"


@app.route('/results/')
def results():
    try:
        con, cursor = connect()
    
        class result():
            def __init__(self, rank, args):
                self.rank = rank
                self.name = args[0]
                self.id = args[1]
                self.wins = args[2]
        querry = 'SELECT ' +\
            ' combatant.name, ' +\
            ' combatant.id, ' +\
            ' count(fight.combatant_one) ' +\
            'FROM ' +\
            ' (SELECT ' +\
            '   fight.combatant_one ' +\
            '  FROM ' +\
            '   public.fight ' +\
            '  WHERE ' +\
            "   fight.winner = 'One' " +\
            '  Union ALL ' +\
            '  SELECT ' +\
            '   fight.combatant_two ' +\
            '  FROM ' +\
            '   public.fight ' +\
            '  WHERE ' +\
            "   fight.winner = 'Two') as fight, " +\
            ' combatant ' +\
            'WHERE ' +\
            ' fight.combatant_one = combatant.id ' +\
            'GROUP BY ' +\
            ' combatant.id ' +\
            'ORDER BY ' +\
            ' count(fight.combatant_one) DESC;'
    
        cursor.execute(querry)
        results = cursor.fetchall()
        output = []
        rank = 1
        for data in results:
            info = result(str(rank), data)
            output.append(info)
            rank += 1
        print (output)
        con.commit()
        con.close()
        return render_template('results.html', combatants=output)
    except:
        return "ERROR happened"

@app.route('/battle/<int:id1>-<int:id2>')
@app.route('/battle/<int:battle_id>')
def battles(battle_id=None, id1=None, id2=None):
    try:
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
        if(battle_id):
            querry = 'SELECT ' +\
                ' fight.winner, ' +\
                ' combatant_one, ' +\
                ' combatant_two, ' +\
                ' (SELECT name FROM combatant ' +\
                '  WHERE fight.combatant_one = combatant.id), ' +\
                ' (SELECT name FROM combatant ' +\
                '  WHERE fight.combatant_two = combatant.id), ' +\
                ' fight.id, ' +\
                ' fight.start, ' +\
                ' fight.finish ' +\
                'FROM ' +\
                ' fight ' +\
                'WHERE ' +\
                " fight.id = '" + str(battle_id) + "';"
            cursor.execute(querry)  # no SQL injection
        elif(id1 and id2):
            querry = 'SELECT ' +\
                ' fight.winner, ' +\
                ' combatant_one, ' +\
                ' combatant_two, ' +\
                ' (SELECT name FROM combatant ' +\
                '  WHERE fight.combatant_one = combatant.id), ' +\
                ' (SELECT name FROM combatant ' +\
                '  WHERE fight.combatant_two = combatant.id), ' +\
                ' fight.id, ' +\
                ' fight.start, ' +\
                ' fight.finish ' +\
                'FROM ' +\
                ' fight ' +\
                'WHERE ' +\
                " combatant_one = '" + str(id1) + "' AND " +\
                " combatant_two = '" + str(id2) + "';"
            cursor.execute(querry)  # no SQL injection
        results = cursor.fetchall()
        fights = []
        if results:
            info = fight(results[0])
            fights.append(info)
        con.commit()
        con.close()
        return render_template('battle_id.html', fights=fights)
    except:
        return "ERROR happened"


@app.route('/battle')
def battle(name=None):
    try:
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
            ' fight.winner, ' +\
            ' combatant_one, ' +\
            ' combatant_two, ' +\
            ' (SELECT name FROM combatant ' +\
            '  WHERE fight.combatant_one = combatant.id), ' +\
            ' (SELECT name FROM combatant ' +\
            '  WHERE fight.combatant_two = combatant.id), ' +\
            ' fight.id ' +\
            'FROM ' +\
            ' fight;'
        cursor.execute(querry)
        results = cursor.fetchall()
        battle_list = []
        if results:
            for battle in results:
                new_fight = fight(battle)
                battle_list.append(new_fight)
        con.commit()
        con.close()
        return render_template('battle.html', fights=battle_list)
    except:
        return "ERROR happened"


@app.route('/combatant/')
def combatants():
    con, cursor = connect()

    class combatant():
         def __init__(self, args):
            self.id = args[0]
            self.name = args[1]
            self.species = args[2]
    querry = 'SELECT ' +\
        ' combatant.id, ' +\
        ' combatant.name, ' +\
        ' species.name ' +\
        'FROM ' +\
        ' combatant, ' +\
        ' species ' +\
        'WHERE ' +\
        ' combatant.species_id = species.id ' +\
        'ORDER BY ' +\
        ' combatant.name;'
    cursor.execute(querry)
    results = cursor.fetchall()
    combatant_list = []
    if results:
        for guy in results:
            new_guy = combatant(guy)
            combatant_list.append(new_guy)
    print(combatant_list)
    con.commit()
    con.close()
    return render_template('combatants.html', combatants=combatant_list)
    

def connect():
    con = psycopg2.connect(
        database='safetydome',
        user='flask',
        password='flask',
        host='localhost'
        )
    if not con:
        print("could not connect")
    cursor = con.cursor()
    return con, cursor

if __name__ == '__main__':
    app.run(debug=True, port=8058)
