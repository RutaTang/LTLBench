from copy import deepcopy


class ReferenceValue[Type]:
    def __init__(self, value: Type):
        self.value = value

    def update(self, value):
        self.value = value

    def get(self):
        return deepcopy(self.value)
