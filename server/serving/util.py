class ConstantDict(dict):
    def __setitem__(self, key, value):
        if self.get(key) is not None:
            raise ValueError('key {} has already existed in the dict'.format(key))
        super().__setitem__(key, value)
