# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 15:17:04 2018

@author: Atticus
"""

import csv2db
import sqlite3


print('Initializing database...')

# This dict maps files to tables in a one-to-one relationship.
single_tables = {
    'HATE_CRIMES': '../data/LMPD_OP_BIAS_7',
    'OFFICER_ASSAULTS': '../data/AssaultedOfficerData',
    'FIREARM_INTAKE': '../data/FIREARMS_DATA_0_0'
}
# This structure maps files to tables in a many-to-one relationship.
# For this DB, only crime data needs to merged from single-year files.
merge_tables = [
    ('CRIMES', [
        '../data/Crime_Data_2008',
        '../data/Crime_Data_2009',
        '../data/Crime_Data_2010',
        '../data/Crime_Data_2011',
        '../data/Crime_Data_2012',
        '../data/Crime_Data_2013',
        '../data/Crime_Data_2014',
        '../data/Crime_Data_2015',
        '../data/Crime_Data_2016_29',
        '../data/Crime_Data_2017_1'
    ])
]

# This block creates and inserts data into the one-to-one tables
for table_name, file_name in single_tables.items():
    header, rows = csv2db.parse_csv_data(file_name)
    # Correcting spelling in source file
    for index, field in enumerate(header):
        if field == 'DATE_OCCURED':
            header[index] = 'DATE_OCCURRED'
    col_types = csv2db.declare_col_types(header, rows)
    # Correcting inconsistencies in source file
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
    temp_statement = csv2db.compile_ct_statement(
        header, col_types, table_name, True
    )
    create_statement = csv2db.compile_ct_statement(
        header, col_types, table_name
    )

    insert_statement = (
        """
        INSERT INTO {}
        VALUES(
        """
        + ('?, '*len(header)).rstrip(', ')
        + ');'
    )

    conn = sqlite3.connect('../lou_crime_database.db')
    cur = conn.cursor()
    try:
        # First half creates temp table from raw data
        print('Dropping old temp table...')
        cur.execute("DROP TABLE IF EXISTS {};".format('TEMP_' + table_name))
        print('Creating temp table...')
        cur.execute(temp_statement)
        print('Inserting temp values...')
        cur.executemany(
            insert_statement.format('TEMP_' + table_name), table_values
        )
        conn.commit()
        # Second half creates perm table from distinct temp rows
        print('Dropping old table...')
        cur.execute("DROP TABLE IF EXISTS {};".format(table_name))
        print('Creating table...')
        cur.execute(create_statement)
        print('Inserting values...')
        cur.execute(
            """
            INSERT INTO {0}
            SELECT DISTINCT *
            FROM TEMP_{0};
            """.format(table_name)
        )
        conn.commit()
        print('New table created and populated using:\n' + create_statement)
    finally:
        conn.rollback()
        cur.close()
        conn.close()

# This block merges files, then creates and inserts data into "merged" tables
for table_name, file_names in merge_tables:
    file_headers = []
    file_col_types = []
    file_rows = []
    for file_name in file_names:
        header, rows = csv2db.parse_csv_data(file_name)
        # Correcting spelling in source file
        for index, field in enumerate(header):
            if field == 'DATE_OCCURED':
                header[index] = 'DATE_OCCURRED'
        col_types = csv2db.declare_col_types(header, rows)
        # Correcting inconsistencies in source file
        for row in rows:
            for index, entry in enumerate(row):
                if entry == 'LVIL':
                    row[index] = 'LOUISVILLE'
                elif entry == 'NULL':
                    row[index] = None
        file_headers.append(header)
        file_col_types.append(col_types)
        file_rows.append(rows)

    table_header, table_col_types, table_rows = csv2db.merge_to_table(
        file_headers, file_col_types, file_rows
    )

    table_values = []
    for row in table_rows:
        table_values.append(tuple(row))
    temp_statement = csv2db.compile_ct_statement(
        table_header, table_col_types, table_name, True
    )
    create_statement = csv2db.compile_ct_statement(
        table_header, table_col_types, table_name
    )

    insert_statement = (
        """
        INSERT INTO {}
        VALUES(
        """
        + ('?, '*len(table_header)).rstrip(', ')
        + ');'
    )

    conn = sqlite3.connect('../lou_crime_database.db')
    cur = conn.cursor()
    try:
        # First half creates temp table from raw data
        print('Dropping old temp table...')
        cur.execute("DROP TABLE IF EXISTS {};".format('TEMP_' + table_name))
        print('Creating temp table...')
        cur.execute(temp_statement)
        print('Inserting temp values...')
        cur.executemany(
            insert_statement.format('TEMP_' + table_name), table_values
        )
        conn.commit()
        # Second half creates perm table from distinct temp rows
        print('Dropping old table...')
        cur.execute("DROP TABLE IF EXISTS {};".format(table_name))
        print('Creating table...')
        cur.execute(create_statement)
        print('Inserting values...')
        cur.execute(
            """
            INSERT INTO {0}
            SELECT DISTINCT *
            FROM TEMP_{0};
            """.format(table_name)
        )
        conn.commit()
        print('New table created and populated using:\n' + create_statement)
    finally:
        conn.rollback()
        cur.close()
        conn.close()

print('Database initialized.')
