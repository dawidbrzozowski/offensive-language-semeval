from typing import List

from preprocessing.cleaning.data_cleaners import DataCleaner
from preprocessing.vectorization.data_vectorizers import DataVectorizer
from preprocessing.vectorization.text_vectorizers import TextVectorizer


class DataPreprocessor:
    """
    This class is meant to combine data cleaning and data vectorization.
    Together it should deliver the whole process of preprocessing the data.
    fit(...) should perform fitting for data cleaner and data vectorizer.
    preprocess(...) should clean the data first, and then vectorize.

    """
    def __init__(self, data_cleaner: DataCleaner, data_vectorizer: DataVectorizer):
        self.data_cleaner = data_cleaner
        self.data_vectorizer = data_vectorizer

    def fit(self, data: List[dict]):
        self.data_cleaner.fit(data)
        texts = [record['text'] for record in data]
        outputs = [{'average': record['average'], 'std':record['std']} for record in data]
        self.data_vectorizer.fit(texts, outputs)

    def preprocess(self, data: List[dict]):
        self.data_cleaner.clean(data)
        texts = [record['text'] for record in data]
        outputs = [{'average': record['average'], 'std': record['std']} for record in data]
        processed_texts, processed_output = self.data_vectorizer.vectorize(texts, outputs)
        return processed_texts, processed_output

    def get_vectorization_metainf(self) -> dict:
        return self.data_vectorizer.get_vectorization_metainf()


class RealDataPreprocessor:
    # TODO this parameter could also be changed for some kind of preset
    def __init__(self, ready_text_cleaner: DataCleaner, ready_text_vectorizer: TextVectorizer):
        # TODO for now it is DataCleaner. When Text and Output cleaner is implemented, change that to Text!
        self.text_cleaner = ready_text_cleaner
        self.text_vectorizer = ready_text_vectorizer

    def preprocess(self, data: str or List[str]):
        if type(data) is str:
            data = [data]
        data = self.text_cleaner.clean(data)
        return self.text_vectorizer.vectorize(data)