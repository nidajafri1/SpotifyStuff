# -*- coding: utf-8 -*-
"""
Created on Sun May 17 23:37:38 2020

@author: n.jafri
"""
import pandas as pd
import numpy as np
from scipy.spatial import distance
from scipy.spatial.distance import cdist

class IdealSpotifySongs:
    """Input your Spotify audio features Pandas DataFrame of your liked tracks, and call on its columns you want analysed to return a list of tracks closest to 
    your ideal input of danceability, energy, speechiness, valence, tempo.
    
    Please ensure your object you pass is a Pandas DataFrame.
    
    Attributes:
        features_df = DataFrame, Pandas DataFrame of your Spotify liked tracks with its associated danceability, energy, speechiness, valence, tempo.
    
    """
    def __init__(self, features_df):
        self.features_df = features_df 
        
    def features_series(self, column_danceability, column_energy, column_speechiness, column_valence, column_tempo, column_track, column_artist):
        """Converts your Pandas DataFrame into Series with each row being a 1*5 matrix with the index being 'track - artist'.
        
        column_danceability: str, column in your DataFrame with danceability Spotify feature. 
        column_energy: str, column in your DataFrame with energy Spotify feature.
        column_speechiness: str, column in your DataFrame with speechiness Spotify feature.
        column_valence: str, column in your DataFrame with valence Spotify feature.
        column_tempo: str, column in your DataFrame with tempo Spotify feature.
        column_track: str, column in your DataFrame with track name.
        column_artist: str, column in your DataFrame with artist name.
        
        """
        my_music_df = self.features_df.filter([column_danceability, column_energy, column_speechiness, column_valence, column_tempo])
        my_music_series = pd.Series(my_music_df.values.tolist(), index=self.features_df[column_track].str.cat(self.features_df[column_track], sep=' - ')) 
        
        return my_music_series
        
    def min_dist_list(self, danceability, energy, speechiness, valence, tempo, my_music_series):
        """Returns a list of minimum distance of each track in your music series with respect to your ideal audio features inputs.
        
        danceability: float64, Danceability describes how suitable a track is for dancing based on a combination of musical elements including 
        tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable. 
        
        energy: float64, Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. 
                For example, death metal has high energy, while a Bach prelude scores low on the scale. 
                Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
        
        speechiness: float64, Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. 
                    Values above 0.66 describe tracks that are probably made entirely of spoken words. 
                    Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. 
                    Values below 0.33 most likely represent music and other non-speech-like tracks.
        
        valence: float64, A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. 
                Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while 
                tracks with low valence sound more negative (e.g. sad, depressed, angry).
        
        tempo: float64, The overall estimated tempo of a track in beats per minute (BPM). 
            In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration. 
            
        my_music_series: Pandas Series, Pandas Series with index 'track - artist', each one-dimensional array of vectors of features of each track.
        
        
        """
        ideal_choice = [danceability, energy, speechiness, valence, tempo]
        min_dist_list = []
        
        for index1,array1 in my_music_series.iteritems():
            temp_series = pd.Series(data=distance.euclidean(ideal_choice,array1))
            for index2,array2 in temp_series.iteritems():
                min_dist_list.append(array2)
                
        return min_dist_list
                
    def min_dist_df(self, min_dist_list, column_track, column_artist):
        """Returns a DataFrame with minimum distance between your ideal audio features input and in order the closest tracks to them within your liked tracks Spotify.
        
        min_dist_list: list, list acquired of minimum distance from IdealSpotifySongs.min_dist_list()
        column_track: str, column in your DataFrame with track name.
        column_artist: str, column in your DataFrame with artist name.
        
        """
        min_dist_df = pd.DataFrame(data=min_dist_list, index=self.features_df[column_track].str.cat(self.features_df[column_artist], sep=' - '))
        min_dist_df.rename(columns={0: 'Minimum_dist_between_idealchoice_and_track'}, inplace=True)
        min_dist_df.sort_values(by=['Minimum_dist_between_idealchoice_and_track'], ascending=True, inplace=True)
        
        return min_dist_df
        

        