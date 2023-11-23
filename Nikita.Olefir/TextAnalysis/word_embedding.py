"""
This module includes create_word_embeddings() function that creates column with embeddings of the words of a specified column.
"""
from nltk.tokenize import word_tokenize
from gensim.models import Word2Vec

def create_word_embeddings(dataframe, column_name: str, embedding_column: str = 'comment_embeddings', vector_size: int = 100, window: int = 5, min_count: int = 1, workers: int = 4):
    """
    Creates word embeddings for text data in a DataFrame.

    Arguments:
        dataframe (pd.DataFrame): The input pandas DataFrame containing lemmatized text data.
        column_name (str): The name of the column containing words.
        embedding_column (str): The name of the column to store the comment embeddings (default is 'comment_embeddings').
        vector_size (int): Dimensionality of the word vectors (default is 100).
        window (int): Maximum distance between the current and predicted word within a sentence (default is 5).
        min_count (int): Ignores all words with a total frequency lower than this (default is 1).
        workers (int): Number of CPU cores to use for training the Word2Vec model (default is 4).

    Returns:
        pd.DataFrame: DataFrame with an additional column for comment embeddings.

    Examples:
        create_comment_embeddings(df, 'column_name', 'comment_embeddings', vector_size=100, window=5, min_count=1, workers=4)
    """
    dataframe['tokenized_comments'] = dataframe[column_name].apply(lambda x: word_tokenize(str(x)))
    model = Word2Vec(sentences=dataframe['tokenized_comments'], vector_size=vector_size, window=window, min_count=min_count, workers=workers)

    def get_comment_embedding(comment, model):
        word_vectors = [model.wv[word] for word in comment if word in model.wv]
        if word_vectors:
            comment_vector = sum(word_vectors) / len(word_vectors)
            return comment_vector
        else:
            return None

    dataframe[embedding_column] = dataframe['tokenized_comments'].apply(lambda x: get_comment_embedding(x, model))

    return dataframe