# spotify-data-analysis
Tools to analyze personal Spotify data. (I'm also storing my data here, which is probably not useful for anyone else)

## To Use

1. Request your data from Spotify: https://www.spotify.com/us/account/privacy/
2. Unzip `my_spotify_data.zip`, which should be emailed a few days after your request, to create the `MyData` directory. 
3. Therein, open `StreamingHistory0` and `StreamingHistory1`.
4. If you already have a file for the CURRENT_YEAR, according to the format `historyCURRENT_YEAR.json`, skip to step 5. Otherwise, create separate .json files for each year for which you have data.

    This could look like:
      ```
        history2020.json
        history2021.json
        history2022.json
      ```

5. When adding new data from subsequent data requests, open `StreamingHistory0.json` and figure out where its first entry places in the existing file for that given year. I recommend using "Find on page", and searching by `msPlayed`, as this number will often be unique (and if not, uncommon). 

      `StreamingHistory1.json` will begin directly after the last entry of `StreamingHistory0.json`, making it much simpler.

      *TODO: Streamline this process with a function. I tried to do this in v2.0 but it was too difficult.*

6. Ensure that JSON format is maintained. For example below, when adding "Drink the Water" from another file, you'd have to first add a comma to the previous end of the file, "Dreams Tonite". Next, paste "Drink the Water" below, ensuring there is still a closing bracket at the end of the file.

      ```
        {
          "endTime" : "2020-06-27 22:55",
          "artistName" : "Alvvays",
          "trackName" : "Dreams Tonite",
          "msPlayed" : 195944
        }**,**                                        <--- REMEMBER TO ADD THIS COMMA
        {                                             <--- ALL CURLY BRACES SHOULD ALIGN
          "endTime" : "2020-06-28 01:43",
          "artistName" : "Eisley",
          "trackName" : "Drink the Water",
          "msPlayed" : 4317
        }                                             <--- THIS CURLY BRACE SHOULD BE ABOVE THE ENDING BRACKET
      ]
      ```


## Functions

### songs_sum(year1, mode="lifetime", decimal_place=2)
    
   *Find the amount of time you listened to songs in Spotify for a single year, or for all years which you have data for.*
    
   *Time calculated in miliseconds (ms), minutes (m), hours (h), with total listen time in days (d).*
    
#### Arguments
    - year1: either the single year (mode="year"); or the first year of data (mode="lifetime")
    - mode: valid inputs are "year" for calculating a single year's listening, or "lifetime" for cumulative listening in the range \[starting year, current year]
    - decimal_place: the number of digits specified after the decimal

*Example Output:*
```
  Virkelighetens Etterklang by Kalandra
      15560827ms 259.35m 4.32h
  The Waiting Game by Kalandra
      17370921ms 289.52m 4.83h
  Runaway by AURORA
      17536437ms 292.27m 4.87h
  All Is Soft Inside by AURORA
      18983523ms 316.39m 5.27h
  It Gets Easier by Kalandra
      19080974ms 318.02m 5.3h
  Í Tokuni by Eivør
      19140217ms 319.0m 5.32h
  Slow Motion by Kalandra
      20047137ms 334.12m 5.57h
  Borders by Kalandra
      22024639ms 367.08m 6.12h
  Brave New World by Kalandra
      22765254ms 379.42m 6.32h
  Helvegen by Kalandra
      28661044ms 477.68m 7.96h
  TOTAL:  51.31d
```

### artists_sum(year1, mode="lifetime", decimal_place=2)

   *Find the amount of time you listened to artists in Spotify for a single year, or for all years which you have data for.*
    
   *Time calculated in miliseconds (ms), minutes (m), hours (h), with total listen time in days (d).*
    
#### Arguments
    - year1: either the single year (mode="year"); or the first year of data (mode="lifetime")
    - mode: valid inputs are "year" for calculating a single year's listening, or "lifetime" for cumulative listening in the range \[starting year, current year]
    - decimal_place: the number of digits specified after the decimal

*Example Output:*
```
  BENEE
      62045446ms 1034.09m 17.23h
  Menke
      71656300ms 1194.27m 19.9h
  C418
      75538078ms 1258.97m 20.98h
  Alice et Moi
      84333351ms 1405.56m 23.43h
  Cherry Glazerr
      96767069ms 1612.78m 26.88h
  Kero Kero Bonito
      130701079ms 2178.35m 36.31h
  Eivør
      148177271ms 2469.62m 41.16h
  Skott
      162602217ms 2710.04m 45.17h
  Kalandra
      242256865ms 4037.61m 67.29h
  AURORA
      375465000ms 6257.75m 104.3h
  TOTAL:  51.31d
```
