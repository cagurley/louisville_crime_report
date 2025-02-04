# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 18:07:47 2018

@author: Atticus
"""

from matplotlib import pyplot as plt
import os
import sqlite3


def right_subset(point_dict, num):
    """
    Returns a specified number of points
    from a dict in order of greatest
    x/key value to least in a new dict.
    """
    item_list = list(point_dict.items())
    item_list.sort(key=None, reverse=True)
    new_dict = dict()
    new_dict.update(item_list[0:num])
    return new_dict


def linear_regression(point_dict, slope_comparison=False):
    """
    Returns a two-tuple consisting of two-tuples
    containing the x and y endpoints for a simple
    linear regression line calculated for a dict of
    points with x-values as keys and y-values as values.
    If slope_comparison is set to True, then regression
    y-values will be divided by their sample mean and the
    x-intercept will be set to the lowest x-value in the
    dict.
    """
    x_bar = 0
    y_bar = 0
    numerator = 0
    denominator = 0
    for item in point_dict.items():
        x_bar += item[0]
        y_bar += item[1]
    x_bar /= len(point_dict.items())
    y_bar /= len(point_dict.items())
    for item in point_dict.items():
        xi = item[0]
        yi = item[1]
        numerator += (xi - x_bar) * (yi - y_bar)
        denominator += (xi - x_bar) * (xi - x_bar)
    b_hat = numerator / denominator
    a_hat = y_bar - b_hat*x_bar
    x0 = min(point_dict.keys())
    xf = max(point_dict.keys())
    if slope_comparison is True:
        b_hat /= y_bar
        y0 = 0
        yf = b_hat*(xf - x0)
    else:
        y0 = a_hat + b_hat*x0
        yf = a_hat + b_hat*xf
    return (x0, xf), (y0, yf)


print('Drawing graphs...')

arson = dict()
assault = dict()
burglary = dict()
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

crime_types = {
    'ARSON': arson,
    'ASSAULT': assault,
    'BURGLARY': burglary,
    'DISTURBING THE PEACE': dist_the_peace,
    'DRUGS/ALCOHOL VIOLATIONS': drugs_alcohol,
    'DUI': dui,
    'FRAUD': fraud,
    'HOMICIDE':  homicide,
    'MOTOR VEHICLE THEFT': motor_vehicle_theft,
    'OTHER': other,
    'ROBBERY': robbery,
    'SEX CRIMES': sex_crimes,
    'THEFT/LARCENY': theft_larceny,
    'VANDALISM': vandalism,
    'VEHICLE BREAK-IN/THEFT':  vehicle_breakin_theft,
    'WEAPONS': weapons
}

years = []
results = None
conn = sqlite3.connect('../lou_crime_database.db')
cur = conn.cursor()
try:
    cur.execute(
        """
        SELECT DISTINCT CAST(SUBSTR(DATE_OCCURRED, 1, 4) AS INTEGER) AS YEAR
        FROM CRIMES
            WHERE YEAR >= '2008'
            ORDER BY 1;
        """
    )
    for entry in cur.fetchall():
        years.append(entry[0])
    cur.execute(
        """
        SELECT CAST(SUBSTR(DATE_OCCURRED, 1, 4) AS INTEGER) AS YEAR, CRIME_TYPE, COUNT(*) AS COUNT
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
    for crime_type_dict in crime_types.values():
        crime_type_dict.update([(year, 0)])
for row in results:
    for db_type_value, crime_type_dict in crime_types.items():
        if row[1] == db_type_value:
            crime_type_dict.update([(row[0], row[2])])

if not os.path.exists('../graphs'):
    os.mkdir('../graphs')

for crime_type_dict in crime_types.values():
    line_color = 'k'
    if crime_type_dict == homicide:
        line_color = 'b'
    elif crime_type_dict == weapons:
        line_color = 'r'
    elif crime_type_dict in [dui, other]:
        continue
    plt.plot(crime_type_dict.keys(), crime_type_dict.values(), line_color)
plt.xticks(years, years)
plt.ylim(ymin=0)
plt.xlabel('Year of Occurrence')
plt.ylabel('Crime Count')
plt.title('Crimes 2008-2017')
plt.savefig('../graphs/all_standard_10.png')
plt.close()

wea_x, wea_y = linear_regression(weapons)
plt.plot(weapons.keys(), weapons.values(), 'ro')
plt.plot(wea_x, wea_y, 'r')
plt.xticks(years, years)
plt.ylim(ymin=0)
plt.xlabel('Year of Occurrence')
plt.ylabel('Crime Count')
plt.title('Weapons Crimes 2008-2017')
plt.savefig('../graphs/weapons_standard_10.png')
plt.close()

hom_x, hom_y = linear_regression(homicide)
plt.plot(homicide.keys(), homicide.values(), 'bo')
plt.plot(hom_x, hom_y, 'b')
plt.xticks(years, years)
plt.ylim(ymin=0)
plt.xlabel('Year of Occurrence')
plt.ylabel('Crime Count')
plt.title('Homicides 2008-2017')
plt.savefig('../graphs/homicides_standard_10.png')
plt.close()

# Note that weapons and homicide values were set above
ars_x, ars_y = linear_regression(arson)
ass_x, ass_y = linear_regression(assault)
bur_x, bur_y = linear_regression(burglary)
dis_x, dis_y = linear_regression(dist_the_peace)
dru_x, dru_y = linear_regression(drugs_alcohol)
fra_x, fra_y = linear_regression(fraud)
mot_x, mot_y = linear_regression(motor_vehicle_theft)
oth_x, oth_y = linear_regression(other)
rob_x, rob_y = linear_regression(robbery)
sex_x, sex_y = linear_regression(sex_crimes)
the_x, the_y = linear_regression(theft_larceny)
van_x, van_y = linear_regression(vandalism)
veh_x, veh_y = linear_regression(vehicle_breakin_theft)

plt.plot(ars_x, ars_y, 'k')
plt.plot(ass_x, ass_y, 'k')
plt.plot(bur_x, bur_y, 'k')
plt.plot(dis_x, dis_y, 'k')
plt.plot(dru_x, dru_y, 'k')
plt.plot(fra_x, fra_y, 'k')
plt.plot(hom_x, hom_y, 'b')
plt.plot(mot_x, mot_y, 'k')
plt.plot(rob_x, rob_y, 'k')
plt.plot(sex_x, sex_y, 'k')
plt.plot(the_x, the_y, 'k')
plt.plot(van_x, van_y, 'k')
plt.plot(veh_x, veh_y, 'k')
plt.plot(wea_x, wea_y, 'r')
plt.xticks(years, years)
plt.ylim(ymin=0)
plt.xlabel('Year of Occurrence')
plt.ylabel('Crime Count')
plt.title('Linear Regressions per Crime Type 2008-2017')
plt.savefig('../graphs/regressions_standard_10.png')
plt.close()

ars_x, ars_y = linear_regression(arson, True)
ass_x, ass_y = linear_regression(assault, True)
bur_x, bur_y = linear_regression(burglary, True)
dis_x, dis_y = linear_regression(dist_the_peace, True)
dru_x, dru_y = linear_regression(drugs_alcohol, True)
dui_x, dui_y = linear_regression(dui, True)
fra_x, fra_y = linear_regression(fraud, True)
hom_x, hom_y = linear_regression(homicide, True)
mot_x, mot_y = linear_regression(motor_vehicle_theft, True)
rob_x, rob_y = linear_regression(robbery, True)
sex_x, sex_y = linear_regression(sex_crimes, True)
the_x, the_y = linear_regression(theft_larceny, True)
van_x, van_y = linear_regression(vandalism, True)
veh_x, veh_y = linear_regression(vehicle_breakin_theft, True)
wea_x, wea_y = linear_regression(weapons, True)

plt.plot(ars_x, ars_y, 'k')
plt.plot(ass_x, ass_y, 'k')
plt.plot(bur_x, bur_y, 'k')
plt.plot(dis_x, dis_y, 'k')
plt.plot(dru_x, dru_y, 'k')
plt.plot(fra_x, fra_y, 'k')
plt.plot(hom_x, hom_y, 'b')
plt.plot(mot_x, mot_y, 'k')
plt.plot(rob_x, rob_y, 'k')
plt.plot(sex_x, sex_y, 'k')
plt.plot(the_x, the_y, 'k')
plt.plot(van_x, van_y, 'k')
plt.plot(veh_x, veh_y, 'k')
plt.plot(wea_x, wea_y, 'r')
plt.xticks(years, years)
plt.xlabel('Year of Occurrence')
plt.ylabel('Adjusted Crime Value')
plt.title('Adjusted Regressions per Crime Type 2008-2017')
plt.savefig('../graphs/regressions_adjusted_10.png')
plt.close()

ars_x, ars_y = linear_regression(right_subset(arson, 5), True)
ass_x, ass_y = linear_regression(right_subset(assault, 5), True)
bur_x, bur_y = linear_regression(right_subset(burglary, 5), True)
dis_x, dis_y = linear_regression(right_subset(dist_the_peace, 5), True)
dru_x, dru_y = linear_regression(right_subset(drugs_alcohol, 5), True)
dui_x, dui_y = linear_regression(right_subset(dui, 5), True)
fra_x, fra_y = linear_regression(right_subset(fraud, 5), True)
hom_x, hom_y = linear_regression(right_subset(homicide, 5), True)
mot_x, mot_y = linear_regression(right_subset(motor_vehicle_theft, 5), True)
rob_x, rob_y = linear_regression(right_subset(robbery, 5), True)
sex_x, sex_y = linear_regression(right_subset(sex_crimes, 5), True)
the_x, the_y = linear_regression(right_subset(theft_larceny, 5), True)
van_x, van_y = linear_regression(right_subset(vandalism, 5), True)
veh_x, veh_y = linear_regression(right_subset(vehicle_breakin_theft, 5), True)
wea_x, wea_y = linear_regression(right_subset(weapons, 5), True)

plt.plot(ars_x, ars_y, 'k')
plt.plot(ass_x, ass_y, 'k')
plt.plot(bur_x, bur_y, 'k')
plt.plot(dis_x, dis_y, 'k')
plt.plot(dru_x, dru_y, 'k')
plt.plot(fra_x, fra_y, 'k')
plt.plot(hom_x, hom_y, 'b')
plt.plot(mot_x, mot_y, 'k')
plt.plot(rob_x, rob_y, 'k')
plt.plot(sex_x, sex_y, 'k')
plt.plot(the_x, the_y, 'k')
plt.plot(van_x, van_y, 'k')
plt.plot(veh_x, veh_y, 'k')
plt.plot(wea_x, wea_y, 'r')
plt.xticks(years[-5:], years[-5:])
plt.xlabel('Year of Occurrence')
plt.ylabel('Adjusted Crime Value')
plt.title('Adjusted Regressions per Crime Type 2013-2017')
plt.savefig('../graphs/regressions_adjusted_05.png')
plt.close()

ars_x, ars_y = linear_regression(right_subset(arson, 3), True)
ass_x, ass_y = linear_regression(right_subset(assault, 3), True)
bur_x, bur_y = linear_regression(right_subset(burglary, 3), True)
dis_x, dis_y = linear_regression(right_subset(dist_the_peace, 3), True)
dru_x, dru_y = linear_regression(right_subset(drugs_alcohol, 3), True)
dui_x, dui_y = linear_regression(right_subset(dui, 3), True)
fra_x, fra_y = linear_regression(right_subset(fraud, 3), True)
hom_x, hom_y = linear_regression(right_subset(homicide, 3), True)
mot_x, mot_y = linear_regression(right_subset(motor_vehicle_theft, 3), True)
rob_x, rob_y = linear_regression(right_subset(robbery, 3), True)
sex_x, sex_y = linear_regression(right_subset(sex_crimes, 3), True)
the_x, the_y = linear_regression(right_subset(theft_larceny, 3), True)
van_x, van_y = linear_regression(right_subset(vandalism, 3), True)
veh_x, veh_y = linear_regression(right_subset(vehicle_breakin_theft, 3), True)
wea_x, wea_y = linear_regression(right_subset(weapons, 3), True)

plt.plot(ars_x, ars_y, 'k')
plt.plot(ass_x, ass_y, 'k')
plt.plot(bur_x, bur_y, 'k')
plt.plot(dis_x, dis_y, 'k')
plt.plot(dru_x, dru_y, 'k')
plt.plot(fra_x, fra_y, 'k')
plt.plot(hom_x, hom_y, 'b')
plt.plot(mot_x, mot_y, 'k')
plt.plot(rob_x, rob_y, 'k')
plt.plot(sex_x, sex_y, 'k')
plt.plot(the_x, the_y, 'k')
plt.plot(van_x, van_y, 'k')
plt.plot(veh_x, veh_y, 'k')
plt.plot(wea_x, wea_y, 'r')
plt.xticks(years[-3:], years[-3:])
plt.xlabel('Year of Occurrence')
plt.ylabel('Adjusted Crime Value')
plt.title('Adjusted Regressions per Crime Type 2015-2017')
plt.savefig('../graphs/regressions_adjusted_03.png')
plt.close()

print('Graphs drawn.')
