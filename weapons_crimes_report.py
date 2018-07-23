# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 18:07:47 2018

@author: Atticus
"""

from matplotlib import pyplot as plt
import sqlite3


arson = dict()
assault = dict()
buglary = dict()
dist_the_peace = dict()
drugs_alcohol = dict()
dui = dict()
fraud = dict()
homicide = dict()
motor_vehicle_theft = dict()
other = dict()
robbery = dict()
sex_crimes = dict()
theft_larceny = dict()
vandalism = dict()
vehicle_breakin_theft = dict()
weapons = dict()

years = []
results = None
conn = sqlite3.connect('lou_crime_database.db')
cur = conn.cursor()
try:
    cur.execute(
        """
        SELECT DISTINCT SUBSTR(DATE_OCCURRED, 1, 4) AS YEAR
        FROM CRIMES
            WHERE YEAR >= '2008'
            ORDER BY 1;
        """
    )
    for entry in cur.fetchall():
        years.append(entry[0])
    cur.execute(
        """
        SELECT SUBSTR(DATE_OCCURRED, 1, 4) AS YEAR, CRIME_TYPE, COUNT(*) AS COUNT
        FROM CRIMES
            WHERE YEAR >= '2008'
            GROUP BY 1, 2
            ORDER BY 1, 2;
        """
    )
    results = cur.fetchall()
    conn.commit()
finally:
    conn.rollback()
    cur.close()
    conn.close()

for year in years:
    arson.update([(year, 0)])
    assault.update([(year, 0)])
    buglary.update([(year, 0)])
    dist_the_peace.update([(year, 0)])
    drugs_alcohol.update([(year, 0)])
    dui.update([(year, 0)])
    fraud.update([(year, 0)])
    homicide.update([(year, 0)])
    motor_vehicle_theft.update([(year, 0)])
    other.update([(year, 0)])
    robbery.update([(year, 0)])
    sex_crimes.update([(year, 0)])
    theft_larceny.update([(year, 0)])
    vandalism.update([(year, 0)])
    vehicle_breakin_theft.update([(year, 0)])
    weapons.update([(year, 0)])
for row in results:
    if row[1] == 'ARSON':
        arson.update([(row[0], row[2])])
    elif row[1] == 'ASSAULT':
        assault.update([(row[0], row[2])])
    elif row[1] == 'BURGLARY':
        buglary.update([(row[0], row[2])])
    elif row[1] == 'DISTURBING THE PEACE':
        dist_the_peace.update([(row[0], row[2])])
    elif row[1] == 'DRUGS/ALCOHOL VIOLATIONS':
        drugs_alcohol.update([(row[0], row[2])])
    elif row[1] == 'DUI':
        dui.update([(row[0], row[2])])
    elif row[1] == 'FRAUD':
        fraud.update([(row[0], row[2])])
    elif row[1] == 'HOMICIDE':
        homicide.update([(row[0], row[2])])
    elif row[1] == 'MOTOR VEHICLE THEFT':
        motor_vehicle_theft.update([(row[0], row[2])])
    elif row[1] == 'OTHER':
        other.update([(row[0], row[2])])
    elif row[1] == 'ROBBERY':
        robbery.update([(row[0], row[2])])
    elif row[1] == 'SEX CRIMES':
        sex_crimes.update([(row[0], row[2])])
    elif row[1] == 'THEFT/LARCENY':
        theft_larceny.update([(row[0], row[2])])
    elif row[1] == 'VANDALISM':
        vandalism.update([(row[0], row[2])])
    elif row[1] == 'VEHICLE BREAK-IN/THEFT':
        vehicle_breakin_theft.update([(row[0], row[2])])
    elif row[1] == 'WEAPONS':
        weapons.update([(row[0], row[2])])
#print(arson)
#print(assault)
#print(buglary)
#print(dist_the_peace)
#print(drugs_alcohol)
#print(dui)
#print(fraud)
#print(homicide)
#print(motor_vehicle_theft)
#print(other)
#print(robbery)
#print(sex_crimes)
#print(theft_larceny)
#print(vandalism)
#print(vehicle_breakin_theft)
print(weapons)
print(weapons.keys())
print(weapons.values())

#bins = list(weapons.keys())
#for index, value in enumerate(bins):
#    bins[index] = int(value)
plt.plot(weapons.keys(), weapons.values(), 'o')
plt.show()
    
