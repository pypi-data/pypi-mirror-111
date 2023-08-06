# django-admincharts

Add [Chart.js](https://www.chartjs.org/docs/latest/) visualizations to your Django admin using a mixin class.

## Example

![django-admincharts example](https://user-images.githubusercontent.com/649496/124193149-f3c4c380-da8b-11eb-95d9-74e4f81c4c0a.png)

```python
from django.contrib import admin

from .models import BillingAccount
from admincharts.admin import AdminChartMixin
from admincharts.utils import months_between_dates


@admin.register(BillingAccount)
class BillingAccountAdmin(AdminChartMixin, admin.ModelAdmin):
    def get_list_chart_data(self, queryset):
        if not queryset:
            return {}

        # Cannot reorder the queryset at this point
        earliest = min([x.ctime for x in queryset])

        labels = []
        totals = []
        for b in months_between_dates(earliest, timezone.now()):
            labels.append(b.strftime("%b %Y"))
            totals.append(
                len(
                    [
                        x
                        for x in queryset
                        if x.ctime.year == b.year and x.ctime.month == b.month
                    ]
                )
            )

        return {
            "labels": labels,
            "datasets": [
                {"label": "New accounts", "data": totals, "backgroundColor": "#79aec8"},
            ],
        }
```

## Installation

```console
$ pip install django-admincharts
```

Use the `AdminChartMixin` with an `admin.ModelAdmin` class to add a chart to the changelist view.

Options can be set directly on the class:

```python
from django.contrib import admin
from admincharts.admin import AdminChartMixin

@admin.register(MyModel)
class MyModelAdmin(AdminChartMixin, admin.ModelAdmin):
    list_chart_type = "bar"
    list_chart_data = {}
    list_chart_options = {"aspectRatio": 6}
    list_chart_config = None  # Override the combined settings
```

Or by using the class methods which gives you access to the queryset being used for the current view:

```python
class MyModelAdmin(AdminChartMixin, admin.ModelAdmin):
    def get_list_chart_queryset(self, result_list):
        ...

    def get_list_chart_type(self, queryset):
        ...

    def get_list_chart_data(self, queryset):
        ...

    def get_list_chart_options(self, queryset):
        ...

    def get_list_chart_config(self, queryset):
        ...
```

The `type`, `data`, and `options` are passed directly to Chart.js to render the chart.
[Look at the Chart.js docs to see what kinds of settings can be used.](https://www.chartjs.org/docs/latest/configuration/)
