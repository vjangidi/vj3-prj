'''
Created on Nov 8, 2016

@author: Varun
'''

class Context(object):
    '''
    classdocs
    '''

    def __init__(self, context):
        '''
        Constructor
        '''
        self.context = context
        self.GenreId2Count = {}
        self.GenreId2RewardPayoff = {}
        
    def getContext(self):
        return self.context
        
    def addCountForGenreId(self, genreId):
        self.GenreId2Count[genreId] = 1 if self.GenreId2Count.get(genreId) is None else self.GenreId2Count[genreId] + 1
            
    def addRewardForGenreId(self,genreId):   
        self.GenreId2RewardPayoff[genreId] = 1 if self.GenreId2RewardPayoff.get(genreId) is None else self.GenreId2RewardPayoff[genreId] + 1
        
    def getCountForGenreId(self, genreId):
        return self.GenreId2Count[genreId]
    
    def getRewardForGenreId(self, genreId):
        return self.GenreId2RewardPayoff[genreId]