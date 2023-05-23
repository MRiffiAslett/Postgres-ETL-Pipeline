import os
import glob
import psycopg2
import pandas as pd
from Queries import *


def process_song_file(cur, filepath):
    # Open the song file
    """This function reads the songs log file row by row, selects the required fields, and inserts them into the song and artist tables.
        Parameters:
            cur (psycopg2.cursor()): Cursor of the sparkifydb database
            filepath (str): The filepath of the file to be analyzed
    """
    df = pd.read_json(filepath, lines=True)
    
    for value in df.values:
        num_songs, artist_id, artist_latitude, artist_longitude, artist_location, artist_name, song_id, title, duration, year = value

    
    # Insert the artist record
    artist_data = artist_id, artist_name, artist_location, artist_latitude, artist_longitude
    cur.execute(artist_table_insert, artist_data)
    
      # Insert the song record
    song_data = song_id, title, artist_id, year, duration
    cur.execute(song_table_insert, song_data)
    

def process_log_file(cur, filepath):
    # Open the log file
    """"This function reads the user activity log file row by row, filters by NexSong, selects the required fields, transforms them, and inserts them into the time, users, and songplays tables.
            Parameters:
                cur (psycopg2.cursor()): Cursor of the sparkifydb database
                filepath (str): The filepath of the file to be analyzed
    """
    df = pd.read_json(filepath, lines=True)

    # Filter by the NextSong action
    df = df[df['page'] == 'NextSong']

    # Convert the timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # Insert the time data records
    time_data = []
    for line in t:
        time_data.append([line, line.hour, line.day, line.week, line.month, line.year, line.day_name()])
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')

    time_df = pd.DataFrame(time_data, columns=column_labels)

    time_df = pd.DataFrame.from_records(time_data, columns=column_labels)
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # Load the user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']] 

    # Insert the user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # Insert the songplay records
    for index, row in df.iterrows():
        
        # Get the songid and artistid from the song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # Insert the songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), int(row.userId), row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)

def process_data(cur, conn, filepath, func):
    # Get all the files matching the extension from the directory   
    """This function walks through all the files nested under the specified filepath and processes all the logs found.
    Parameters:
        cur (psycopg2.cursor()): The sparkifydb database cursor
        conn (psycopg2.connect()): The connection to the sparkifycdb database
        filepath (str): The parent filepath of the logs to be analyzed
        func (python function): The function to be used to process each log
    Returns:
        The name of the processed files
    """
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # Get the total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # Iterate over the files and process them
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))

    """This function is used to extract and transform all the data from the song and user activity logs and load it into a PostgreSQL DB.
    """
def main():

    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres password=Datascience1*")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
