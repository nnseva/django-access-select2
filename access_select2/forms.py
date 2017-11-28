from django_select2.forms import ModelSelect2Widget as _ModelSelect2Widget
from django_select2.forms import ModelSelect2MultipleWidget as _ModelSelect2MultipleWidget
from django_select2.forms import ModelSelect2TagWidget as _ModelSelect2TagWidget

from access.managers import AccessManager


class AccessSelect2WidgetMixin(object):
    def filter_queryset(self, term, queryset=None, request=None, *av, **kw):
        # the `request` parameter here appear from views.py
        queryset = AccessManager(queryset.model).apply_visible(queryset, request)
        return super(AccessSelect2WidgetMixin, self).filter_queryset(term, queryset=queryset, *av, **kw)


class ModelSelect2Widget(AccessSelect2WidgetMixin, _ModelSelect2Widget):
    pass


class ModelSelect2MultipleWidget(AccessSelect2WidgetMixin, _ModelSelect2MultipleWidget):
    pass


class ModelSelect2TagWidget(AccessSelect2WidgetMixin, _ModelSelect2TagWidget):
    pass
