from text_clsf_lib.data_preparation.data_balancing import undersample_to_even, cut_off_longer_texts
from text_clsf_lib.preprocessing.cleaning.data_cleaners import PresetDataCleaner, TextCleaner, OutputCleaner
from text_clsf_lib.preprocessing.preprocessors import DataPreprocessor


def prepare_model_data(data_params: dict, vectorizer_params: dict) -> dict:
    """
    Prepares data from preset configuration (data_params, vectorizer_params) for model traning and testing.
    :param data_params: dict
    :param vectorizer_params: dict
    :return: dict. Contains cleaned texts (train/test) and also vectorized, ready for model input.
    """
    # retrieve data
    train_corpus, test_corpus = get_train_test_corpus(data_params['data_extractor'])

    corpus_word_limit = data_params['corpus_word_limit']
    X_name = data_params['X_name']
    if corpus_word_limit is not None:
        assert X_name is not None, 'If you want to reduce your corpus based on word count,' \
                                   ' you need to provide the key name for your input texts'
        train_corpus = cut_off_longer_texts(train_corpus, X_name, corpus_word_limit)
        test_corpus = cut_off_longer_texts(test_corpus, X_name, corpus_word_limit)

    y_name = data_params['y_name']
    if data_params['use_corpus_balancing']:
        assert y_name is not None, 'If you want to undersample your corpus based on different categories amounts,' \
                                    ' you need to privde the key name for your y labels.'
        train_corpus = undersample_to_even(train_corpus, y_name)
        test_corpus = undersample_to_even(test_corpus, y_name)

    # prepare components for data processing
    data_cleaner = prepare_data_cleaner(data_params['cleaning_params'])
    vectorizer_func = vectorizer_params.get('vectorizer_retriever_func')
    data_vectorizer = vectorizer_func(vectorizer_params)
    preprocessor = DataPreprocessor(data_cleaner, data_vectorizer)

    # prepare data using prepared components
    train_corpus = preprocessor.clean(train_corpus)
    test_corpus = preprocessor.clean(test_corpus)

    preprocessor.fit(train_corpus)
    preprocessor.save(vectorizer_params['save_dir'])

    train_corpus_vec = preprocessor.vectorize(train_corpus)
    test_corpus_vec = preprocessor.vectorize(test_corpus)

    return {
        'train_vectorized': train_corpus_vec,
        'test_vectorized': test_corpus_vec,
        'train_cleaned': train_corpus,
        'test_cleaned': test_corpus
    }


def get_train_test_corpus(data_extractor):
    """Retrieves data from a given data_extractor"""
    data_extractor = data_extractor()
    return data_extractor.get_train_test_corpus()


def prepare_data_cleaner(cleaning_params):
    """Prepares DataCleaner"""
    text_cleaner = TextCleaner(**cleaning_params['text'])
    output_cleaner = OutputCleaner(verifier_func=cleaning_params['output']['output_verification_func'])
    return PresetDataCleaner(text_cleaner, output_cleaner)
