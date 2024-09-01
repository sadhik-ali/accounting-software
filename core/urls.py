from django.urls import path
from . import views
from .views import (AccountCreditNoteView,SearchReceiptView,SearchDebitTableView,PaymentListTable,AccountCreditTableView,
                    AccountDebitTableView,SearchCreditTableView,DeleteDebitNoteView,ReceiptListTable,
                    EditPaymentView,SearchPaymentView,AccountmMasterUserView,
                    DeleteAccountmMasterUserView,DeleteCreditNoteView, AccountMasterDetailView, 
                    AccountMasterView,EditAccountmMasterUserView,VoucherConfigurationListView,
                    CompanyDetailsMasterView,VoucherConfigurationTable,
                    CompanyMasterUserView,CompanyMasterDetailView,DeletecompanymMasterUserView,
                    EditCompanyMasterUserView,ValidateVoucherConfiguration,EnterAmountView,
                    PaymentEnterAmountView,AccountDebitNoteView,EditReceiptView,
                    )
app_name = "core"

urlpatterns = [
    # Main 
    path("", views.index, name="index"),

    # franchise - accounts - debit-note
    path("accounts/debit-note/",AccountDebitNoteView.as_view(),name="account_debit_note"),
    path('accounts/debit-note/delete/<int:pk1>/<int:pk2>/', DeleteDebitNoteView.as_view(), name='delete_debit_note'),
    path("accounts/debit-note/search/",SearchDebitTableView.as_view(),name="search_debit_note"),
    path("accounts/debit-note/<str:series>/<int:serial_no>/", AccountDebitNoteView.as_view(), name="account_debit_note"),
    path("accounts/debit-note/table/",AccountDebitTableView.as_view(),name="account_debit_table"),
    # franchise - accounts - credit-note
    path("accounts/credit-note/",AccountCreditNoteView.as_view(),name="account_credit_note"),
    path("accounts/credit-note/table/",AccountCreditTableView.as_view(),name="account_credit_table"),
    path("accounts/credit-note/search/",SearchCreditTableView.as_view(),name="search_credit_note"),
    path('accounts/credit-note/<str:series>/<str:serial_no>/', AccountCreditNoteView.as_view(), name='account_credit_note'),
    path('accounts/credit-note/delete/<int:pk1>/<int:pk2>/', DeleteCreditNoteView.as_view(), name='delete_credit_note'),
    # franchise - accounts - company master
    path('accounts/company-master/details/', CompanyDetailsMasterView.as_view(), name='company_details_master'),
    path('accounts/company-master/list/',CompanyMasterUserView.as_view(),name='company_master_list'),
    path('accounts/company-master/<slug:slug>/', CompanyMasterDetailView.as_view(), name='companymaster_detail'),
    path("accounts/company-master/delete/<int:pk>/",DeletecompanymMasterUserView.as_view(),name="delete_company_master_list",),
    path("accounts/company-master/edit/<int:pk>/",EditCompanyMasterUserView.as_view(),name="edit_company_master_list"),
    # franchise - accounts - account master
    path('accounts/account-master/', AccountMasterView.as_view(), name='acc_master'),
    path('accounts/account-master/list/',AccountmMasterUserView.as_view(),name='acc_master_list'),
    path("accounts/account-master/delete/<int:pk>/",DeleteAccountmMasterUserView.as_view(),name="delete_acc_master_list",),
    path('accounts/account-master/<slug:slug>/', AccountMasterDetailView.as_view(), name='account_master_detail'),
    path("accounts/account-master/list/edit/<int:pk>/",EditAccountmMasterUserView.as_view(),name="edit_acc_master_list"),
    # franchise - accounts - voucher configuration 
    path('accounts/voucher-configuration/list/search/', VoucherConfigurationTable.as_view(), name='voucher_search'),
    path('accounts/voucher-configuration/', VoucherConfigurationListView.as_view(), name='voucher_configuration'),
    path('accounts/validate-voucher-configuration/', ValidateVoucherConfiguration.as_view(), name='validate_voucher_configuration'),
    # franchise - accounts - receipt voucher
    path('accounts/receipt-voucher/', EnterAmountView.as_view(), name='receipt'),
    path("accounts/receipt-voucher/list/", ReceiptListTable.as_view(), name="receipt_list"),
    path('accounts/receipt-voucher-modify/', SearchReceiptView.as_view(), name='receipt_modify'),
    path('accounts/receipt-voucher/edit/', EditReceiptView.as_view(), name='edit_receipt'),
    # franchise - accounts - payment voucher
    path('accounts/payment-voucher/edit/', EditPaymentView.as_view(), name='edit_payment'),
    path('accounts/payment-voucher-modify/', SearchPaymentView.as_view(), name='payment_modify'),
    path('accounts/payment-voucher/', PaymentEnterAmountView.as_view(), name='payment'),
    path("accounts/payment-voucher/list/", PaymentListTable.as_view(), name="payment_list"),

]

