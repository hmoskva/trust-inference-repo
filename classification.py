import nltk
import random
import pickle
import os

from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from nltk.classify import ClassifierI
from nltk.tokenize import word_tokenize
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from statistics import mode


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes/len(votes)
        return conf


short_pos = open("positive.txt", "r").read()
short_neg = open("negative.txt", "r").read()

documents = []
all_words = []
allowed_word_typs = ["J", "V", "R"]
for r in short_pos.split('\n'):
    documents.append((r, 'pos'))
    words = word_tokenize(r)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_typs:
            all_words.append(w[0].lower())
for r in short_neg.split('\n'):
    documents.append((r, 'neg'))
    words = word_tokenize(r)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_typs:
            all_words.append(w[0].lower())


all_words = nltk.FreqDist(all_words)
# print(all_words.most_common(15))

ts = all_words.most_common(1000)
word_features = [w[0] for w in ts]
# word_features = list(all_words.keys())[:3000]


def find_features(doc):
    words = word_tokenize(doc)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


# print((find_features(movie_reviews.words('neg/cv442_15499.txt'))))

featuresets = [(find_features(rev), cat) for (rev, cat) in documents]
random.shuffle(featuresets)
# print(len(featuresets))

training_set = featuresets[:1000]
testing_set = featuresets[1000:2000]

classifier = nltk.NaiveBayesClassifier.train(training_set)
#
# classifier_f = open("naivebayes.pickle", "rb")
# classifier = pickle.load(classifier_f)
# classifier_f.close()

# print("Original Naive bayes algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
classifier.show_most_informative_features(15)

# save_classifier = open("naivebayes.pickle", "wb")
# pickle.dump(classifier, save_classifier)
# save_classifier.close()


# MultinomialBN algorithm
mnb_classifier = SklearnClassifier(MultinomialNB())
mnb_classifier.train(training_set)
# print("Multinomial algo accuracy percent:", (nltk.classify.accuracy(mnb_classifier, testing_set)) * 100)


# Bernoulli algorithm
bn_classifier = SklearnClassifier(BernoulliNB())
bn_classifier.train(training_set)
# print("Bernoulli algo accuracy percent:", (nltk.classify.accuracy(bn_classifier, testing_set)) * 100)

# LogisticRegression
lr_classifier = SklearnClassifier(LogisticRegression())
lr_classifier.train(training_set)
# print("LogisticRegression algo accuracy percent:", (nltk.classify.accuracy(lr_classifier, testing_set)) * 100)

#SGDClassifier
sgd_classifier = SklearnClassifier(SGDClassifier())
sgd_classifier.train(training_set)
# print("SGDClassifier algo accuracy percent:", (nltk.classify.accuracy(sgd_classifier, testing_set)) * 100)

#SVC
linsvc_classifier = SklearnClassifier(LinearSVC())
linsvc_classifier.train(training_set)
# print("LinearSVC algo accuracy percent:", (nltk.classify.accuracy(linsvc_classifier, testing_set)) * 100)

#NuSVC
NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
# print("NuSVC algo accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set)) * 100)

vote_classifier = VoteClassifier(mnb_classifier, bn_classifier, lr_classifier, linsvc_classifier, NuSVC_classifier)


def sentiment(text):
    feats = find_features(text)
    return vote_classifier.classify(feats), vote_classifier.confidence(feats)

