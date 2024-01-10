### 
 # file            spotify.py
 # authors         Robert McManus
 # github          @remcmanu
 # date            2024-1-9
 # description     A program to analyze spotify data.
 #
 # sources:
 #  https://docs.python.org/3/library/cmd.html#cmd.Cmd.cmdloop
 #  
###

import os
import cmd
import time
import datetime as dt
import pandas as pd
import json

class CadenzaShell(cmd.Cmd):
  intro = "Welcome to Cadenza.    Type help or ? to list commands.\n"
  prompt = "(cadenza) "
  file = None

  def do_EOF(self, arg):
    '^Z + return'
    return True

  def do_create_csv(self, arg):
    'Turns StreamingHistory files into .csv files sorted by year.'
    create_csv(*parse(arg))
  
  def do_song_analysis(self, arg):
    'Analyze song data to calculate total listen time.'
    # Call the song_analysis method with the parsed arguments
    args = parse(arg)

    if len(args) < 1:
      print(f"Requires at least 1 argument (song title)!")
      return
    
    song_analysis(*args)
  
def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(arg.split())

###          ###
 # CREATE CSV #
###          ###
def create_csv(*args):
  'Process multiple input JSON files into respective output CSV files'
  
  if not len(args) > 0:
    print(f"Requires at least 1 argument!")
    return
  
  combined_json_df = None
  for filename in args:
    # if not a json file, fail quietly
    if not filename.lower().endswith('.json'):
      print(f"{filename} did not end in .json!")
      return
    # if file not in directory, fail quietly
    if not os.path.isfile(filename):
      print('There was an error opening the file!')
      return
    
    # Read JSON file into Pandas DataFrame, then combine
    file_df = pd.read_json(filename)
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
      # Save the updated unique entries back to the same file
      combined_existing_and_year_data.to_csv(filename, index=False)

    # if the file doesn't exist, save year_data directly
    else:
      year_data.to_csv(f'spotify_data_{year}.csv', index=False)


###             ###
 # SONG ANALYSIS #
###             ###
def song_analysis(song_title, year=None, beginning=None, end=None, format='minutes'):
  'Calculate total time spent listening to a song in given year / all time'

  if song_title == None:
    print(f"Requires at least 1 argument (song title)!")
    return
  
  df = None
  if not year == None:
    filename = f'spotify_data_{year}.csv'
    if not os.path.isfile(filename):
      print('There was an error opening the file!')
      return
    df = pd.read_csv(filename)
  
  else:
    for file in os.listdir('.'):
      if file.lower().endswith('.csv'):
        next_df = pd.read_csv(file)
        df = pd.concat([df, next_df], ignore_index=True)

  filtered_rows = df[df['trackName'] == song_title]
  total_ms_played = filtered_rows['msPlayed'].sum()
  
  # Get total time given format
  total_time = None
  match format:
    case "minutes":
      total_time = total_ms_played / 1000 / 60 
    case "hours":
      total_time = total_ms_played / 1000 / 60 / 60
    case "days":
      total_time = total_ms_played / 1000 / 60 / 60 / 24
  
  print(f"Total time played for '{song_title}': {total_time} {format}")




def songs_sum(year1, mode="lifetime", decimal_place=2):
  """Find the amount of time you listened to given songs in Spotify (total/per year).\n  mode="lifetime" (where year1 is first file's year)\n  mode="year" (where year1 is single year)\n decimal_place=#s after decimal"""
  
  today = dt.today() # https://www.geeksforgeeks.org/python-program-to-print-current-year-month-and-day/
  current_year = today.year

  sums = {}
  total = 0
  
  if (mode == "lifetime"): # year1 = first file's year
    year2 = current_year + 1
  elif (mode == "year"): # year1 = year to analyze
    year2 = year1 + 1
  
  # for each year file
  for n in range(year1, year2):
    f = open('history' + str(n) + '.json', 'r') # https://www.tutorialspoint.com/file-objects-in-python
    data = json.load(f) # https://www.geeksforgeeks.org/read-json-file-using-python/
    # for each json entry
    for i in data:
      total += i['msPlayed']
      combinedStr = i['trackName'] + " by " + i['artistName']
      # add to existing, or create new entry
      if (combinedStr in sums):
        sums[combinedStr] = sums[combinedStr] + i['msPlayed']
      else:
        sums[combinedStr] = i['msPlayed']
    f.close() # https://www.tutorialspoint.com/python/file_close.htm
  
  sorted_sum = sorted(sums.items(), key = lambda x: x[1], reverse = False) # https://careerkarma.com/blog/python-sort-a-dictionary-by-value/
  
  for i in sorted_sum:
    print(i[0])
    print("    " + str(round(i[1], decimal_place)) + "ms", str(round(i[1] / 60000, decimal_place)) + "m", str(round(i[1] / 3600000, decimal_place)) + "h")
  print("TOTAL: ", str(round(total / 86400000, decimal_place)) + "d")


def artists_sum(year1, mode="lifetime", decimal_place=2):
  """Find the amount of time you listened to given artists in Spotify (total/per year).\n  mode="lifetime" (where year1 is first file's year)\n  mode="year" (where year1 is single year)\n decimal_place=#s after decimal"""
  
  today = dt.today()
  current_year = today.year

  sums = {}
  total = 0

  if (mode == "lifetime"): # year1 = first file's year
    year2 = current_year + 1
  elif (mode == "year"): # year1 = year to analyze
    year2 = year1 + 1
  
  # for each file
  for n in range(year1, year2):
    f = open('history' + str(n) + '.json', 'r')
    data = json.load(f)
    # for each json entry
    for i in data:
      total += i['msPlayed']
      artistName = i['artistName']
      # add to existing, or create new entry
      if (artistName in sums):
        sums[artistName] = sums[artistName] + i['msPlayed']
      else:
        sums[artistName] = i['msPlayed']
    f.close()
  
  sorted_sum = sorted(sums.items(), key = lambda x: x[1], reverse = False)
  
  for i in sorted_sum:
    print(i[0])
    print("    " + str(round(i[1], decimal_place)) + "ms", str(round(i[1] / 60000, decimal_place)) + "m", str(round(i[1] / 3600000, decimal_place)) + "h")
  print("TOTAL: ", str(round(total / 86400000, decimal_place)) + "d")

if __name__ == '__main__':
  CadenzaShell().cmdloop()