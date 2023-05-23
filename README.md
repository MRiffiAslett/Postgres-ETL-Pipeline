# Sparkify PostgreSQL ETL

## Data Modeling with Postgres
- The data will be modeled using a star schema in PostgreSQL, which consists of one fact table and four dimension tables.
- The star schema is suitable for this analysis as it simplifies queries and enables efficient aggregation of data.

## Database Schema
The schema used in this project is as follows:

### Fact Table
***songplays*** - Records in log data associated with song plays (page: NextSong)

- `songplay_id` (INT) PRIMARY KEY: ID of each user song play
- `start_time` (TIMESTAMP) NOT NULL: Timestamp of user activity start
- `user_id` (INT) NOT NULL: ID of user
- `level` (TEXT): User level (free/paid)
- `song_id` (TEXT) NOT NULL: ID of played song
- `artist_id` (TEXT) NOT NULL: ID of song artist
- `session_id` (INT): ID of user session
- `location` (TEXT): User location
- `user_agent` (TEXT): User agent used to access the Sparkify platform

### Dimension Tables
***users*** - Users in the app

- `user_id` (INT) PRIMARY KEY: ID of user
- `first_name` (TEXT) NOT NULL: First name of user
- `last_name` (TEXT) NOT NULL: Last name of user
- `gender` (TEXT): Gender of user (M/F)
- `level` (TEXT): User level (free/paid)

***songs*** - Songs in music database

- `song_id` (TEXT) PRIMARY KEY: ID of song
- `title` (TEXT) NOT NULL: Title of song
- `artist_id` (TEXT) NOT NULL: ID of song artist
- `year` (INT): Year of song release
- `duration` (FLOAT) NOT NULL: Duration of song in milliseconds

***artists*** - Artists in music database

- `artist_id` (TEXT) PRIMARY KEY: ID of artist
- `name` (TEXT) NOT NULL: Name of artist
- `location` (TEXT): Location of artist
- `latitude` (FLOAT): Latitude location of artist
- `longitude` (FLOAT): Longitude location of artist

***time*** - Timestamps of records in songplays broken down into specific units

- `start_time` (TIMESTAMP) PRIMARY KEY: Timestamp of record
- `hour` (INT): Hour associated with start_time
- `day` (INT): Day associated with start_time
- `week` (INT): Week of year associated with start_time
- `month` (INT): Month associated with start_time
- `year` (INT): Year associated with start_time
- `weekday` (TEXT): Name of weekday associated with start_time

## ETL Pipeline using Python
The ETL (Extract, Transform, Load) pipeline is implemented in Python and follows the following steps:

1. Database and tables are created using the provided SQL statements in `sql_queries.py`.

2. The song data is processed and loaded into the `songs` and `artists` dimension tables.

3. The log data is processed and loaded into the `time` and `users` dimension tables. 

4. The `songplays` fact table is populated by querying the `songs` and `artists` tables to obtain the respective IDs based on song information.

5. The ETL process is performed for all files in the song and log datasets.

6. The ETL pipeline is executed by running `etl.py` script.

# Project Structure

The project includes the following files:

- `data` folder: Contains the JSON files of song and log data.
- `Queries.py`: Includes all the SQL queries required for creating tables, inserting data, and performing other operations.
- `Table_generator.py`: Drops and creates the tables defined in the schema using the queries from `queries.py`.
- `etl.py`: The Python script that performs the ETL process for all files in the song and log datasets. It reads the data, transforms it, and loads it into the appropriate tables.
- `README.md`: The current file, which provides an overview of the project, its structure, and the ETL pipeline.

## Steps to Run the Project

1. Run `Table_generator.py` to create the database and tables required for the ETL process.
2. Verify the tables by running `test.ipynb` and checking the first few rows of each table.
3. Execute `etl.py` to perform the ETL pipeline and populate the tables with the data from the song and log datasets.

By following these steps, you will successfully create a database schema and perform the ETL process to analyze Sparkify's song and user activity data.
