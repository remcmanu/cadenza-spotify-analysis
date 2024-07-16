### 
 # file            spotify.py
 # authors         Robert McManus
 # github          @remcmanu
 # date            2024-01-09
 # description     Converts Spotify data .json files to .csv, removing duplicates
 #
 # sources:
 #  
 #  
###

import os
import pandas as pd


def create_csv_files(*args):
    'Process multiple input JSON files into respective output CSV files'

    combined_json_df = None
    for file in os.listdir('.'):
        if file.lower().endswith('.json'):
            # Read JSON file into Pandas DataFrame, then combine
            file_df = pd.read_json(file)
            combined_json_df = pd.concat([combined_json_df, file_df], ignore_index=True)

    # Remove duplicates based on all columns
    combined_json_df.drop_duplicates(inplace=True)

    # Convert 'endTime' to datetime for easier manipulation
    combined_json_df['endTime'] = pd.to_datetime(combined_json_df['endTime'])

    # Split data into separate DataFrames based on years
    for year, year_data in combined_json_df.groupby(combined_json_df['endTime'].dt.year):
        filename = f'spotify_data_{year}.csv'

        # if the file exists, merge into existing data
        if os.path.isfile(filename):
            # Read the existing data from the CSV file
            existing_data = pd.read_csv(filename)
            # Convert back to datetime to compare with year_data
            existing_data['endTime'] = pd.to_datetime(existing_data['endTime'], format='%Y-%m-%d %H:%M:%S')
            # Concatenate the existing_data with year_data
            combined_existing_and_year_data = pd.concat([existing_data, year_data], ignore_index=True)
            # Remove duplicates based on all columns
            combined_existing_and_year_data.drop_duplicates(inplace=True)
            # sort by date descending
            combined_existing_and_year_data.sort_values('endTime', ascending = True, inplace = True)
            # Save the updated unique entries back to the same file
            combined_existing_and_year_data.to_csv(filename, index=False)

        # if the file doesn't exist, save year_data directly
        else:
            year_data.sort_values('endTime', ascending = True, inplace = True)
            year_data.to_csv(f'spotify_data_{year}.csv', index=False)

    return 0

if __name__ == '__main__':
    create_csv_files()