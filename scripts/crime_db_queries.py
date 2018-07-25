# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 17:27:45 2018

@author: Atticus
"""

import csv2db
import os


if not os.path.exists('../queries'):
    os.mkdir('../queries')

select1 = """
    SELECT CRIME_TYPE, COUNT(*) AS COUNT
    FROM CRIMES
    GROUP BY 1
    ORDER BY 1;
    """
select2 = """
    SELECT SUBSTR(DATE_OCCURRED, 1, 4) AS YEAR, COUNT(*) AS COUNT
    FROM CRIMES
        WHERE YEAR >= '2008'
        GROUP BY 1
        ORDER BY 1;
    """
select3 = """
    SELECT SUBSTR(DATE_OCCURRED, 1, 4) AS YEAR, CRIME_TYPE, COUNT(*) AS COUNT
    FROM CRIMES
        WHERE YEAR >= '2008'
        GROUP BY 1, 2
        ORDER BY 1, 2;
    """
select4 = """
    SELECT SUBSTR(DATE_OCCURRED, 1, 4) AS YEAR, CRIME_TYPE, COUNT(*) AS COUNT
    FROM CRIMES
        WHERE YEAR >= '2008'
        GROUP BY 1, 2
        ORDER BY 2, 1;
    """
select5 = """
    SELECT SUBSTR(CR.DATE_OCCURRED, 1, 4) AS CRIME_YEAR, COUNT(*) AS COUNT
    FROM CRIMES AS CR
    INNER JOIN FIREARM_INTAKE AS FI ON CR.INCIDENT_NUMBER = FI.INCIDENT_NUMBER
        WHERE CRIME_YEAR >= '2008'
        GROUP BY 1
        ORDER BY 1;
    """
select6 = """
    SELECT COUNT(*) AS COUNT
    FROM CRIMES;
    """
select7 = """
    SELECT COUNT(*) AS COUNT
    FROM FIREARM_INTAKE;
    """
select8 = """
    SELECT COUNT(*) AS COUNT
    FROM HATE_CRIMES;
    """
select9 = """
    SELECT COUNT(*) AS COUNT
    FROM OFFICER_ASSAULTS;
    """

csv2db.select_to_csv('../lou_crime_database.db', select1, '../queries/CR_crime_type')
csv2db.select_to_csv('../lou_crime_database.db', select2, '../queries/CR_year')
csv2db.select_to_csv('../lou_crime_database.db', select3, '../queries/CR_crime_type_per_year')
csv2db.select_to_csv('../lou_crime_database.db', select4, '../queries/CR_year_per_crime_type')
csv2db.select_to_csv('../lou_crime_database.db', select5, '../queries/CR_FI_firearms_by_crime_year')
csv2db.select_to_csv('../lou_crime_database.db', select6, '../queries/CR_count')
csv2db.select_to_csv('../lou_crime_database.db', select7, '../queries/FI_count')
csv2db.select_to_csv('../lou_crime_database.db', select8, '../queries/HC_count')
csv2db.select_to_csv('../lou_crime_database.db', select9, '../queries/OA_count')
