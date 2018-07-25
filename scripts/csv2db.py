# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 12:30:46 2018

@author: CAGurley
"""

import csv
import re
import sqlite3


def parse_csv_data(file_path):
    rows = []
    with open(file_path + '.csv') as raw_data:
        reader = csv.reader(raw_data)
        for row in reader:
            stripped_row = []
            for entry in row:
                stripped_row.append(entry.strip().upper())
            rows.append(stripped_row)

    header = rows.pop(0)
    for counter, name in enumerate(header):
        name = re.sub(r'\s+', r'_', name)
        header[counter] = re.sub(r'\W+', r'', name)

    return header, rows


def declare_col_types(header, rows):
    try:
        lengths = {len(header)}
        for row in rows:
            lengths.add(len(row))
        if len(lengths) != 1:
            raise IndexError("Row length mismatch")
    except IndexError:
        print("Header and rows must all be of equal length")
    else:
        col_counter = 0
        col_types = []
        while col_counter < len(header):
            int_row_counter = 1
            for row in rows:
                if (bool(re.search(r'^\d+$', row[col_counter]))
                        and int_row_counter < len(rows)):
                    int_row_counter += 1
                    continue
                elif (bool(re.search(r'^\d+$', row[col_counter]))
                        and int_row_counter >= len(rows)):
                    if (col_counter == 0
                            and re.search(r'ID$', header[col_counter], re.I)):
                        col_types.append('INTEGER PRIMARY KEY')
                    else:
                        col_types.append('INTEGER')
                    break
                else:
                    col_types.append('TEXT')
                    break
            col_counter += 1
        return col_types


def compile_ct_statement(header, col_types, table_name, temporary=False):
    try:
        if re.search(r'\W+', table_name) is not None:
            raise ValueError("Table name error")
    except ValueError:
        print(
            "Table name must consist only of letters, digits, and underscores."
        )
    else:
        table_name = table_name.upper()
        counter = 0
        statement_center = ''
        while counter < len(header):
            statement_center += (
                "\n    "
                + header[counter]
                + " "
                + col_types[counter]
                + ","
            )
            counter += 1
        statement_center = statement_center.rstrip(',')
        temp_mod = ['', '']
        if temporary is True:
            temp_mod[0] = 'TEMP '
            temp_mod[1] = 'TEMP_'
        ct_statement = (
            "CREATE {}TABLE IF NOT EXISTS ".format(temp_mod[0])
            + temp_mod[1]
            + table_name
            + "("
            + statement_center
            + "\n);"
        )
        return ct_statement


def merge_to_table(header_group, col_types_group, rows_list_group):
    try:
        lengths = set()
        header_set = set()
        col_types_set = set()
        for header in header_group:
            lengths.add(len(header))
            header_set.add(tuple(header))
        for col_types in col_types_group:
            lengths.add(len(col_types))
            col_types_set.add(tuple(col_types))
        for rows_list in rows_list_group:
            for row in rows_list:
                lengths.add(len(row))
        if len(lengths) != 1:
            raise IndexError("Non-uniform row lengths")
        elif len(header_set) != 1 or len(col_types_set) != 1:
            raise ValueError("Non-uniform column defintions")
    except IndexError:
        print("Ensure that all data is of uniform, positive length")
    except ValueError:
        print("Ensure that headers and column types are identical")
    else:
        merged_rows = []
        for rows_list in rows_list_group:
            merged_rows.extend(rows_list)
        return list(header_set.pop()), list(col_types_set.pop()), merged_rows


def select_to_csv(db_path, select_statement, file_path='new_query'):
    try:
        if (re.search(r'^(?:with|select).+;$', select_statement.strip(), flags=re.I | re.S) is None
                or len(re.findall(r';', select_statement)) != 1):
            raise ValueError("Invalid select statement")
    except ValueError as e:
        print(e)
    else:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        try:
            full_path = file_path + '.csv'
            cur.execute(select_statement)
            with open(full_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                header = []
                for entry in cur.description:
                    header.append(entry[0])
                csvwriter.writerow(header)
                csvwriter.writerows(cur.fetchall())
            conn.commit()
        finally:
            conn.rollback()
            cur.close()
            conn.close()
    return None
