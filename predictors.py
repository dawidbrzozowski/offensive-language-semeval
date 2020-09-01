from configs.presets.predictor_config import PredictorPreparer
from utils.files_io import load_json


class Predictor:
    def __init__(self, predictor_config):
        predictor_preparer = PredictorPreparer(predictor_config)
        self.preprocessor = predictor_preparer.get_preprocessor()
        self.model_runner = predictor_preparer.get_model_runner()

    def predict(self, text: list or str):
        preprocessed = self.preprocessor.preprocess([text]) if type(text) is str else self.preprocessor.preprocess(text)
        return self.model_runner.run(preprocessed)


if __name__ == '__main__':
    inp = ["donald trump is a", 'barack obama is a']
    predictor = Predictor(load_json('configs/data/predictor_config.json'))
    print(predictor.predict(inp))