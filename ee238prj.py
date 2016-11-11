'''
Created on Nov 6, 2016

@author: Varun/Fathima
'''
from user import User
from movie import Movie
from context import Context
import random
import math

Seperator = '::'
ITERCOUNT = 50000
RANDOM_REWARD_MOVIECOUNT = 50
A = 1.5
Beta = 0.25
Alpha = 0.5


dictOfMovieIdToGenreList = {}
dictOfUserIdToContext = {}
dictOfContext2Cluster = {}
dictOfContexts2Counts = {}
listOfGenres = []
dictOfArrivalToContext = {}

def getMovieListForAGenreId(genreId):
    return filter(lambda mov : genreId in mov.getGenreList(), dictOfMovieIdToGenreList.values())


def initGenreList():
    listOfGenresTemp = []
    for movie in dictOfMovieIdToGenreList.values():
        listOfGenresTemp.extend(movie.getGenreList())
        
    listOfGenres.extend(list(set(listOfGenresTemp)))

def getNormalizedRatingVector(user):
        return [user.getNormalizedRatingForGenre(genreId) for genreId in listOfGenres]

#Select 50 movies randomly for each user out of which 10 movies each are assigned to
#one of 5 ratings 
def randomRewardPayOffs():
    for userId in dictOfUserIdToContext.keys():
        user = dictOfUserIdToContext[userId]
        listOfAvlblMovies = dictOfMovieIdToGenreList.keys()
        listOfRatedMovies = user.getRatedMovieList()
        listOfAvlblRandomMovies = list(set(listOfAvlblMovies).difference(set(listOfRatedMovies)))
        randomMovies = random.sample(listOfAvlblRandomMovies, RANDOM_REWARD_MOVIECOUNT)
        ratingSeq = [1,2,3,4,5]
        for movieid in randomMovies:
            chosenRating = random.choice(ratingSeq)
            user.addReward(chosenRating, movieid)
            
    
def readMovie():
    f = open("C:\UCLA MS\EE238\ml-1m\ml-1m\movies.dat")
    for line in f:
        movieItems = line.split("\n")[0].split(Seperator)
        movieId = movieItems[0]
        title = movieItems[1]
        genreList =movieItems[2].split("|")
        dictOfMovieIdToGenreList[movieId] = Movie(movieId, title, genreList)
        

def buildContexts():
    f = open("C:\\UCLA MS\\EE238\\ml-1m\\ml-1m\\ratings.dat")
    for line in f:
        ratingItems = line.split("\n")[0].split(Seperator)
        userId = ratingItems[0]
        movieId = ratingItems[1]
        rating = ratingItems[2]
        if dictOfUserIdToContext.get(userId) is None:
            newuser = User(userId)
            dictOfUserIdToContext[userId] = newuser
            
        user = dictOfUserIdToContext.get(userId)
        for genreId in dictOfMovieIdToGenreList[movieId].genreList:
                user.addRating(genreId, rating, movieId)
       
def initContext2Counts(): 
    listOfRatingVectors = list(set([tuple(getNormalizedRatingVector(user)) for user in dictOfUserIdToContext.values()]))
    listOfContexts = [Context(context) for context in listOfRatingVectors]
    for context in listOfContexts:
        dictOfContexts2Counts[context.getContext()] = context
        
def calculateCosineDistance(pastContext,currentRatingContext):
    dotProduct = reduce(lambda x, y : x + y, [pastContext[i]*currentRatingContext[i] for i in xrange(len(pastContext))])
    scalarProduct = math.sqrt(reduce(lambda x, y : x + y, [pastContext[i]*pastContext[i] for i in xrange(len(pastContext))])) \
                    * math.sqrt(reduce(lambda x, y : x + y, [currentRatingContext[i]*currentRatingContext[i] for i in xrange(len(currentRatingContext))]))
    
    return dotProduct/scalarProduct
        

if __name__ == '__main__':
    readMovie()
    buildContexts()
    initGenreList()
    initContext2Counts()
    randomRewardPayOffs()
    for i in xrange(ITERCOUNT):
        #Randomly select an user from User list dictOfUserIdToContext.keys()
        #Observe the context. dictOfUserIdToContext[UserId]
        #Find past arrived contexts within t^alpha 
        #Find Closest contexts from them
        #Check the count of each cluster in these contexts and see if its less than A* t^Beta * lnt^Alpha
        #Explore or exploit
        #Update the counts of Cluster
        #Update the context of user with the rating if provided and dict mapping
        randomUserId = random.choice(dictOfUserIdToContext.keys())
        currentRatingContext = dictOfUserIdToContext[randomUserId]
        
        noOfClosestPastArrivalsToBeConsidered = math.floor(math.pow(i, Alpha))
        dictOfArrivalToContext[i] = currentRatingContext
        listOfDistancesWRTCurrentContext = [(pastContext,calculateCosineDistance(pastContext,currentRatingContext)) for pastContext in dictOfArrivalToContext.values()]
        list.reverse(listOfDistancesWRTCurrentContext)
        listOfDistance = [distance for context, distance in listOfDistancesWRTCurrentContext]
        listOfDistance.sort()
        listOfPastClosestContexts = []
        for minDist in listOfDistance:
            listOfContextsWithMinDist = filter(lambda x : x[1] == minDist , listOfDistancesWRTCurrentContext)
            if len(listOfContextsWithMinDist) > noOfClosestPastArrivalsToBeConsidered:
                listOfPastClosestContexts.extend(listOfContextsWithMinDist[:noOfClosestPastArrivalsToBeConsidered])
                break
            else:
                listOfPastClosestContexts.extend(listOfContextsWithMinDist)
            
        explorationParam = A * math.pow(i, Beta) * math.log(math.pow(i, Alpha))       
        pass
    
