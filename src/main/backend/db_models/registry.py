
class Registry_new:
    _registry_new = {}

    @classmethod
    def register(cls, key, value):
        cls._registry_new[key] = value

    @classmethod
    def get(cls, key):
        return cls._registry_new.get(key)

    @classmethod
    def unregister(cls, key):
        if key in cls._registry:
            del cls._registry_new[key]
    
    @classmethod
    def get_all(cls):
        print(cls._registry_new)