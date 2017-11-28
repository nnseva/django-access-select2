[![Build Status](https://travis-ci.org/nnseva/django-access-select2.svg?branch=master)](https://travis-ci.org/nnseva/django-access-select2)

# Django-Access-Select2

The Django-Access-Select2 package provides a default filtering for the [Django-Select2](http://django-select2.readthedocs.io/en/latest/) package to use access rules defined by the [Django-Access](https://github.com/nnseva/django-access) package.

## Installation

*Stable version* from the PyPi package repository
```bash
pip install django-access-select2
```

*Last development version* from the GitHub source version control system
```bash
pip install git+git://github.com/nnseva/django-access-select2.git
```

## Configuration

Include the `django_select2`, `access`, and `access_select2` applications into the `INSTALLED_APPS` list, like:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    'django_select2',
    'access',
    'access_select2',
    ...
]
```

Remove if present, the existent reference to the Django-Select2 urlconf from your urlconfs and insert the modified one from the package:

```python
# url(r'^select2/', include('django_select2.urls')), -- removed
url(r'^select2/', include('access_select2.urls')), # -- modified
```


## Using

### Define access rules

Define access rules as it is described in the [Django-Access](https://github.com/nnseva/django-access) package documentation.

Note that the Django-Access-Select2 package uses only `apply_visible` AccessManager method to filter, what the user can see  in the dropdown list of objects.

### Use the modified widget

Remove if preset, the existent reference to the widget, and use the modified one

```python
# from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget -- removed
from access_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget # -- modified
```

### Modified view

The `AutoResponseView` class is slightly modified by the package: the `get_queryset` method now takes the positional `request` parameter.

If you are using `AutoResponseView` class directly in your code, yu should replace reference to it to the modified one and modify the
`get_queryset` method prototype:

```python
# from django_select2.views import AutoResponseView -- removed
from access_select2.views import AutoResponseView # -- modified

class MyAutoResponseView(AutoResponseView):
    ...
    # def get_queryset(self):          -- removed
    def get_queryset(self, request): # -- modified
    ...
```

## Example

Having in mind the [example](https://github.com/nnseva/django-access#examples) defined for the [Django-Access](https://github.com/nnseva/django-access), let
we use the the package as the following:

```python
```
