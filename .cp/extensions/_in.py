from jinja2.ext import Extension

def _in(value, a_longer_list):
    return_value = False
    for v in value.split(','):
        if v in a_longer_list:
            return_value = True
    return return_value

class InExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["_in"] = _in
