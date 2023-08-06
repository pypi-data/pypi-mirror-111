# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['admincharts', 'admincharts.migrations']

package_data = \
{'': ['*'],
 'admincharts': ['static/admincharts/*', 'templates/admin/admincharts/*']}

setup_kwargs = {
    'name': 'django-admincharts',
    'version': '0.1.1',
    'description': 'Chart.js integration for Django admin models',
    'long_description': '# django-admincharts\n\nAdd [Chart.js](https://www.chartjs.org/docs/latest/) visualizations to your Django admin using a mixin class.\n\n## Example\n\n![django-admincharts example](https://user-images.githubusercontent.com/649496/124193149-f3c4c380-da8b-11eb-95d9-74e4f81c4c0a.png)\n\n```python\nfrom django.contrib import admin\n\nfrom .models import BillingAccount\nfrom admincharts.admin import AdminChartMixin\nfrom admincharts.utils import months_between_dates\n\n\n@admin.register(BillingAccount)\nclass BillingAccountAdmin(AdminChartMixin, admin.ModelAdmin):\n    def get_list_chart_data(self, queryset):\n        if not queryset:\n            return {}\n\n        # Cannot reorder the queryset at this point\n        earliest = min([x.ctime for x in queryset])\n\n        labels = []\n        totals = []\n        for b in months_between_dates(earliest, timezone.now()):\n            labels.append(b.strftime("%b %Y"))\n            totals.append(\n                len(\n                    [\n                        x\n                        for x in queryset\n                        if x.ctime.year == b.year and x.ctime.month == b.month\n                    ]\n                )\n            )\n\n        return {\n            "labels": labels,\n            "datasets": [\n                {"label": "New accounts", "data": totals, "backgroundColor": "#79aec8"},\n            ],\n        }\n```\n\n## Installation\n\n```console\n$ pip install django-admincharts\n```\n\nUse the `AdminChartMixin` with an `admin.ModelAdmin` class to add a chart to the changelist view.\n\nOptions can be set directly on the class:\n\n```python\nfrom django.contrib import admin\nfrom admincharts.admin import AdminChartMixin\n\n@admin.register(MyModel)\nclass MyModelAdmin(AdminChartMixin, admin.ModelAdmin):\n    list_chart_type = "bar"\n    list_chart_data = {}\n    list_chart_options = {"aspectRatio": 6}\n    list_chart_config = None  # Override the combined settings\n```\n\nOr by using the class methods which gives you access to the queryset being used for the current view:\n\n```python\nclass MyModelAdmin(AdminChartMixin, admin.ModelAdmin):\n    def get_list_chart_queryset(self, result_list):\n        ...\n\n    def get_list_chart_type(self, queryset):\n        ...\n\n    def get_list_chart_data(self, queryset):\n        ...\n\n    def get_list_chart_options(self, queryset):\n        ...\n\n    def get_list_chart_config(self, queryset):\n        ...\n```\n\nThe `type`, `data`, and `options` are passed directly to Chart.js to render the chart.\n[Look at the Chart.js docs to see what kinds of settings can be used.](https://www.chartjs.org/docs/latest/configuration/)\n',
    'author': 'Dave Gaeddert',
    'author_email': 'dave.gaeddert@dropseed.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dropseed/django-admincharts',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
