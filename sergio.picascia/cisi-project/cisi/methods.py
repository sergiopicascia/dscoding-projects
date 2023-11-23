"""
Methods for retrieving data in CINI format.
"""
import numpy as np

class BaseRetrieval:
    """
    The base method for retrieving documents given a certain query.
    """
    def __init__(self, random_state=None):
        self.random_state = random_state
        
    def score(self, y_true, y_pred):
        """
        Evaluate the performance of the model computing a score.

        Parameters
        ----------
        y_true: iter of iter of int
            The correct documents associated to each query.
        y_pred: iter of iter of int
            The predicted documents associated to each query.
            
        Returns
        -------
        score: float
            A score representing the ratio between corrected predicted
            over total predictions.
        """
        values = np.empty((len(y_true,)))
        for i, _ in enumerate(y_true):
            values[i] = len(np.intersect1d(y_pred[i], y_true[i])) / len(y_pred)
        score = np.mean(values)
        return score

class RandomRetrieval(BaseRetrieval):
    """
    A method for retrieving `n` random documents given a certain query.
    """
    def __init__(self, n=50, random_state=None):
        super().__init__(random_state)
        self.n = n
    
    def predict(self, documents, queries):
        """
        Predict a set of documents for each query randomly.

        Parameters
        ----------
        documents: iter of str
            An iterable of strings representing documents.
        queries: iter of str
            An iterable of strings representing queries.
            
        Returns
        -------
        predictions: list of lists of int
            For each query, a list of indexes representing documents 
            that have been associated to it.
        """
        predictions = []
        for _ in queries:
            query_docs = np.random.RandomState(
                seed=self.random_state
            ).choice(range(1, len(documents)+1), size=self.n)
            predictions.append(query_docs)
        return predictions
    
class TermFrequencyRetrieval(BaseRetrieval):
    """
    A method for retrieving documents given a certain query
    based on the term frequency.
    """
    def __init__(
        self,
        method='topn',
        n=50,
        threshold=None,
        random_state=None
        ):
        super().__init__(random_state)
        self.method = method
        self.n = n
        self.threshold = threshold
    
    def fit(self, documents):
        """
        Build a matrix of term frequencies
        with shape (len(documents), len(vocabulary)).

        Parameters
        ----------
        documents: iter of str
            An iterable of strings representing documents.
        """
        vocabulary = set(' '.join(documents).split(' '))
        term_frequency = np.zeros((len(documents), len(vocabulary)))
        vocabulary = dict(zip(vocabulary, range(len(vocabulary))))
        for i, txt in enumerate(documents):
            for word in txt.split(' '):
                term_frequency[i][vocabulary[word]] += 1
        for i, _ in enumerate(term_frequency):
            term_frequency[i] = term_frequency[i] / np.sum(term_frequency[i])
        self.vocabulary = vocabulary
        self.term_frequency = term_frequency
        
    def predict(self, queries):
        """
        Predict a set of documents for each query, based on the
        term frequency matrix.

        Parameters
        ----------
        queries: iter of str
            An iterable of strings representing queries.
        """
        similarity = np.empty((len(queries), self.term_frequency.shape[0]))
        for j, query in enumerate(queries):
            words = list(
                {
                    self.vocabulary[word] 
                    for word in query.split(' ')
                    if word in self.vocabulary
                }
            )
            for i, _ in enumerate(self.term_frequency):
                similarity[j][i] = self.term_frequency[i][words].sum()
        if self.method == 'topn':
            predictions = similarity.argsort(axis=1)[:, -self.n:]
        elif self.method == 'threshold':
            idx = np.argwhere(similarity > self.threshold)
            predictions = np.split(idx[:, 1], np.unique(idx[:, 0], return_index=True)[1][1:])
        predictions = [p + 1 for p in predictions]
        return predictions
    