# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 17:27:45 2018

@author: Atticus
"""

import csv2db


crime_type_select = """
    SELECT CRIME_TYPE, COUNT(*) AS COUNT
    FROM CRIMES
    GROUP BY 1
    ORDER BY 1;
    """
csv2db.select_to_csv('lou_crime_database.db', crime_type_select, 'CRIMES_crime_type_count')
