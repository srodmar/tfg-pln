import nltk
from nltk.corpus import twitter_samples

tweets = twitter_samples.strings('positive_tweets.json')
print nltk.pos_tag(nltk.word_tokenize(tweets[34]))
