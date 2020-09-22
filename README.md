# Coding Test

## Installation
The following code was run using Python 3.7.3  

Install Mongodb, I used Mongodb 4.0.20 community edition
https://docs.mongodb.com/v4.0/administration/install-community/  
  
Install requirements: 
 ```
pip install -r requirements.txt 
 ```
 
## Get data
 Get some data to put in the database (you can download multiple files if desired):  
 ```
 wget ftp://ftp.ais.dk/ais_data/aisdk_20181101.csv
 ```
 
 ## Insert data and generate report
 ```
 python main.py --files <downloaded files>  
 ```
 Example:
 ```
 python main.py --files aisdk_20181101.csv
 ```
  
 To only generate a report leave out the --files flag
  
  ## Output
  The generated report:
  ```
{   'missing_count': {   'A': 29691,
                         'B': 29712,
                         'C': 29981,
                         'COG': 5861,
                         'Callsign': 29117,
                         'Cargo type': 49993,
                         'D': 29970,
                         'Data source type': 1,
                         'Destination': 34551,
                         'Draught': 33837,
                         'ETA': 37157,
                         'Heading': 11874,
                         'IMO': 39682,
                         'Latitude': 1,
                         'Length': 29624,
                         'Longitude': 1,
                         'MMSI': 1,
                         'Name': 28378,
                         'Navigational status': 8594,
                         'ROT': 15753,
                         'SOG': 3865,
                         'Ship type': 29813,
                         'Timestamp': 0,
                         'Type of mobile': 0,
                         'Type of position fixing device': 28094,
                         'Width': 29645},
    'stats': {   'Cargo type': {   'Category OS': 138,
                                   'Category X': 888,
                                   'Category Y': 573,
                                   'Category Z': 44,
                                   'No additional information': 3338,
                                   'Reserved for future use': 238},
                 'Data source type': {'AIS': 55211},
                 'Navigational status': {   'Aground': 3,
                                            'At anchor': 265,
                                            'Constrained by her draught': 181,
                                            'Engaged in fishing': 7571,
                                            'Moored': 1537,
                                            'Not under command': 110,
                                            'Reserved for future amendment [HSC]': 309,
                                            'Reserved for future amendment [WIG]': 46,
                                            'Reserved for future use [11]': 43,
                                            'Restricted maneuverability': 2256,
                                            'Under way sailing': 765,
                                            'Under way using engine': 33532},
                 'Ship type': {   'Anti-pollution': 18,
                                  'Cargo': 5724,
                                  'Diving': 78,
                                  'Dredging': 891,
                                  'Fishing': 6851,
                                  'HSC': 333,
                                  'Law enforcement': 71,
                                  'Medical': 25,
                                  'Military': 205,
                                  'Other': 1631,
                                  'Passenger': 3075,
                                  'Pilot': 1019,
                                  'Pleasure': 393,
                                  'Port tender': 34,
                                  'Reserved': 118,
                                  'SAR': 998,
                                  'Sailing': 321,
                                  'Spare 1': 17,
                                  'Spare 2': 4,
                                  'Tanker': 2256,
                                  'Towing': 135,
                                  'Towing long/wide': 17,
                                  'Tug': 1183,
                                  'WIG': 2},
                 'Type of mobile': {   'AtoN': 255,
                                       'B': 1,
                                       'Base Station': 2626,
                                       'Class A': 50565,
                                       'Class B': 1765},
                 'Type of position fixing device': {   'Combined GPS/GLONASS': 346,
                                                       'GLONASS': 41,
                                                       'GPS': 23716,
                                                       'Integrated navigation system': 76,
                                                       'Internal': 1914,
                                                       'Loran-C': 2,
                                                       'Surveyed': 1023}},
    'timestamp': 1600780150.870621}
  ```   
  
  missing_count contains the missing count for all fields.
  stats_contains distinct value count for all fields which where apropriate
  
  ## Summary of the structure, approach
  The reason I chose the database structure stems from the reasons:  
  
  1. I noticed that most of the columns had empty values, which would suggest that a table structure is not the optimal data structure for this data. With a document structure, I am free to only add fields that have data for each document and create sparse indexes for documents that contain those fields.
  
  2. Inspecting the Timestamp field it is clear that if a future case of streaming data there would fast continuous updates, I, therefore, think it is a good idea to optimize for better write performance which this document structure allows for.
  
  3. It seems like many of the columns in the dataset act as placeholders and only contains information for some specific type of ships. Considering this I think it is quite likely that extra columns can be added in the future to contain specific information for som new ship class. It is then good that the datastructe allows for such updates.
  
  I, therefore, choose a document structure database and created sparse indexes only for existing fields.
  The ETL pipeline used pandas because of the ease in which you can load csv files, replace different types of undefined values, and then convert it to a filtered dict.
  
  ## Areas of improvement
  1. There is currently no check for uniqueness when inserting the data, so it is now possible to insert the same data multiple times. An easy way to solve this would be to create a unique composite index for timestamp + ship_id.
  
  2. Location is now stored as floats, MongoDb supports the GEO JSON format which allows you to preform location querries easily, and update would be to add location on this format instead.
  
  3. Timestamp field is unclear, a much better way would be to define the timestamp as a Unix timestamp in milliseconds. This would solve the problem of uncertainty when dealing with dates and not defined timezones.
  
  4. No parallelism for the ETL or report generation
  
