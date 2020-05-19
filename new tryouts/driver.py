from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary
from gensim.test.utils import datapath
from lda import LdaModel
from pathlib import Path
import os



#PASUL 0 DATA CLEANING
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# create English stop words list
en_stop = get_stop_words('en')
tokenizer = RegexpTokenizer(r'\w+')



doc_set = []
for filename in os.listdir('./'):
    if filename.endswith(".txt"):
        path_in_str = os.path.join('./', filename)
        print(path_in_str)
        with open(path_in_str,"r") as f:
            contents = f.read()
            doc_set.append(contents)
            print([contents])

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:

    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)
    print('TOKENS')
    print(tokens)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]
    print('REMOVE STOP WORDS')
    print(stopped_tokens)

    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    print('STEAMED')
    print(stemmed_tokens)

    # add tokens to list
    texts.append(stemmed_tokens)



#  PASUL I
# # Create a corpus from a list of texts
common_dictionary = Dictionary(texts)
print(common_texts)
common_corpus = [common_dictionary.doc2bow(text) for text in common_texts]
# # Train the model on the corpus.
model = LdaModel(common_corpus, num_topics=10)
print(model)

# # Save model to disk.
temp_file = datapath("model")
model.save(temp_file)
#  SFARSIT PASUL I

# PASUL 2
# Load a potentially pretrained model from disk.
# model = LdaModel.load(temp_file)


# Create a new corpus, made of previously unseen documents.
# WHILE
# Vine text din FE
# Aplicam functii de formatare pe text ca sa fie ca mai jos
other_texts = [
        ['computer', 'time', 'graph'],
        ['survey', 'response', 'eps'],
        ['human', 'system', 'computer']
    ]
other_corpus = [common_dictionary.doc2bow(text) for text in other_texts]

unseen_doc = other_corpus[0]
vector = model[unseen_doc]  # get topic probability distribution for a document
print(vector)
# Trimitem vector catre FE
# END WHILE
# SFARSTI PASUL 2