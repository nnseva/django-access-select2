from django.http import JsonResponse

from django_select2.views import AutoResponseView as _AutoResponseView


class AutoResponseView(_AutoResponseView):
    def get(self, request, *args, **kwargs):
        self.widget = self.get_widget_or_404()
        self.term = kwargs.get('term', request.GET.get('term', ''))
        self.object_list = self.get_queryset(request)
        context = self.get_context_data()
        return JsonResponse({
            'results': [
                {
                    'text': self.widget.label_from_instance(obj),
                    'id': obj.pk,
                }
                for obj in context['object_list']
            ],
            'more': context['page_obj'].has_next()
        })

    def get_queryset(self, request):
        """Get QuerySet from cached widget."""
        kwargs = {
            model_field_name: self.request.GET.get(form_field_name)
            for form_field_name, model_field_name in self.widget.dependent_fields.items()
            if form_field_name in self.request.GET and self.request.GET.get(form_field_name, '') != ''
        }
        return self.widget.filter_queryset(self.term, queryset=self.queryset, request=request, **kwargs)
