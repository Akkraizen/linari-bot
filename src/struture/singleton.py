class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance._created = False
        return cls._instance

    @property
    def created(self) -> bool:
        if not self._created:
            self._created = True
            return False
        return True
