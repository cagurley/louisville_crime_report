# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 17:27:45 2018

@author: Atticus
"""

import csv2db


crimes_select1 = """
    SELECT CRIME_TYPE, COUNT(*) AS COUNT
    FROM CRIMES
    GROUP BY 1
    ORDER BY 1;
    """
crimes_select2 = """
    SELECT SUBSTR(DATE_OCCURED, 1, 4) AS YEAR, COUNT(*) AS COUNT
    FROM CRIMES
        WHERE YEAR >= '2008'
        GROUP BY 1
        ORDER BY 1;
    """
crimes_select3 = """
    SELECT SUBSTR(DATE_OCCURED, 1, 4) AS YEAR, CRIME_TYPE, COUNT(*) AS COUNT
    FROM CRIMES
        WHERE YEAR >= '2008'
        GROUP BY 1, 2
        ORDER BY 1, 2;
    """
crimes_select4 = """
    SELECT SUBSTR(DATE_OCCURED, 1, 4) AS YEAR, CRIME_TYPE, COUNT(*) AS COUNT
    FROM CRIMES
        WHERE YEAR >= '2008'
        GROUP BY 1, 2
        ORDER BY 2, 1;
    """
crimes_select5 = """
    SELECT SUBSTR(CR.DATE_OCCURED, 1, 4) AS CRIME_YEAR, COUNT(*) AS COUNT
    FROM CRIMES AS CR
    INNER JOIN FIREARM_INTAKE AS FI ON CR.INCIDENT_NUMBER = FI.INCIDENT_NUMBER
        WHERE CRIME_YEAR >= '2008'
        GROUP BY 1
        ORDER BY 1;
    """

csv2db.select_to_csv('lou_crime_database.db', crimes_select1, 'CRIMES_crime_type')
csv2db.select_to_csv('lou_crime_database.db', crimes_select2, 'CRIMES_year')
csv2db.select_to_csv('lou_crime_database.db', crimes_select3, 'CRIMES_crime_type_per_year')
csv2db.select_to_csv('lou_crime_database.db', crimes_select4, 'CRIMES_year_per_crime_type')
csv2db.select_to_csv('lou_crime_database.db', crimes_select5, 'CR_FI_firearms_by_crime_year')
