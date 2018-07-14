# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 17:27:45 2018

@author: Atticus
"""

import csv2db


select1 = """
    SELECT CRIME_TYPE, COUNT(*) AS COUNT
    FROM CRIMES
    GROUP BY 1
    ORDER BY 1;
    """
select2 = """
    SELECT SUBSTR(DATE_OCCURED, 1, 4) AS YEAR, COUNT(*) AS COUNT
    FROM CRIMES
        WHERE YEAR >= '2008'
        GROUP BY 1
        ORDER BY 1;
    """
select3 = """
    SELECT SUBSTR(DATE_OCCURED, 1, 4) AS YEAR, CRIME_TYPE, COUNT(*) AS COUNT
    FROM CRIMES
        WHERE YEAR >= '2008'
        GROUP BY 1, 2
        ORDER BY 1, 2;
    """
select4 = """
    SELECT SUBSTR(DATE_OCCURED, 1, 4) AS YEAR, CRIME_TYPE, COUNT(*) AS COUNT
    FROM CRIMES
        WHERE YEAR >= '2008'
        GROUP BY 1, 2
        ORDER BY 2, 1;
    """
select5 = """
    SELECT SUBSTR(CR.DATE_OCCURED, 1, 4) AS CRIME_YEAR, COUNT(*) AS COUNT
    FROM CRIMES AS CR
    INNER JOIN FIREARM_INTAKE AS FI ON CR.INCIDENT_NUMBER = FI.INCIDENT_NUMBER
        WHERE CRIME_YEAR >= '2008'
        GROUP BY 1
        ORDER BY 1;
    """
select6 = """
    WITH DFI AS (
        SELECT DISTINCT *
        FROM FIREARM_INTAKE
    )
    SELECT SUBSTR(CR.DATE_OCCURED, 1, 4) AS CRIME_YEAR, COUNT(*) AS COUNT
    FROM CRIMES AS CR
    INNER JOIN DFI ON CR.INCIDENT_NUMBER = DFI.INCIDENT_NUMBER
        WHERE CRIME_YEAR >= '2008'
        GROUP BY 1
        ORDER BY 1;
    """
select7 = """
    WITH DCR AS (
        SELECT DISTINCT *
        FROM CRIMES
    ), DFI AS (
        SELECT DISTINCT *
        FROM FIREARM_INTAKE
    )
    SELECT SUBSTR(DCR.DATE_OCCURED, 1, 4) AS CRIME_YEAR, COUNT(*) AS COUNT
    FROM DCR
    INNER JOIN DFI ON DCR.INCIDENT_NUMBER = DFI.INCIDENT_NUMBER
        WHERE CRIME_YEAR >= '2008'
        GROUP BY 1
        ORDER BY 1;
    """
select8a = """
    SELECT COUNT(*) AS COUNT
    FROM CRIMES;
    """
select8b = """
    WITH DCR AS (
        SELECT DISTINCT *
        FROM CRIMES
    )
    SELECT COUNT(*) AS COUNT
    FROM DCR;
    """
select9a = """
    SELECT COUNT(*) AS COUNT
    FROM FIREARM_INTAKE;
    """
select9b = """
    WITH DFI AS (
        SELECT DISTINCT *
        FROM FIREARM_INTAKE
    )
    SELECT COUNT(*) AS COUNT
    FROM DFI;
    """
select10a = """
    SELECT COUNT(*) AS COUNT
    FROM HATE_CRIMES;
    """
select10b = """
    WITH DHC AS (
        SELECT DISTINCT *
        FROM HATE_CRIMES
    )
    SELECT COUNT(*) AS COUNT
    FROM DHC;
    """
select11a = """
    SELECT COUNT(*) AS COUNT
    FROM OFFICER_ASSAULTS;
    """
select11b = """
    WITH DOA AS (
        SELECT DISTINCT *
        FROM OFFICER_ASSAULTS
    )
    SELECT COUNT(*) AS COUNT
    FROM DOA;
    """

csv2db.select_to_csv('lou_crime_database.db', select1, 'CRIMES_crime_type')
csv2db.select_to_csv('lou_crime_database.db', select2, 'CRIMES_year')
csv2db.select_to_csv('lou_crime_database.db', select3, 'CRIMES_crime_type_per_year')
csv2db.select_to_csv('lou_crime_database.db', select4, 'CRIMES_year_per_crime_type')
csv2db.select_to_csv('lou_crime_database.db', select5, 'CR_FI_firearms_by_crime_year')
csv2db.select_to_csv('lou_crime_database.db', select6, 'CR_DFI_firearms_by_crime_year')
csv2db.select_to_csv('lou_crime_database.db', select7, 'DCR_DFI_firearms_by_crime_year')
csv2db.select_to_csv('lou_crime_database.db', select8a, 'CR_count')
csv2db.select_to_csv('lou_crime_database.db', select8b, 'DCR_count')
csv2db.select_to_csv('lou_crime_database.db', select9a, 'FI_count')
csv2db.select_to_csv('lou_crime_database.db', select9b, 'DFI_count')
csv2db.select_to_csv('lou_crime_database.db', select10a, 'HC_count')
csv2db.select_to_csv('lou_crime_database.db', select10b, 'DHC_count')
csv2db.select_to_csv('lou_crime_database.db', select11a, 'OA_count')
csv2db.select_to_csv('lou_crime_database.db', select11b, 'DOA_count')
