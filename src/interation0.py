import sqlite3
import uuid
#import re

connection = sqlite3.connect("ersatztv.sqlite3")
cursor = connection.cursor()

#select * from Table_Name order by Column_Name offset 234 rows fetch next 16 rows only
#plexmovies = cursor.execute("SELECT id FROM PlexMovie ORDER BY id  ASC LIMIT 6").fetchall()


plexmovies = cursor.execute("SELECT id FROM 'PlexMovie' ORDER BY id ASC").fetchall()
for movie_data in plexmovies:
    for movie_id_raw in movie_data:
        movie_id = str(movie_id_raw) 
        print("processing movie_id: "+movie_id)
        
        title_raw = cursor.execute("SELECT Title FROM MovieMetadata WHERE MovieId = "+movie_id).fetchall()[0]
        plot_raw = cursor.execute("SELECT Plot FROM MovieMetadata WHERE MovieId = "+movie_id).fetchall()[0]
        year_raw = cursor.execute("SELECT year FROM MovieMetadata WHERE MovieId = "+movie_id).fetchall()[0]
        title_year = title_raw[0]+" ("+str(year_raw[0])+")"
        '''
        print(title_raw[0])
        print(year_raw[0])
        print(plot_raw[0])
        '''

        print(title_year)
        
        # collection_id = Create a new collection with title_year
        # Create a new collection_item with collection_id 


      #  test = cursor.execute("SELECT seq FROM Sqlite_Sequence WHERE name = Library").fetchall()
        #current_seq_id = cursor.execute("select seq from sqlite_sequence WHERE name = 'PlexMovie'").fetchall()[0]
        #next_seq_id = current_seq_id[0]+1
        #print(current_seq_id[0])
        #print(next_seq_id)
        #increment_seq_id = cursor.execute("select seq from sqlite_sequence WHERE name = 'PlexMovie'").fetchall()[0]
      #  
        collection_insert = cursor.execute("INSERT INTO Collection ('Name', 'UseCustomPlaybackOrder') VALUES ('"+title_year+"', 0)")
        collection_seq_id = cursor.execute("select seq from sqlite_sequence WHERE name = 'Collection'").fetchall()[0]
        next = str(collection_seq_id[0])
        collection_item_insert = cursor.execute("INSERT INTO 'CollectionItem' ('CollectionId','MediaItemId','CustomIndex') VALUES ("+next+","+movie_id+",NULL);")
        #filler_insert = cursor.execute()
        #channel_insert = cursor.execute()

        filler_insert = cursor.execute("INSERT INTO FillerPreset ('Name','FillerKind','FillerMode','Duration','Count','PadToNearestMinute','CollectionType','CollectionId','MediaItemId','MultiCollectionId','SmartCollectionId','AllowWatermarks') VALUES ('"+title_year+"',5,0,NULL,NULL,NULL,0,"+next+",NULL,NULL,NULL,0);")
        filler_seq_id = cursor.execute("select seq from sqlite_sequence WHERE name = 'FillerPreset'").fetchall()[0]
        next = str(filler_seq_id[0])

        channel_seq_id = cursor.execute("select seq from sqlite_sequence WHERE name = 'Channel'").fetchall()[0]
        next_channel = str(channel_seq_id[0]+5)
        random_uuid = str(uuid.uuid4())
        channel_insert = cursor.execute("INSERT INTO Channel ('FFmpegProfileId','FallbackFillerId','Name','Number','PreferredAudioLanguageCode','StreamingMode','UniqueId','WatermarkId','Categories','Group','PreferredSubtitleLanguageCode','SubtitleMode','MusicVideoCreditsMode','PreferredAudioTitle','MusicVideoCreditsTemplate') VALUES  (5,'"+next+"','"+title_year+"','"+next_channel+"','',5,'"+random_uuid+"',NULL,NULL,'Movies','',0,0,NULL,NULL);")
                
        connection.commit()