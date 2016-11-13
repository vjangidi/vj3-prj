'''
Created on Nov 8, 2016

@author: Varun/Fathima
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
        if self.GenreId2Count.get(genreId) is None:
            self.GenreId2Count[genreId] = 1  
        else:
            self.GenreId2Count[genreId] = self.GenreId2Count[genreId] + 1
            
    def addRewardForGenreId(self,genreId, rewardRating):
        if self.GenreId2RewardPayoff.get(genreId) is None:
            self.GenreId2RewardPayoff[genreId] = [rewardRating]  
        else:
            self.GenreId2RewardPayoff[genreId].append(rewardRating)
        
    def getCountForGenreId(self, genreId):
        return 0 if self.GenreId2Count.get(genreId) is None else self.GenreId2Count[genreId]
    
    def getRewardForGenreId(self, genreId):
        if self.GenreId2RewardPayoff.get(genreId) is None:
            return [0]
        else:
            return self.GenreId2RewardPayoff.get(genreId)