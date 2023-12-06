# Scan Shows
# Create one channel per episode "Show Name (YYYY) SXXEXX - Episode Title"
# - create collection containing MediaItem
# - create FillerPreset containing collection
# - create Channel from FillerPreset
# Group episodes under "Show Name (YYYY)"
# Yeah really rough version, but worked on raw run and re-run without duplication
# a bit more tweaking and I'll make purdy yee-haw 


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

cursor = connection.cursor()

def get_show_title(ShowId):
    #print(ShowId)
    ShowMetadata = cursor.execute("SELECT Title, Year FROM 'ShowMetadata' WHERE ShowId = "+str(ShowId)).fetchone()
    ShowTitle_raw = ShowMetadata[0]+" ("+str(ShowMetadata[1])+")"
    ShowTitle = ShowTitle_raw.replace("'","")
    return ShowTitle

def get_show_seasons(ShowId):
    #print(ShowId)
    ShowSeasons = cursor.execute("SELECT Id FROM 'Season' WHERE ShowId = "+str(ShowId)).fetchall()
    return ShowSeasons

def get_season_number(SeasonId):
    ShowSeason = cursor.execute("SELECT SeasonNumber from 'Season' WHERE Id = "+str(SeasonId)).fetchall()
    return ShowSeason

def get_season_episodes(SeasonId):
    SeasonEpisodes = cursor.execute("SELECT Id FROM 'Episode' WHERE SeasonId = "+str(SeasonId)).fetchall()
    return SeasonEpisodes

def get_episode_metadata(EpisodeId):
    EpisodeMetadata = cursor.execute("SELECT EpisodeNumber, Title FROM 'EpisodeMetadata' WHERE EpisodeId = "+str(EpisodeId)).fetchone()
    return EpisodeMetadata

def create_collection(EpisodeLabel):
    try:
      exists = cursor.execute("SELECT id FROM 'Collection' WHERE NAME = '"+EpisodeLabel+"'").fetchall()[0]
      print("exists")
    except:
      cursor.execute("INSERT INTO Collection ('Name', 'UseCustomPlaybackOrder') VALUES ('"+EpisodeLabel+"', 0)")
      connection.commit()

    collection_id = cursor.execute("Select id from 'Collection' WHERE NAME = '"+EpisodeLabel+"'").fetchall()[0]
    return collection_id;

def create_collection_item(collection_id, MediaItemId):
    try:
        exists = cursor.execute("Select CollectionId from CollectionItem WHERE MediaItemId = "+str(MediaItemId)).fetchall()
        print("exists: " +str(exists[0]))
        print("collectitem exists")
    except Exception as e:
        exists = cursor.execute("INSERT INTO 'CollectionItem' ('CollectionId','MediaItemId','CustomIndex') VALUES ("+collection_id+","+MediaItemId+",NULL);")    
        connection.commit()
    return True;


def create_preset(EpisodeLabel, collection_id):
    try:
        exists = cursor.execute("Select Id from FillerPreset WHERE CollectionId = "+collection_id).fetchall()
        print("exists: " +str(exists[0]))
        print("preet exists")
    except:
        filler_insert = cursor.execute("INSERT INTO FillerPreset ('Name','FillerKind','FillerMode','Duration','Count','PadToNearestMinute','CollectionType','CollectionId','MediaItemId','MultiCollectionId','SmartCollectionId','AllowWatermarks') VALUES ('"+EpisodeLabel+"',5,0,NULL,NULL,NULL,0,"+collection_id+",NULL,NULL,NULL,1);")
        connection.commit()

    print("test")
    exists = cursor.execute("Select Id from FillerPreset WHERE CollectionId = "+collection_id).fetchall()
    print(exists[0][0])
    return exists[0][0]



def create_channel(preset_id, EpisodeLabel, ShowTitle):
    try:
        exists = cursor.execute("Select Id from Channel WHERE Name = "+EpisodeLabel).fetchall()
        print("exists: " +str(exists[0]))
    except:
        random_uuid = str(uuid.uuid4())
        channel_seq_id = cursor.execute("select seq from sqlite_sequence WHERE name = 'Channel'").fetchall()[0]
        next_channel = str(channel_seq_id[0]+1)
        channel_insert = cursor.execute("INSERT INTO Channel ('FFmpegProfileId','FallbackFillerId','Name','Number','PreferredAudioLanguageCode','StreamingMode','UniqueId','WatermarkId','Categories','Group','PreferredSubtitleLanguageCode','SubtitleMode','MusicVideoCreditsMode','PreferredAudioTitle','MusicVideoCreditsTemplate') VALUES  (1,'"+preset_id+"','"+EpisodeLabel+"','"+next_channel+"',NULL,1,'"+random_uuid+"',1,NULL,'"+ShowTitle+"','',0,0,NULL,NULL);")
    connection.commit()


def build_episode_title(ShowId):
    print("Show Title: "+get_show_title(ShowId))
    ShowTitle = get_show_title(ShowId).replace("'","")

    for SeasonId in get_show_seasons(ShowId):
        SeasonNumber = str(get_season_number(SeasonId[0])[0][0]).zfill(2)

        for Episode in get_season_episodes(SeasonId[0]):
            EpisodeNumber = str(get_episode_metadata(Episode[0])[0]).zfill(3)
            EpisodeTitle = get_episode_metadata(Episode[0])[1]
            
            EpisodeLabelRaw = ShowTitle+" - S"+SeasonNumber+"E"+EpisodeNumber+" - "+EpisodeTitle
            EpisodeLabel = EpisodeLabelRaw.replace("'","")
            print(EpisodeLabel)
            print(Episode[0]) 
            collection_id_raw = create_collection(EpisodeLabel)
            collection_id = str(collection_id_raw[0])
            print("Collction : " +collection_id)
            create_collection_item(collection_id, str(Episode[0]))
            preset_id = create_preset(EpisodeLabel, collection_id)
            print("preset : "+str(preset_id))
            create_channel(str(preset_id),EpisodeLabel,ShowTitle)



    #print(get_season_episodes(SeasonId))
    #print(get_episode_metadata(EpisodeId))

#build_episode_title(2192, 2193, 2194)

#print(get_show_seasons(2192))
#print(get_season_episodes(2193))

shows = cursor.execute("SELECT id FROM 'Show' ORDER BY id ASC").fetchall()
for data in shows:
    print(data)
    build_episode_title(str(data[0]))
