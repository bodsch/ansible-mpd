# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """
        Ansible file jinja2 tests
    """

    def filters(self):
        return {
            'type': self.var_type,
            'encode': self.encode,
            'find_in_dict': self.find_in_dict
        }

    def var_type(self, var):
        """
          Get the type of a variable
        """
        return type(var).__name__

    def encode(self, data):
        """

        """
        result = None

        data = data.replace(' ', '_')
        data = data.lower()

        spcial_char_map = {
            ord('ä'): 'ae', ord('ü'): 'ue', ord('ö'): 'oe', ord('ß'): 'ss'
        }

        data = data.translate(spcial_char_map)

        return data

    def find_in_dict(self, data, value, default):
        """
        """
        if data.get(value):
            result = data.get(value)
        else:
            result = default

        return result
