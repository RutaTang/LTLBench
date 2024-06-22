from copy import deepcopy


class ReferenceValue[Type]:
    """
    ReferenceValue is a class that allows to store a reference to a value, especially for built-in primitive types.
    """

    def __init__(self, value: Type):
        self.value = value

    def update(self, value):
        self.value = value

    def get(self):
        return deepcopy(self.value)
