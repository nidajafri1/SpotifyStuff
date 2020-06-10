import spotipy
import spotipy.util as util
import pandas as pd
import os

class SpotifyData:
    """This class gets your liked tracks from Spotify (in nested dicts), each track's uri's and then 
        you can use each track's uri list to call on each of the track's features. You can then input the
        tracks into a Pandas DataFrame and export to csv with a function.
        
        Please ensure you have a Spotify Developer account with client ID, client secret and redirect URI into your app
        
        Attributes:
            username: str, your Spotify username
            scope: will always be 'user-library-read'. Read Spotipy documentation for anything else.
            client_id: your client ID acquired from your Spotify's developer account.
            client secret: your client secret acquired from your Spotify's developer account.
            redirect_uri: location that the authorization server will send the user to once the app has been successfully authorized
            
            """    
    
    def __init__(self, username, scope, client_id, client_secret, redirect_uri):
        self.username=username
        self.scope=scope
        self.client_id=client_id
        self.client_secret=client_secret
        self.redirect_uri=redirect_uri
        self.features_df=None
        

    def get_user_tracks(self):
        """Call on API to get use tracks. Output: dictionary of tracks with 17 elements of info on tracks
        """
        token = util.prompt_for_user_token(self.username, self.scope, client_id=self.client_id,
                                           client_secret=self.client_secret, redirect_uri=self.redirect_uri) #access token
        if token:
                sp = spotipy.Spotify(auth=token)
                results = sp.current_user_saved_tracks()
                tracks = results['items']
                tracks_dict = [d['track'] for d in tracks] #dictionary of tracks
                
                return tracks_dict
        else:
            print("can't get token or refresh it?")
            
            
    def get_uri_list(self, tracks_dict):
        """List of uri required to call on audio features stats of tracks
        
        tracks_dict: a nested dictionary containing track names you acquired from get_user_tracks()
        """
        uri_list = [d['uri'] for d in tracks_dict]
        
        return uri_list
    

    def get_features(self, uri_list, tracks_dict):
        """Acquires features of tracks and turns them into Pandas dataframe of JUST features of your liked tracks.
        
        uri_list: the list you acquired from get_uri_list. A Spotify URI (Uniform Resource Indicator) is a link that you can find in the Share menu of any track, album, or Artist Profile on Spotify.
        tracks_dict: a nested dictionary containing track names you acquired from get_user_tracks()
        
        """
        token = util.prompt_for_user_token(self.username, self.scope, client_id=self.client_id,
                                           client_secret=self.client_secret) #access token
        
        if token:
            sp = spotipy.Spotify(auth=token)
            audio_features = sp.audio_features(uri_list) #requesting features for all ur tracks
            features_df = pd.DataFrame.from_dict(audio_features) #putting the dict of tracks into a dataframe
            
            return features_df
        
        else:
            print("can't get token or refresh it?")
            

    def get_artists(self, features_df, tracks_dict):
        """Pandas dataframe of features and artist names of the song each row describes
        
        features_df: features dataframe acquired from get_features(). Output is the dataframe with associated artists names.
        tracks_dict: a nested dictionary containing track names you acquired from get_user_tracks()
            
        """
        artists_dict = [d['artists'] for d in tracks_dict]
        artists_name = [d[0]['name'] for d in artists_dict]
        features_df['Artists'] = artists_name
        
        return features_df


    def get_tracks(self,features_df, tracks_dict):
        """Pandas dataframe of features, artist names and track names. 
        
        features_df: features dataframe acquired from get_artists(). Output is the dataframe with associated track names. 
        tracks_dict: a nested dictionary containing track names you acquired from get_user_tracks()
        
        """
        track_names = [d['name'] for d in test_dict]
        features_df['Track'] = track_names
        
        return features_df
    

    def features_df_to_csv(self, features_df):
        """saves pandas dataframe into a csv file
        
        features_df: dataframe acquired from get_tracks(). Pandas DataFrame with track name, artists and features that returns a csv file and its location."""
        features = features_df.to_csv('features.csv', index=False, encoding='utf-8')
        
        print("your file is saved in {}".format(os.path.abspath(os.getcwd())))
    
    
    
    

            
