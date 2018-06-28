# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 12:30:46 2018

@author: CAGurley
"""

import csv
import re
import sqlite3


def _parse_lmpd_hc_csv():
    header = None
    rows_list = []
    with open('LMPD_OP_BIAS_7.csv') as raw_hc_data:
        reader = csv.reader(raw_hc_data)
        for row in reader:
            stripped_row = []
            for entry in row:
                stripped_row.append(entry.strip().upper())
            rows_list.append(stripped_row)
        header = rows_list.pop(0)
    return header, rows_list


def newfunc():
    pass


header_list, list_lists = _parse_lmpd_hc_csv()

list_tuples = []
for row in list_lists:
    list_tuples.append(tuple(row))
column_types = []

print(header_list)
print(list_lists)
for value in header_list:
    print(value)
print(len(header_list))
print(len(list_lists))

counter = 0
while counter < len(header_list):
    int_row_counter = 1
    for row in list_lists:
        if (bool(re.search(r'^\d+$', row[counter]))
                and int_row_counter < len(list_lists)):
            int_row_counter += 1
            continue
        elif (bool(re.search(r'^\d+$', row[counter]))
                and int_row_counter >= len(list_lists)):
            column_types.append('INTEGER PRIMARY KEY')
            break
        else:
            column_types.append('TEXT')
            break
    counter += 1
print(column_types)

new_counter = 0
statement_center = ''
while new_counter < len(header_list):
    statement_center += (
        "\n    "
        + header_list[new_counter]
        + " "
        + column_types[new_counter]
        + ","
    )
    new_counter += 1
statement_center = statement_center.rstrip(',')
create_statement = (
    "CREATE TABLE IF NOT EXISTS LOU_HATE_CRIMES("
    + statement_center
    + "\n);"
)
print(create_statement)

conn = sqlite3.connect('lou_hate_crime_database.db')
cur = conn.cursor()
try:
    cur.execute("DROP TABLE IF EXISTS LOU_HATE_CRIMES;")
    cur.execute(create_statement)
    cur.executemany("""
                    INSERT INTO LOU_HATE_CRIMES
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, list_tuples)
    conn.commit()
finally:
    conn.rollback()
    cur.close()
    conn.close()
