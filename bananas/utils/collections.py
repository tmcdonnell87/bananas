class ModelChoices(tuple):

    def __new__(cls, **kwargs):
        return tuple.__new__(cls, kwargs.values())

    def __init__(self, **kwargs):
        super(ModelChoices, self).__init__()
        self.__choices = kwargs

    def __getattr__(self, item):
        try:
            return self.__choices[item][0]
        except KeyError:
            raise AttributeError
