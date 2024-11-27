from jinja2.ext import Extension

def issubset(value, a_longer_list):
    return set(value).issubset(set(a_longer_list))

class SubsetExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["issubset"] = issubset
