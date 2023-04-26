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
            'encode': self.encode,
            'find_in_dict': self.find_in_dict
        }

    def encode(self, data):
        """
        """
        data = data.replace(' ', '_')
        data = data.lower()

        special_char_map = {
            ord('ä'): 'ae', ord('ü'): 'ue', ord('ö'): 'oe', ord('ß'): 'ss'
        }

        data = data.translate(special_char_map)

        return data

    def find_in_dict(self, data, value, default):
        """
        """
        if data.get(value):
            result = data.get(value)
        else:
            result = default

        return result
