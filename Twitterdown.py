from twitterscraper import query

# if __name__ == '__main__':
#     list_of_tweets = query_tweets("realDonaldTrump", 1)

# print the retrieved tweets to the screen:
# list_of_tweets = query_tweets("realDonaldTrump",1)
# for tweet in list_of_tweets:
#     print(tweet.text)


tweet = query.query_single_page('https://twitter.com/realDonaldTrump')
print(tweet)


# #Or save the retrieved tweets to file:
# file = open('output.txt','wb')
# for tweet in query_tweets("realDonaldTrump", 1):
#     # file.write(tweet.encode('utf-8'))
#     print(tweet)
#     file.write(tweet)
# file.close()
