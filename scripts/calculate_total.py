import os
import argparse
import pandas as pd
from datetime import datetime

# Function to calculate total time
def calculate_total_time(
        songs, artist, start, end=None, time_format='minutes'
):
    # """ Calculate total time spent listening to song(s)

    #     Parameters:
    #         - songs - 
    # """
    
    'Calculate total time spent listening to song(s)'
    
    df = None
    # if no start, use every CSV file
    if start is None:
        for file in os.listdir('.'):
            if file.lower().endswith('.csv'):
                year_df = pd.read_csv(file)
                df = pd.concat([df, year_df], ignore_index=True)
    
    # else, figure out the range and only use those
    elif start is not None:
        start_year = start.year
        end_year = end.year
        filename = None
        for i in range(start_year, end_year + 1):
            filename = f'spotify_data_{i}.csv'
            if not os.path.isfile(filename):
                print(f'There was an error opening the file {filename}!')
                return
            year_df = pd.read_csv(filename)
            df = pd.concat([df, year_df], ignore_index=True)
    
    songs_df = None
    # if artist, get list of all there songs
    if artist is not None:
        songs_df = df[df['artistName'] == artist]
    
    # if songs
    if songs is not None:
        for song in songs:
            song_df = df[df['trackName'] == song]
            songs_df = pd.concat([songs_df, song_df], ignore_index=True)
    
    # get time factor based on format
    time_factor = None
    match time_format:
      case "minutes":
        time_factor = 1000 * 60 
      case "hours":
        time_factor =  1000 * 60 * 60
      case "days":
        time_factor = 1000 * 60 * 60 * 24

    # print sums, descending
    total_time = 0
    sum_df = songs_df.groupby(['artistName', 'trackName'])['msPlayed'].sum().reset_index()
    sum_df = sum_df.sort_values('msPlayed', ascending = False)
    for index, row in sum_df.iterrows():
        total_time += row['msPlayed'] 
        print(f"Track: {row['trackName']}, Artist: {row['artistName']}, Total msPlayed: {round(row['msPlayed'] / time_factor, 2)} {time_format}")
    print(f"Total time played: {round(total_time / time_factor, 2)} {time_format}")
    
    return 0

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description = 'Calculate total time for songs or an artist')

    # Define mutually exclusive group for songs or artist
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('--songs', nargs = '+', help = 'One or more song names')
    group.add_argument('--artist', help = 'Name of the artist')

    # Optional arguments
    parser.add_argument('--range', action = 'store_true', help = 'Use range for tracking')
    parser.add_argument('--start', default = None, help = 'Start datetime for tracking')
    parser.add_argument('--end', default = None, help = 'End datetime for tracking')
    parser.add_argument('--format', choices = ['hours', 'days'], default = 'minutes', help = 'Display format')

    args = parser.parse_args()

    # Convert start and end strings to datetime objects
    start_datetime = datetime.strptime(args.start, '%Y-%m-%d %H:%M') if args.start is not None else None
    end_datetime = datetime.strptime(args.end, '%Y-%m-%d %H:%M') if args.end is not None else datetime.now()

    # Perform the calculations based on provided arguments
    return calculate_total_time(args.songs, args.artist, start_datetime, end_datetime, args.format)

if __name__ == '__main__':
    main()