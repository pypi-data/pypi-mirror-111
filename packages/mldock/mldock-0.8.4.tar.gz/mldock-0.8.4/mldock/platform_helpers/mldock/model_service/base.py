from abc import ABCMeta, abstractmethod


class ModelService(object):
    """
    ModelService wraps up all preprocessing, inference and postprocessing
    functions used by model service. It is defined in a flexible manner to
    be easily extended to support different frameworks.
    """
    __metaclass__ = ABCMeta

    model = None

    def __init__(self, model_path: str):
        """
            Internal initialize ModelService.
            
            args:
                model_path (str): path to model
            return:
                model object
        """
        self.model = self.load_model(model_path)

    @abstractmethod
    def load_model(self, model_path: str):
        """
            (Abstract) load model
        
            args:
                model_path(str): path to model
        """
        # pylint: disable=unnecessary-pass
        pass

    @abstractmethod
    def predict(self, input):
        """
            (Abstract) Predict method

            args:
                input : iterable of records model takes at prediction time.
            return:
                iterable of outputs from model
        """
        # pylint: disable=unnecessary-pass
        pass

    @abstractmethod
    def input_transform(input, **kwargs):
        """
            (Abstract) Output Transform

            args:
                input: raw iterable from request
            return:
                input transformed data
        """
        # pylint: disable=unnecessary-pass
        pass

    @abstractmethod
    def output_transform(predictions, **kwargs):
        """
            (Abstract) Output Transform

            args:
                predictions: predictions returned from model.predict
            return:
                output transformed predictions
        """
        # pylint: disable=unnecessary-pass
        pass
