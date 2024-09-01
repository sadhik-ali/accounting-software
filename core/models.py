from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Max
from django.utils import timezone



# Create your models here.


class AccountMaster(models.Model):
    account_code = models.IntegerField()
    opbal = models.FloatField()
    curbal = models.FloatField()
    drcr = models.CharField(max_length=100)
    disp = models.CharField(max_length=1)
    coid = models.CharField(max_length=1)
    brid = models.CharField(max_length=1)
    FYCcode = models.CharField(max_length=1)


    def __str__(self):
        return self.account_code


class Table_Accountsmaster(models.Model):
    account_code = models.IntegerField(blank=True, null=True, unique=True)
    head = models.CharField(max_length=100, unique=True)

    GROUP_CHOICES = [
        ('LIABILITIES', 'LIABILITIES'),
        ('INCOME', 'INCOME'),
        ('EXPENSES', 'EXPENSES'),
        ('TRADING EXPENSES', 'TRADING EXPENSES'),
        ('TRADING INCOME', 'TRADING INCOME'),
        ('CURRENT ASSET', 'CURRENT ASSET'),
        ('FIXED ASSETS', 'FIXED ASSETS'),
        ('CURRENT LIABILITIES', 'CURRENT LIABILITIES'),
        ('INDIRECT INCOME', 'INDIRECT INCOME'),
        ('INDIRECT EXPENSES', 'INDIRECT EXPENSES'),
        ('SUNDRY DEBTORS', 'SUNDRY DEBTORS'),
        ('SUNDRY CREDITORS', 'SUNDRY CREDITORS'),
        ('CASH AT BANK', 'CASH AT BANK'),
        ('DUTIES AND TAXES', 'DUTIES AND TAXES'),
        ('LOANS', 'LOANS'),
        ('CAPITAL ACCOUNT', 'CAPITAL ACCOUNT'),
    ]

    group = models.CharField(max_length=249, choices=GROUP_CHOICES)

    CATEGORY_CHOICES = [
        ('Accounts', 'Accounts'),
        ('Cashbook', 'Cashbook'),
        ('Bank', 'Bank'),
        ('Customers', 'Customers'),
        ('Suppliers', 'Suppliers'),
    ]
    category = models.CharField(max_length=249, choices=CATEGORY_CHOICES)

    PRICEGROUP_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ]
    pricegroup = models.CharField(max_length=249, null=True, blank=True, choices=PRICEGROUP_CHOICES)

    DEBIT_CREDIT_CHOICES = [
        ('Debit', 'Debit'),
        ('Credit', 'Credit'),
    ]
    debitcredit = models.CharField(max_length=249, choices=DEBIT_CREDIT_CHOICES)

    gstno = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=299, null=True, blank=True)
    state = models.CharField(max_length=249, null=True, blank=True)
    address2 = models.CharField(max_length=299, null=True, blank=True)
    statecode = models.CharField(max_length=249, null=True, blank=True)
    address3 = models.CharField(max_length=249, null=True, blank=True)
    panno = models.CharField(max_length=249, null=True, blank=True)
    district = models.CharField(max_length=249, null=True, blank=True)
    creditlimit = models.CharField(max_length=249, null=True, blank=True)
    email = models.CharField(max_length=249, null=True, blank=True)
    creditdays = models.CharField(max_length=249, null=True, blank=True)
    telno = models.CharField(max_length=50,null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    opbalance = models.IntegerField(null=True, blank=True, default=0)
    whattsapp = models.CharField(max_length=249, null=True, blank=True)
    currentbalance = models.CharField(max_length=249, null=True, blank=True)
    slug = models.SlugField(max_length=250, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.account_code:
            last_id = Table_Accountsmaster.objects.aggregate(max_id=Max('account_code'))['max_id']
            self.account_code = (last_id or 999) + 1

        if self.head:
            self.head = self.head.upper()

        if not self.slug:
            self.slug = slugify(self.head)

        if self.whattsapp is None:
            self.whattsapp = ""

        super(Table_Accountsmaster, self).save(*args, **kwargs)

        # Ensure the corresponding Table_Acntchild instance is created or updated
        Table_Acntchild.objects.update_or_create(
            account_master=self,
            defaults={
                'account_code': self.account_code,
                'openning_balance': self.opbalance,
                'current_balance': self.opbalance or 0,
                'debit_Credit': self.debitcredit,
                'disp': 'Y', 
                'company_id': 'C', 
                'branch_id': '1', 
                'fyc_code': '2024-2025' 
            }
        )


    def __str__(self):
        return f"{self.head} ({self.account_code})"

    def get_absolute_url(self):
        return reverse("web:account_master_detail", kwargs={"slug": self.slug})



class VoucherConfiguration(models.Model):
    CATEGORY_CHOICES = [
        ('receipt', 'Receipt'),
        ('payment', 'Payment'),
        ('Debit Note', 'Debit Note'),
        ('Credit Note', 'Credit Note'),
    ]
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    series = models.CharField(max_length=255)
    serial_no = models.IntegerField()

    class Meta:
        unique_together = ('category', 'series')

    def __str__(self):
        return f"{self.category} - {self.series} - {self.serial_no}"
    


class Table_Companydetailsmaster(models.Model):
    company_id = models.CharField(max_length=1, unique=True)
    companyname = models.CharField(max_length=50, unique=True)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    address3 = models.CharField(max_length=50, blank=True, null=True)
    pinCode = models.IntegerField()
    phoneno = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    gst = models.CharField(max_length=30, unique=True)
    pan = models.CharField(max_length=30, blank=True, null=True)
    finyearfrom = models.DateField()
    finyearto = models.DateField(blank=True, null=True)
    slug = models.SlugField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.company_id

    def save(self, *args, **kwargs):
        # Generate slug from the company name if not set
        if not self.slug:
            self.slug = slugify(self.companyname)
        super().save(*args, **kwargs)
        
        # Calculate fycode based on finyearfrom and finyearto
        fycode = f"{self.finyearfrom.year}-{self.finyearto.year}"

        Table_companyDetailschild.objects.update_or_create(
            company_id=self,
            defaults={
                'finyearfrom': str(self.finyearfrom),
                'finyearto': str(self.finyearto),
                'fycode': fycode,
                'databasename1': 'databasename1',  # This should ideally be dynamic or provided
            }
        )

    def get_absolute_url(self):
        return reverse("web:companymaster_detail", kwargs={"slug": self.slug})


class Table_companyDetailschild(models.Model):
    company_id = models.ForeignKey(Table_Companydetailsmaster, on_delete=models.CASCADE)
    fycode = models.CharField(max_length=20)
    finyearfrom = models.CharField(max_length=19)
    finyearto = models.CharField(max_length=10, blank=True, null=True)
    databasename1 = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.company_id.companyname} - {self.fycode}"


class Table_Voucher(models.Model):
    Series = models.CharField(max_length=255, blank=True, null=True)
    VoucherNo = models.IntegerField(blank=True, null=True)
    Vdate = models.DateField(blank=True, null=True)
    Accountcode = models.CharField(max_length=255, blank=True, null=True)
    Headcode = models.CharField(max_length=255, blank=True, null=True)
    CStatus = models.CharField(max_length=255, blank=True, null=True)
    payment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    VAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    VType = models.CharField(max_length=255, blank=True, null=True)
    Narration = models.TextField(blank=True, null=True)
    UserID = models.CharField(max_length=255, blank=True, null=True)
    FYCode = models.CharField(max_length=255, blank=True, null=True)
    Coid = models.CharField(max_length=255, blank=True, null=True)
    Branch_ID = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.Series} - {self.VoucherNo}"


class Table_Acntchild(models.Model):
    account_master = models.ForeignKey(Table_Accountsmaster, on_delete=models.CASCADE, related_name='children')
    account_code = models.CharField(max_length=20)
    openning_balance = models.CharField(max_length=19)
    current_balance = models.CharField(max_length=10)   
    debit_Credit = models.CharField(max_length=10)
    disp = models.CharField(max_length=10)
    company_id = models.CharField(max_length=10)
    branch_id = models.CharField(max_length=10)
    fyc_code = models.CharField(max_length=10)



class Table_DrCrNote(models.Model):
    series = models.CharField(max_length=15, null=True, blank=True)
    noteno = models.CharField(max_length=15, null=True, blank=True)
    ndate = models.DateField(default=timezone.now, null=True, blank=True)
    accountcode = models.CharField(max_length=15, null=True, blank=True)
    narration = models.CharField(max_length=100, null=True, blank=True)
    dramount = models.CharField(max_length=15, null=True, blank=True)
    cramount = models.CharField(max_length=15, null=True, blank=True)
    ntype = models.CharField(max_length=1, null=True, blank=True)
    userid = models.CharField(max_length=25, null=True, blank=True)
    coid = models.CharField(max_length=1, null=True, blank=True)
    fycode = models.CharField(max_length=15, null=True, blank=True)
    brid = models.CharField(max_length=1, null=True, blank=True)

    def __str__(self):
        return f"Series: {self.series}, Noteno: {self.noteno}, Date: {self.ndate}"
