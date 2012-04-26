from django.contrib import admin
from sd1_events.models import *

class EventOptionsAdmin(admin.TabularInline):
    model = RegistrationOptions
    fk_name = "event"
    extra = 0

class EventRegistrationAdmin(admin.TabularInline):
    model = EventRegistration
    fk_name = "event"
    extra = 0

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super(EventRegistrationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'option':
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(event__exact = request._obj_)  
            else:
                field.queryset = field.queryset.none()

        return field

class EventAdmin(admin.ModelAdmin):
    inlines = [ EventOptionsAdmin, EventRegistrationAdmin, ]
    list_display = ('__unicode__', 'total_regs')

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(EventAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(EventInfo, EventAdmin)

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('user', 'total')

admin.site.register(Receipt, ReceiptAdmin)