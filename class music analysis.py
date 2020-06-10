import numpy as np
import pandas as pd
import seaborn as sns
import os 
from sklearn.cluster import KMeans
import math

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler() #initliase

scaler.fit(numeric_chartmusic)

#take logs for varying orders of magnitudes
import pandas as pd
features_df = pd.read_csv('Features_DataFrame.csv', header=0, encoding='utf-8')        
float_only = features_df.select_dtypes(include=['float64'])
scaler.fit(float_only)
unstacked = (float_only).unstack().to_frame()
averages = sns.barplot(y=unstacked.index.get_level_values(0),x=unstacked[0])

float_only = np.log(self.features_df.select_dtypes(include=['float64'])).dropna(axis=1).replace(np.inf, 0).replace(-np.inf, 0)

def magnitude(x):
    return int(math.log10(x))

x=features_df['speechiness'].mean()
magnitude(x)

sns.pairplot(float_only)
sns.pairplot(np.log(float_only))

#plot the mean and the standard deviation of each float column
#plot the pairplot, KDE ofc 
#CLUSTERING!!

#to ask henry: 1) to specify object types 2) to raise errors on types
#               2) to roll back axis to np.exp())
#               3) multiple inheritance - self.float only 
#               4) GET 100 TRACKS!! - priority uno! 
#               5) get data saved in place rather than return a print? 
#                6) index return minimum distance list! 

class SpotifyDataAnalysis:
    def __init__(self, features_df):
        self.features_df = pd.read_csv(features_df, header=0, encoding='utf-8')        
    
    #Gives you the average and error bars of each feature, after log transformations (for scaling)    
    def averages(self): #to ask henry
        float_only = self.features_df.select_dtypes(include=['float64'])
        unstacked = (np.log(float_only)).unstack().to_frame()
        averages = sns.barplot(y=unstacked.index.get_level_values(0),x=unstacked[0])
        
        return averages
        
    #Gives you the distribution and correlation between two features, KDE.
    #Pass through columns as string.
    def joint_distributions(self, col1, col2): 
        float_only = self.features_df.select_dtypes(include=['float64'])
        jointplot = sns.jointplot(x=col1, y=col2, data=float_only, kind='kde', color='k') #positiveness v energy in songs
        
        return jointplot
    
    #Gives you the KDE distribution of all columns and correlations between them.
    def pairwise_distributions(self):
        float_only = self.features_df.select_dtypes(include=['float64'])
        g=sns.PairGrid(float_only)
        g.map_diag(sns.kdeplot)
        pairwisekdeplot=g.map_offdiag(sns.kdeplot, n_levels=6)        

        return pairwisekdeplot
    
    #please pass through the number of clusters 
    def kmeansclusters(self, numberofclusters):
        float_only = np.log(self.features_df.select_dtypes(include=['float64'])).dropna(axis=1).replace(np.inf, 0).replace(-np.inf, 0)
        Kmean = KMeans(n_clusters=numberofclusters)
        Kmean.fit(float_only)
        label = Kmean.labels_
        float_only.loc[:,'label']=label
        float_only.set_index(features['Artists'], inplace=True)
        cluster_pairplot = sns.pairplot(float_only, hue='label')
        
        return cluster_pairplot
    
    def saveplots(self, plot, nameofplotdotpng):
        plot_ = plot.get_figure()
        plot_.savefig(nameofplotpng, dpi=400)

        return os.path.abspath(os.getcwd())

#average of all the numerical stuff
#variability 
#distributions of your stuff
#clustering