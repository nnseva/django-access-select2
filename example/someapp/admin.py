from django.contrib import admin
from access.admin import *

from access_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget, ModelSelect2TagWidget # -- modified

from someapp.models import *

class ChildAdmin(AccessTabularInline):
    model = SomeChild

# Register your models here.
class ObjectAdmin(AccessModelAdmin):
    inlines = [
        ChildAdmin,
    ]

    related_search_fields = {
        'editor_group': ('name__startswith',),
        'viewer_groups': ('name__startswith',),
    }

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Overrides the default widget for Foreignkey fields if they are
        specified in the select_search_fields class attribute.
        """
        kw = {}
        kw.update(kwargs)
        if isinstance(db_field, models.ForeignKey) and hasattr(self, 'related_search_fields') \
                and db_field.name in self.related_search_fields:
            kw['widget'] = ModelSelect2Widget(model=db_field.target_field.model,search_fields=self.related_search_fields[db_field.name])
        elif isinstance(db_field, models.ManyToManyField) and hasattr(self, 'related_search_fields') \
                and db_field.name in self.related_search_fields:
            kw['widget'] = ModelSelect2MultipleWidget(model=db_field.target_field.model,search_fields=self.related_search_fields[db_field.name])
        return super(ObjectAdmin, self).formfield_for_dbfield(db_field, **kw)

    class Media:
        js = ['//code.jquery.com/jquery-2.2.4.js']

# Register your models here.
admin.site.register(SomeObject,ObjectAdmin)
