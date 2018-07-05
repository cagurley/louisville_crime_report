# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 15:17:04 2018

@author: Atticus
"""

import csv2db
import sqlite3


child_tables = {
    'HATE_CRIMES': 'LMPD_OP_BIAS_7',
    'OFFICER_ASSAULTS': 'AssaultedOfficerData',
    'FIREARM_INTAKE': 'FIREARMS_DATA_0_0',
    'CRIMES_2008': 'Crime_Data_2008',
    'CRIMES_2009': 'Crime_Data_2009',
    'CRIMES_2010': 'Crime_Data_2010',
    'CRIMES_2011': 'Crime_Data_2011',
    'CRIMES_2012': 'Crime_Data_2012',
    'CRIMES_2013': 'Crime_Data_2013',
    'CRIMES_2014': 'Crime_Data_2014',
    'CRIMES_2015': 'Crime_Data_2015',
    'CRIMES_2016': 'Crime_Data_2016_29',
    'CRIMES_2017': 'Crime_Data_2017_1'
}
for table_name, file_name in child_tables.items():
    header, rows = csv2db.parse_csv_data(file_name)
    column_types = csv2db.declare_col_types(header, rows)
    for row in rows:
        entry_counter = 0
        for entry in row:
            if entry == 'LVIL':
                row[entry_counter] = 'LOUISVILLE'
            elif entry == 'NULL':
                row[entry_counter] = None
            entry_counter += 1
    table_values = []
    for row in rows:
        table_values.append(tuple(row))
    create_statement = csv2db.compile_ct_statement(
        header, column_types, table_name
    )
    print(create_statement)

    insert_statement = (
        """
        INSERT INTO {}
        VALUES(
        """
        + ('?, '*len(header)).rstrip(', ')
        + ');'
    )

    conn = sqlite3.connect('lou_crime_database.db')
    cur = conn.cursor()
    try:
        cur.execute("DROP TABLE IF EXISTS {};".format(table_name))
        cur.execute(create_statement)
        cur.executemany(insert_statement.format(table_name), table_values)
        conn.commit()
    finally:
        conn.rollback()
        cur.close()
        conn.close()
