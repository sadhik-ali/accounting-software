from django.contrib import admin
from .models import Table_Acntchild,VoucherConfiguration,Table_Accountsmaster, Table_Voucher,Table_Companydetailsmaster,Table_companyDetailschild


admin.site.register(Table_Acntchild)
admin.site.register(Table_Accountsmaster)



class TableVoucherAdmin(admin.ModelAdmin):
    list_display = ('Series', 'VoucherNo', 'Vdate', 'Accountcode', 'Headcode', 'payment', 'VAmount', 'VType', 'Narration', 'CStatus', 'UserID', 'FYCode', 'Coid', 'Branch_ID')
    search_fields = ('Series', 'VoucherNo', 'Accountcode', 'Headcode', 'Narration')
    list_filter = ('Series', 'Vdate', 'VType', 'CStatus')

admin.site.register(Table_Voucher, TableVoucherAdmin)

@admin.register(VoucherConfiguration)
class VoucherConfigurationAdmin(admin.ModelAdmin):
    list_display = ('category', 'series', 'serial_no')
    search_fields = ('category', 'series')
    list_filter = ('category',)



class CompanydetailsmasterAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'companyname', 'email', 'gst', 'pan')

class CompanyDetailschildAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'fycode', 'finyearfrom', 'finyearto', 'databasename1')

admin.site.register(Table_Companydetailsmaster, CompanydetailsmasterAdmin)
admin.site.register(Table_companyDetailschild, CompanyDetailschildAdmin)

