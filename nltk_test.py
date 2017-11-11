__author__ = 'Habibd'
import nltk
import random
from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer
from nltk.corpus import stopwords, state_union, movie_reviews
from nltk.stem import PorterStemmer
from nltk import pos_tag

text = "Hello Mr. Smith, how are you doing today? The weather is great, " \
       "and Python is awesome. The sky is blue. You shouldn't eat cardboard"


def main():
    print(pos_tagging())


def filter_by_removing_stopwords(corpus):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(corpus)
    filtered_sent = [w for w in word_tokens if w not in stop_words]
    return filtered_sent


def filter_by_stemming(corpus):
    ps = PorterStemmer()


def pos_tagging():
    train_text = state_union.raw("2005-GWBush.txt")
    sample_text = state_union.raw("2006-GWBush.txt")
    custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
    tokenized = custom_sent_tokenizer.tokenize(sample_text)
    x = process_content(tokenized)
    return x


def process_content(tokenized):
    try:
        for i in tokenized[:5]:
            words = word_tokenize(i)
            tagged = pos_tag(words)
            return tagged

    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
# nltk.download()