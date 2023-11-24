import sqlite3
import uuid
import re
import os

# Get the DB Name from env variable ERSATZTV_DB = if not set use default
try:
  DB = os.getenv('ERSATZTV_DB') # None
except IOError:
  DB = "ersatztv.sqlite3"  
else:
  DB = "ersatztv.sqlite3"  
finally:
  connection = sqlite3.connect(DB)

#connection = sqlite3.connect("ersatztv.sqlite3")
cursor = connection.cursor()

  
#current starting point is iterate all Plex movies
plexmovies = cursor.execute("SELECT id FROM 'PlexMovie' ORDER BY id ASC").fetchall()
for movie_data in plexmovies:
  for movie_id_raw in movie_data:
    movie_id = str(movie_id_raw) 
    print("processing movie_id: "+movie_id)
    
    title_raw = cursor.execute("SELECT Title FROM MovieMetadata WHERE MovieId = "+movie_id).fetchall()[0]
    plot_raw = cursor.execute("SELECT Plot FROM MovieMetadata WHERE MovieId = "+movie_id).fetchall()[0]
    year_raw = cursor.execute("SELECT year FROM MovieMetadata WHERE MovieId = "+movie_id).fetchall()[0]
    title_year = title_raw[0]+" ("+str(year_raw[0])+")"
    title_escaped = title_year.replace("'", "")
    title_year = title_escaped 
    
    print("processing movie_id: "+movie_id+" - "+title_year)


    exists = cursor.execute("SELECT id FROM 'Collection' WHERE NAME = '"+title_year+"").fetchall()[0]
'''
    try:
      exists = cursor.execute("SELECT id FROM 'Collection' WHERE NAME = '"+title_year+"").fetchall()[0]
      print(exists)
    except:
      print("new")
       '''
       
    '''
    print(title_raw[0])
    print(year_raw[0])
    print(plot_raw[0])
    '''

    '''debug out

    # Create an empty collection using the movie title and year
    collection_insert = cursor.execute("INSERT INTO Collection ('Name', 'UseCustomPlaybackOrder') VALUES ('"+title_year+"', 0)")
    
    # Obtain the collection_id by getting the auto-incremented Id - and convert it to a string
    collection_seq_id = cursor.execute("select seq from sqlite_sequence WHERE name = 'Collection'").fetchall()[0]
    next = str(collection_seq_id[0])
    
    # using rhe collection_seq_id from above, and the movie_id, add the movie to the collection
    collection_item_insert = cursor.execute("INSERT INTO 'CollectionItem' ('CollectionId','MediaItemId','CustomIndex') VALUES ("+next+","+movie_id+",NULL);")

    # so that we can use it as a channel that starts upon switching to it; it always plays end to end forever
    filler_insert = cursor.execute("INSERT INTO FillerPreset ('Name','FillerKind','FillerMode','Duration','Count','PadToNearestMinute','CollectionType','CollectionId','MediaItemId','MultiCollectionId','SmartCollectionId','AllowWatermarks') VALUES ('"+title_year+"',5,0,NULL,NULL,NULL,0,"+next+",NULL,NULL,NULL,1);")

    # get the autoincremenet Filler Preset Id
    filler_seq_id = cursor.execute("select seq from sqlite_sequence WHERE name = 'FillerPreset'").fetchall()[0]
    next = str(filler_seq_id[0])
    
    # force a commit so that creating the channel doesn't fail whenever it detects my happiness 
    connection.commit()

    # we're now going to create a new channel with the next channel number, using the created collection
    # This doesnt have a schedule just loops over and over at the moment
    
    channel_seq_id = cursor.execute("select seq from sqlite_sequence WHERE name = 'Channel'").fetchall()[0]
    next_channel = str(channel_seq_id[0]+1)
    random_uuid = str(uuid.uuid4())
    channel_insert = cursor.execute("INSERT INTO Channel ('FFmpegProfileId','FallbackFillerId','Name','Number','PreferredAudioLanguageCode','StreamingMode','UniqueId','WatermarkId','Categories','Group','PreferredSubtitleLanguageCode','SubtitleMode','MusicVideoCreditsMode','PreferredAudioTitle','MusicVideoCreditsTemplate') VALUES  (1,'"+next+"','"+title_year+"','"+next_channel+"',NULL,1,'"+random_uuid+"',1,NULL,'Movies','',0,0,NULL,NULL);")
        
    connection.commit()
'''