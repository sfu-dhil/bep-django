import csv
from django_select2.forms import Select2TagWidget, Select2AdminMixin

class Select2TagArrayWidget(Select2AdminMixin, Select2TagWidget):
    def build_attrs(self, base_attrs, extra_attrs=None):
        default_attrs = {
            "data-allow-clear": False,
            "data-token-separators": ',',
            "data-width": '500px',
        }
        default_attrs.update(base_attrs)
        return super().build_attrs(default_attrs, extra_attrs=extra_attrs)

    def optgroups(self, name, value, attrs=None):
        values = value[0].split(',') if len(value) > 0 and value[0] else []
        selected = set(values)
        subgroup = [self.create_option(name, v, v, selected, i) for i, v in enumerate(values)]
        return [(None, subgroup, 0)]

class Select2TagWithCommaArrayWidget(Select2AdminMixin, Select2TagWidget):
    def build_attrs(self, base_attrs, extra_attrs=None):
        default_attrs = {
            "data-allow-clear": False,
            "data-token-separators": '|',
            "data-width": '500px',
        }
        default_attrs.update(base_attrs)
        return super().build_attrs(default_attrs, extra_attrs=extra_attrs)

    def optgroups(self, name, value, attrs=None):
        from pprint import pprint
        print('optgroups')
        pprint(value)
        values = []
        if len(value) > 0 and value[0]:
            pprint(value[0].splitlines())
            values = list(csv.reader(value[0].splitlines(), delimiter=','))[0]
            pprint(values)
        selected = set(values)
        subgroup = [self.create_option(name, v, v, selected, i) for i, v in enumerate(values)]
        return [(None, subgroup, 0)]