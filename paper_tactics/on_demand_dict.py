class OnDemandDict:
    def __init__(self):
        self._cache = {}

    def get(self, key, init):
        if key not in self._cache:
            self._cache[key] = init()
        return self._cache[key]
