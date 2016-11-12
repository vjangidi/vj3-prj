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


dictOfMovieIdToMovie = {}
dictOfUserIdToUser = {}
dictOfContextIds2Contexts = {}
listOfGenres = []
dictOfArrivalToContext = {}

def getMovieListForAGenreId(genreId):
    return filter(lambda mov : genreId in mov.getGenreList(), dictOfMovieIdToMovie.values())


def initGenreList():
    listOfGenresTemp = []
    for movie in dictOfMovieIdToMovie.values():
        listOfGenresTemp.extend(movie.getGenreList())
        
    listOfGenres.extend(list(set(listOfGenresTemp)))

def getNormalizedRatingVector(user):
        return tuple([user.getNormalizedRatingForGenre(genreId) for genreId in listOfGenres])

#Select 50 movies randomly for each user out of which 10 movies each are assigned to
#one of 5 ratings 
def rewardPayOffs():
    f = open("C:\\UCLA MS\\EE238\\ml-1m\\ml-1m\\ratings.dat")
    for line in f:
        ratingItems = line.split("\n")[0].split(Seperator)
        userId = ratingItems[0]
        movieId = ratingItems[1]
        rating = ratingItems[2]
        user = dictOfUserIdToUser[userId]
        user.addReward(rating, movieId)
            
def buildMovies():
    f = open("C:\UCLA MS\EE238\ml-1m\ml-1m\movies.dat")
    for line in f:
        movieItems = line.split("\n")[0].split(Seperator)
        movieId = movieItems[0]
        title = movieItems[1]
        genreList =movieItems[2].split("|")
        dictOfMovieIdToMovie[movieId] = Movie(movieId, title, genreList)
        

def buildUsers():
    f = open("C:\\UCLA MS\\EE238\\ml-1m\\ml-1m\\users.dat")
    for line in f:
        userItems = line.split("\n")[0].split(Seperator)
        userId = userItems[0]
        dictOfUserIdToUser[userId] = User(userId)
                    
def calculateCosineDistance(pastContext,currentRatingContext):
    dotProduct = reduce(lambda x, y : x + y, [pastContext[i]*currentRatingContext[i] for i in xrange(len(pastContext))])
    scalarProduct = math.sqrt(reduce(lambda x, y : x + y, [pastContext[i]*pastContext[i] for i in xrange(len(pastContext))])) \
                    * math.sqrt(reduce(lambda x, y : x + y, [currentRatingContext[i]*currentRatingContext[i] for i in xrange(len(currentRatingContext))]))
    
    return dotProduct/scalarProduct

def getClosestContexts(currentRatingContext, noOfClosestPastArrivalsToBeConsidered):
        listOfPastClosestContexts = []
        
        listOfDistancesWRTCurrentContext = [(pastContext,calculateCosineDistance(pastContext,currentRatingContext)) for pastContext in dictOfArrivalToContext.values()]
        #Reversing the list to ensure first element reflects latest arrival
        list.reverse(listOfDistancesWRTCurrentContext)
        #Sort distances inAscending order
        listOfDistance = [distance for context, distance in listOfDistancesWRTCurrentContext]
        listOfDistance.sort()
        
        #Start with minDist(1st element in sorted distance list) and get all the contexts belonging to 
        #this list. Then check for next bigger dist
        for minDist in listOfDistance:
            listOfContextsWithMinDist = filter(lambda x : x[1] == minDist , listOfDistancesWRTCurrentContext)
            if len(listOfContextsWithMinDist) > noOfClosestPastArrivalsToBeConsidered:
                listOfPastClosestContexts.extend(listOfContextsWithMinDist[:noOfClosestPastArrivalsToBeConsidered])
                break
            else:
                listOfPastClosestContexts.extend(listOfContextsWithMinDist)
        return listOfPastClosestContexts
    
def recommendedGenreIdForExploration(listOfPastClosestContexts, explorationParam):
    genreIdToRecommend = None
    for genreId in listOfGenres:
            pastCountsForThisGenreId = 0
            for context in listOfPastClosestContexts:
                pastCountsForThisGenreId = pastCountsForThisGenreId + context.getCountForGenreId(genreId)
                if pastCountsForThisGenreId < explorationParam:
                    genreIdToRecommend = genreId
                    break
            if genreIdToRecommend is not None:
                break 
    return  genreIdToRecommend

def recommendedGenreIdForExploitation(listOfPastClosestContexts):
        dictOfGenreIdPayoff = {}
        for genreId in listOfGenres:
                pastRewardsForThisGenreId = []
                for context in listOfPastClosestContexts:
                    pastRewardsForThisGenreId.append(context.getRewardForGenreId(genreId))
                dictOfGenreIdPayoff[genreId] = reduce(lambda x, y : x + y, pastRewardsForThisGenreId)/len(pastRewardsForThisGenreId)            
            #Findout highest payoff genreId
        averagePayoffsList = dictOfGenreIdPayoff.values()
        averagePayoffsList.sort()
        maxPayoff = averagePayoffsList[-1]
        listOfMaxPayOffGenreIds = []
        for genreId,payoff in dictOfGenreIdPayoff.iteritems():
            if payoff == maxPayoff:
                listOfMaxPayOffGenreIds.append(genreId)
        return random.choice(listOfMaxPayOffGenreIds)            

if __name__ == '__main__':
    buildMovies()
    initGenreList()
    buildUsers()
    rewardPayOffs()
    for i in xrange(ITERCOUNT):
        #Randomly select an user from User list dictOfUserIdToUser.keys()
        #Observe the context. #Initially user has vector with 0,0... as context (No ratings avlbl) dictOfUserIdToUser[UserId]
        #Find past arrived contexts within t^alpha 
        #Find Closest contexts from them
        #Check the count of each cluster in these contexts and see if its less than A* t^Beta * lnt^Alpha
        #Explore or exploit
        #Update the counts of Cluster
        #Update the context of user with the rating if provided and dict mapping
        randomUserId = random.choice(dictOfUserIdToUser.keys())
        currentUser = dictOfUserIdToUser[randomUserId]
        currentRatingContextId = getNormalizedRatingVector(currentUser)
        currentRatingContext = Context(currentRatingContextId) if dictOfContextIds2Contexts.get(currentRatingContextId) is None else dictOfContextIds2Contexts[currentRatingContextId]
        
        #Find List of Closest contexts
        noOfClosestPastArrivalsToBeConsidered = math.floor(math.pow(i, Alpha))
        listOfPastClosestContexts = getClosestContexts(currentRatingContext, noOfClosestPastArrivalsToBeConsidered)
         
        explorationParam = A * math.pow(i, Beta) * math.log(math.pow(i, Alpha))
        #Check count of each cluster(Genre) in PastClosestContexts. If anyof this is < exploration param, play the cluster
        genreIdToRecommend = recommendedGenreIdForExploration(listOfPastClosestContexts, explorationParam)
        
        if genreIdToRecommend is None:
            #Exploit as there are no GenreIds with count less than Exploration param
            genreIdToRecommend = recommendedGenreIdForExploitation(listOfPastClosestContexts)
            
        #Randomly select a movie from this genreid
        genreIdMovieList = getMovieListForAGenreId(genreIdToRecommend)
        alreadyRecommendedMovieList = dictOfUserIdToUser[randomUserId].getRatedMovieList()
        avlblMovieList = list(set(genreIdMovieList).difference(set(alreadyRecommendedMovieList)))
        
        recommendedMovieId = random.choice(avlblMovieList)
        #Observe the Reward   
        observedReward = currentUser.getRewardForMovieid(recommendedMovieId)
        #Update the counts and payoffs
        currentUser.addRating(genreIdToRecommend, observedReward, recommendedMovieId)
        currentRatingContext.addCountForGenreId(genreIdToRecommend)
        currentRatingContext.addRewardForGenreId(observedReward)
        dictOfArrivalToContext[i] = currentRatingContext
    
