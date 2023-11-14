import contractions
from nltk import word_tokenize
from nltk.corpus import stopwords

# Function: expand contractions (e.g., "it's" -> "it is")
def expand_contractions(text):
    return contractions.fix(text.lower(), slang = True)

# Function: extract words from text
def extract_words(text):
    return [w for w in word_tokenize(text) if w.isalpha()]

# Function: remove 'stopwords' (e.g., "the" is deleted)
def remove_stopwords(list_of_words):
    return [w for w in list_of_words if w not in stopwords.words('english')]

# Function: preprocess text
def preprocess(text):
    return " ".join(remove_stopwords(extract_words(expand_contractions(text))))