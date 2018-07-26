Analysis of Louisville Crime Type Trends
========================================

## Background

To anyone closely following local news in Louisville, Kentucky, it is well known that the number of homicides in the metro area has spiked in recent years. However, I wanted to know whether this represented a rate of increase substantially greater than that of other crime types and, moreover, if there were other, overlooked types of crimes that were increasing at approximately the same rate or greater.

## Methodology

The data utilized is crime data uploaded by the Louisville Metro Police Department (LMPD) and taken from the Louisville Metro Open Data portal; for the links to the relevant pages and a copy of LMPD's terms of use for their data, please see the files in the [/data_reference/](./data_reference/) directory. I initially selected files containing all crime data per individual year for the years 2008 through 2017, as well as separate sets containing all firearm intake, officer assault, and hate crime data, respectively; the year range was selected to account for the most recent, complete 10-year span, the length of allows meaningful analysis of long-term trends without using data so old as to be irrelevant to current trends. The specialized sets were initially selected when my question was less refined; they were excluded from the final analysis in favor of using only the core crime data due to relevance.

From the raw CSV files downloaded from the portal, data is lightly cleaned for spelling and consistency and analyzed for column names and data types as are relevant for SQL table column definitions. A SQLite database is then created or opened if already present. For each type of data, existing database tables are dropped, new tables are created, and records are inserted using predefined table names and source data file names; this is first done with a temporary table and then a permanent table that selects only unique records from the temporary table to remove duplicate rows. Note that specialized firearm intake, officer assault, and hate crime data are stored in separate tables while all general crime data is merged from separate files based on year to a single `CRIMES` table.

The graphs for the final report are generated after selecting counts of crimes grouped by year of occurrence and crime type from the `CRIMES` table where the year of occurrence is 2008 or later (due to late reporting of crimes, older crimes exist in the database). This is then passed into Matplotlib plots to generate graphs relevant to the inquiry. The final report is rendered in HTML with internal links to said graphs. Some of the graphs show raw counts and calculated simple linear regressions for perspective, but the main analysis used to compare relative rate of increase was the use of an adjusted linear regression. This is calculated from the simple linear regression by dividing the simple slope by the mean of the y-values (in this case, counts of crimes) and translating (via subtraction) the function to have its x-intercept at the leftmost x-value (in this case, earliest year) for each relevant year. Thus, these adjusted linear regressions allow for easy visual comparison by displaying the average rate of increase or decrease among individual crime types relative to the mean value for each crime type in a given period.

## Instructions on Running

This project uses uncompiled Python 3.6.5 scripts, and thus Python 3.6.5 or later should be installed on the relevant machine. The `csv`, `os`, `re`, and `sqlite3` standard library modules are all used; these should be installed with Python by default. In addition, the `matplotlib` non-standard library must be installed (via `python -m pip install matplotlib` or another method) in order to render the graphs. After ensuring these dependencies are satisfied and cloning or downloading the repository, open a system shell and navigate the current working directory to the `/scripts/` subdirectory just beneath the project's top-level directory. Enter the Python shell and run `import main` to initialize the database and generate the graphs. Finally, open `report.html` in a web browser from the top-level directory.

To peruse the data via a lightweight, user-friendly GUI, downloading DB Browser for SQLite is recommended.

_**Note:**_ Due to the frequently evolving scope of my project, several artifacts remain that are ultimately unused or were only intended to be used by me before the project's conclusion. This includes the assaulted officer, firearm intake, and hate crime data, which is included in the raw data files and even imported into the database despite omission from the final report, and the `crime_db_queries.py` script, which generates some query results as CSV files that helped me shape my project. One is free to examine the results of these unused endeavors, but they are neither necessary nor intended to be packaged with the final product.

### Thanks for reviewing my project! Please let me know where I can most improve.

###### Project &copy; Colton Atticus Gurley
