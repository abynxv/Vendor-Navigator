from django.contrib import admin
from django.contrib.auth.models import Group
from .models import  *

admin.site.register(VendorModel)
admin.site.register(PurchaseOrderModel)
admin.site.register(HistoricalPerformanceModel)
admin.site.unregister(Group)
admin.site.site_header = "Vendor Management System"
