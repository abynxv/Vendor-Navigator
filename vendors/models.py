from django.db import models
from datetime import date, timedelta


class VendorModel(models.Model):
    name = models.CharField(max_length=100)
    contact = models.TextField(max_length=50)
    address = models.TextField(max_length=150)
    vendor_code = models.CharField(max_length=100, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if not self.vendor_code:
            last_vendor = VendorModel.objects.all().order_by('id').last()
            if last_vendor:
                last_vendor_code = last_vendor.vendor_code
                if last_vendor_code:
                    last_vendor_number = int(last_vendor_code.split('-')[-1])
                    new_vendor_number = last_vendor_number + 1
                else:
                    new_vendor_number = 1
            else:
                new_vendor_number = 1
            self.vendor_code = f"VENDOR-{new_vendor_number:04d}"
        super().save(*args, **kwargs)   
     
    def __str__(self):
        return self.name

class PurchaseOrderModel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    order_date = models.DateField(default=date.today)
    delivery_date = models.DateField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateField(auto_now_add=True)
    acknowledgment_date = models.DateField(null=True, blank=True)

 
    def save(self, *args, **kwargs):
        self.order_date = date.today()                            #Order Date
        self.delivery_date = self.order_date + timedelta(days=5)  #Delivery Date
        self.quantity = len(self.items)                           #quantity

        if not self.po_number:                                    #po number creaton
            last_po = PurchaseOrderModel.objects.all().order_by('id').last()
            if last_po:
                last_po_number_code = last_po.po_number
                if last_po_number_code:
                    last_po_number = int(last_po_number_code.split('-')[-1])
                    new_po_number = last_po_number + 1
                else:
                    new_po_number = 1
            else:
                new_po_number = 1
            self.po_number = f"PURCHASE-{new_po_number:04d}"
        super().save(*args, **kwargs) 



    def __str__(self):
        return self.po_number
    
class HistoricalPerformanceModel(models.Model):
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"



