from text_clsf_lib.predictors.presets import create_predictor_preset


class Predictor:
    """
    This class loads trained model and preprocessor.
    Its goal is to give model predictions on new unprocessed text.
    Predictor has the whole pipeline to perform a prediction.
    Takes in predictor preset. You can generate a predictor preset by using create_predictor_preset()
    """
    def __init__(self, preset: dict):
        preprocessing_params = preset['preprocessing_params']
        model_path = preset['model_path']
        self.preprocessor = preset['preprocessor_func'](preprocessing_params)
        self.model_runner = preset['model_func'](model_path)

    def predict(self, text: list or str):
        """
        :param text: single text or list of texts.
        :return: list of model predictions.
        """
        preprocessed = self.preprocessor.clean_vectorize(text)
        return self.model_runner.run(preprocessed).tolist()


if __name__ == '__main__':
    preset = create_predictor_preset(model_name='bpe_rnn',
                                     type_='bpe')
    pr = Predictor(preset)
    print(pr.predict('easy text with no special meaning fuck fucking trump'))