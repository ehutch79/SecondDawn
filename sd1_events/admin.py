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

class EventAdmin(admin.ModelAdmin):
    inlines = [ EventOptionsAdmin, EventRegistrationAdmin, ]
    list_display = ('__unicode__', 'total_regs')

admin.site.register(EventInfo, EventAdmin)

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('user', 'total')

admin.site.register(Receipt, ReceiptAdmin)