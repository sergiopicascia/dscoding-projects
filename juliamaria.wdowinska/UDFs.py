import contractions
from nltk import word_tokenize
from nltk.corpus import stopwords

# Function: expand contractions (e.g., "it's" -> "it is")
def expand_contractions(x):
    return contractions.fix(x.lower(), slang = True)

# Function: extract words from text
def extract_words(x):
    return [w for w in word_tokenize(x) if w.isalpha()]

# Function: remove 'stopwords' (e.g., "the" is deleted)
def remove_stopwords(x):
    return [w for w in x if w not in stopwords.words('english')]