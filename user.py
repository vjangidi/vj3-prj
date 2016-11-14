'''
Created on Nov 6, 2016

@author: Varun/Fathima
'''

NormalizingConstant = 1/5.0

class User(object):   

    def __init__(self, userId):
        self.dictOfGenreToRatings = {}
        self.listOfMoviesRated = []
        self.rewardDict = {}
        self.userId = userId
        
    #Adds rating for given movieId to a list of ratings already present for genreId
    def addRating(self, genreId, rating, movieId):
        existingRatingsForThisGenre = self.dictOfGenreToRatings.get(genreId)
        if  existingRatingsForThisGenre:
            existingRatingsForThisGenre.append(rating)
        else:
            self.dictOfGenreToRatings[genreId] = [rating]
        self.listOfMoviesRated.append(movieId)
        
    def getRatingListForGenreId(self, genreId):
            return self.dictOfGenreToRatings.get(genreId)
        
    # Computes the mean of available ratings for the given genreId and normalizes it
    # by multiplying with 1/5 
    def getNormalizedRatingForGenre(self, genreId):
        ratingsForGenre = self.dictOfGenreToRatings.get(genreId)
        ratingMean = 0
        if ratingsForGenre is None:
            return ratingMean
        else:
            for rating in ratingsForGenre:
                ratingMean = ratingMean + int(rating)
            return NormalizingConstant * (ratingMean/len(ratingsForGenre))
    
    def getRatedMovieList(self):
        return self.listOfMoviesRated
    
    #Keeps track of movies which user has rated so that reward can be obtained
    def addReward(self, rating, movieId):
            self.rewardDict[movieId] = rating
            
    def getRewardForMovieid(self, movieId):
            return 0 if self.rewardDict.get(movieId) is None else self.rewardDict[movieId] 
