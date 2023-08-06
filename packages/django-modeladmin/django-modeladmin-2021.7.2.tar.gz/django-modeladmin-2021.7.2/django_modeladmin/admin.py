from django.contrib import admin
from django.contrib.admin import register, site
from django.db import models
from django.template.defaultfilters import linebreaksbr
from django.utils.timesince import timesince

from .utils import get_boolean_fields, get_string_fields

class ModelAdmin(admin.ModelAdmin):
    list_display_exclude = []
    list_display_extra = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_display = self.get_formatted_list_display(self.list_display)

    def get_elapsed(self,name1,name2,short_description=None):
        def f(obj):
            dt1, dt2 = getattr(obj,name1), getattr(obj,name2)
            if dt1 and dt2:
                s = str(dt2 - dt1)
                return '.'.join(filter(None,[
                    s.split('.')[0].replace('0:00:00','0').replace('0:00:0',''),
                    s.split('.')[1][0:2]
                ]))
        f.short_description = short_description if short_description is not None else name
        return f

    def get_linebreaksbr(self,name,short_description=None):
        def f(obj):
            if getattr(obj, name):
                return mark_safe(linebreaksbr(getattr(obj, name)))
        f.allow_tags = True
        f.short_description = short_description if short_description is not None else self.model._meta.get_field(name).verbose_name
        f.admin_order_field = name
        return f

    def get_strftime(self,name,format,short_description=None):
        f = lambda obj: getattr(obj, name).strftime(format) if getattr(obj, name) else None
        f.short_description = short_description if short_description is not None else self.model._meta.get_field(name).verbose_name
        f.admin_order_field = name
        return f

    def get_timesince(self,name,short_description=None):
        def f(obj):
            if getattr(obj, name):
                return timesince(getattr(obj, name)).split(',')[0]+' ago'
        f.short_description = short_description if short_description is not None else self.model._meta.get_field(name).verbose_name
        f.admin_order_field = name
        return f

    def get_value(self,key,*args,**kwargs):
        if hasattr(self,key):
            return getattr(self,key)
        func_name = 'get_' + key
        model_func_name = 'get_admin_' + key
        model_key = 'admin_' + key
        if hasattr(self.model,model_func_name):
            return getattr(self.model,model_func_name)(*args,**kwargs)
        if hasattr(self.model,model_key):
            return getattr(self.model,model_key)
        return getattr(super(),func_name)(*args,**kwargs)

    #def get_autocomplete_fields(self,request):
    #    return self.get_value('autocomplete_fields',request)

   # def get_changelist(self,request, **kwargs):
   #     return super().get_changelist(request, **kwargs)

    #def get_changelist_form(self,request, **kwargs):
     #   return super().get_changelist_form(request, **kwargs)

    #def get_exclude(self,request, obj=None):
    #    return self.get_value('exclude',request)

    #def get_fields(self,request, obj=None):
    #    return self.get_value('fields',request,obj)

    #def get_fieldsets(self,request, obj=None):
    #    return self.get_value('fieldsets',request,obj)

    def get_list_display(self,request):
        list_display = []
        if list(self.list_display)!=['__str__']:
            list_display = self.list_display
        elif hasattr(self.model,'get_admin_list_display'):
            list_display = self.model,get_admin_list_display(request)
        elif hasattr(self.model,'admin_list_display'):
            list_display = self.model.admin_list_display
        else:
            list_display = []
            for f in self.model._meta.get_fields():
                if f.name not in self.get_list_display_exclude(request):
                    list_display.append(f.name)
        return self.get_formatted_list_display(list_display)

    def get_formatted_list_display(self,list_display):
        formatted_list_display = []
        for f in list_display:
            if isinstance(f, str):
                formatted_list_display.append(f)
            else:
                new_field_name = f[1]+'_'+f[0]
                func = getattr(self,'get_'+f[0])(*f[1:])
                setattr(self, new_field_name, func)
                formatted_list_display.append(new_field_name)
        return formatted_list_display

    def get_list_display_exclude(self,request):
        return self.list_display_exclude

    def get_list_filter(self,request):
        if hasattr(self,'list_filter') and self.list_filter:
            return self.list_filter
        if hasattr(self.model,'get_admin_list_filter'):
            return self.model,get_admin_list_filter(request)
        if hasattr(self.model,'admin_list_filter'):
            return self.model.admin_list_filter
        return [f.name for f in get_boolean_fields(self.model)]

    def get_ordering(self,request):
        return self.get_value('ordering',request)

    def get_readonly_fields(self,request, obj=None):
        return self.get_value('readonly_fields',request,obj)

    def get_prepopulated_fields(self,request, obj=None):
        return self.get_value('prepopulated_fields',request,obj)

    def get_search_fields(self,request):
        if hasattr(self,'search_fields') and self.search_fields:
            return self.search_fields
        if hasattr(self.model,'get_admin_search_fields'):
            return self.model,get_admin_search_fields(request)
        if hasattr(self.model,'admin_search_fields'):
            return self.model.admin_search_fields
        return [f.name for f in get_string_fields(self.model)]
