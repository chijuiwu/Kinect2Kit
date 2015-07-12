"""
@author Alex Wallar
"""

import json


class Jsonable(object):
    """
    This class should be extended for data entities that you would like
    to make Jsonable by calling the to_json method. All variables that do
    not start with "__" will be included in the JSON string returned by
    the to to_json method
    """

    def to_json(self):
        jsonable_vars = dict()
        for key, elem in vars(self).iteritems():
            if not key.startswith("__"):
                jsonable_vars[key] = elem
        return json.dumps(jsonable_vars)
