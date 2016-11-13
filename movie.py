'''
Created on Nov 6, 2016

@author: Varun/Fathima
'''

class Movie(object):
    '''
    classdocs
    '''
    
    def __init__(self, movieId, title, genreList):
        '''
        Constructor
        '''
        self.movieId = movieId
        self.title = title
        self.genreList = genreList
        
    def getMovieId(self):
        return self.movieId
    
    def getTitle(self):
        return self.title
    
    def getGenreList(self):
        return self.genreList