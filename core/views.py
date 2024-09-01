from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model, login as auth_login
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views import View
from django.db import IntegrityError, transaction
from django.http import JsonResponse, HttpResponseRedirect
import logging, json
from django.core import serializers
logger = logging.getLogger(__name__)
User = get_user_model()
# CRUD operations
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView)
# forms
from .forms import (AccountMasterForm, ComapnyDetailsMasterForm)
# models
from .models import (VoucherConfiguration,Table_Accountsmaster,Table_Companydetailsmaster, Table_Voucher, Table_Acntchild,
                     Table_DrCrNote, Table_companyDetailschild)



def index(request):
    return render(request, 'web/index.html')


class AccountMasterView(CreateView):
    model = Table_Accountsmaster
    form_class = AccountMasterForm
    template_name = 'web/accounts/account-master/acc-master.html'
    success_url = reverse_lazy("core:acc_master")

    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            if self.object.opbalance is None:
                self.object.opbalance = 0
            if self.object.whattsapp is None:
                self.object.whattsapp = ""
            self.object.save()
            messages.success(self.request, 'Account created successfully!')
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('head', 'This head already exists. Please choose a different one.')
            return self.form_invalid(form)


class AccountmMasterUserView(ListView):
    model = Table_Accountsmaster
    template_name = "web/accounts/account-master/acc_master_list.html"
    context_object_name = "userlists"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(head__icontains=search_query)
        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            qs_json = serializers.serialize('json', self.get_queryset())
            return JsonResponse({'results': json.loads(qs_json)}, safe=False)
        else:
            return super(AccountmMasterUserView, self).render_to_response(context, **response_kwargs)


class DeleteAccountmMasterUserView(DeleteView):
    model = Table_Accountsmaster
    success_url = reverse_lazy("core:acc_master")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Account Deleted Successfully")  # Add success message here
        return HttpResponseRedirect(success_url)


class AccountMasterDetailView(DetailView):
    model = Table_Accountsmaster
    template_name = 'web/accounts/account-master/acc_master_detail.html'  # Assuming you have a template for blog detail
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')  # Get slug from URL parameters
        userlists = get_object_or_404(Table_Accountsmaster, slug=slug)
        context["userlist"] = userlists
        return context


class EditAccountmMasterUserView(UpdateView):
    model = Table_Accountsmaster
    form_class = AccountMasterForm
    template_name = 'web/accounts/account-master/acc-master.html'

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, "Account edited successfully!")
            return response
        except IntegrityError:
            form.add_error('head', 'This head already exists. Please choose a different one.')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('core:account_master_detail', kwargs={'slug': self.object.slug})
    

class CompanyDetailsMasterView(CreateView):
    model = Table_Companydetailsmaster
    form_class = ComapnyDetailsMasterForm
    template_name = 'web/accounts/company-master/companydetailsmaster.html'
    success_url = reverse_lazy("core:company_details_master")
    success_message = "Company Details Created Successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class CompanyMasterUserView(ListView):
    model = Table_Companydetailsmaster
    template_name = "web/accounts/company-master/companymaster_list.html"
    context_object_name = "companylists"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(head__icontains=search_query)
        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            qs_json = serializers.serialize('json', self.get_queryset())
            return JsonResponse({'results': json.loads(qs_json)}, safe=False)
        else:
            return super(CompanyMasterUserView, self).render_to_response(context, **response_kwargs)


class CompanyMasterDetailView(DetailView):
    model = Table_Companydetailsmaster
    template_name = 'web/accounts/company-master/companymaster_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        companylists = get_object_or_404(Table_Companydetailsmaster, slug=slug)
        context["companylist"] = companylists
        return context


class DeletecompanymMasterUserView(DeleteView):
    model = Table_Companydetailsmaster
    success_url = reverse_lazy("core:company_details_master")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "Account Deleted Successfully")
        return HttpResponseRedirect(success_url)


class EditCompanyMasterUserView(UpdateView):
    model = Table_Companydetailsmaster
    form_class = ComapnyDetailsMasterForm
    template_name = 'web/accounts/company-master/companydetailsmaster.html'

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, "Account edited successfully!")
            return response
        except IntegrityError:
            form.add_error('head', 'This head already exists. Please choose a different one.')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('core:companymaster_detail', kwargs={'slug': self.object.slug})


class VoucherConfigurationListView(ListView, View):
    model = VoucherConfiguration
    template_name = 'web/accounts/voucher-configuration/voucher_configuration.html'
    success_url = reverse_lazy('core:voucher_configuration')

    def get(self, request, *args, **kwargs):
        configurations = VoucherConfiguration.objects.all()
        next_serial_numbers = {}

        for config in configurations:
            category_series = (config.category, config.series)
            last_serial = VoucherConfiguration.objects.filter(
                category=config.category,
                series=config.series
            ).order_by('-serial_no').first()
            if last_serial:
                next_serial_numbers[category_series] = last_serial.serial_no
            else:
                next_serial_numbers[category_series] = 1

        context = {
            'object_list': configurations,
            'next_serial_numbers': next_serial_numbers
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        category = request.POST.get('category')
        series = request.POST.get('series')
        serial_no = request.POST.get('serial_no')

        if category and series and serial_no:
            try:
                VoucherConfiguration.objects.create(
                    category=category,
                    series=series,
                    serial_no=serial_no
                )
                return redirect(self.success_url)
            except IntegrityError:
                context = {
                    'object_list': VoucherConfiguration.objects.all(),
                    'error': 'This combination of category and series already exists.'
                }
                return render(request, self.template_name, context)

        context = {
            'object_list': VoucherConfiguration.objects.all(),
            'error': 'All fields are required.'
        }
        return render(request, self.template_name, context)


class ValidateVoucherConfiguration(View):
    def get(self, request, *args, **kwargs):
        series = request.GET.get('series')
        next_serial_no = 1  # Default to 1 if no existing serial number

        if series:
            last_serial = Table_Voucher.objects.filter(Series=series).order_by('-VoucherNo').first()
            if last_serial:
                next_serial_no = last_serial.VoucherNo

        return JsonResponse({'next_serial_no': next_serial_no})
    

class EnterAmountView(View):
    template_name = 'web/accounts/receipt/receipt.html'

    def get(self, request, *args, **kwargs):
        vouchers = VoucherConfiguration.objects.filter(category='receipt')
        accountmas = Table_Accountsmaster.objects.filter(category__in=['Cashbook', 'Bank'])
        head_accounts = Table_Accountsmaster.objects.exclude(category__in=['Cashbook', 'Bank'])

        next_serial_numbers = {}
        for voucher in vouchers:
            last_serial = Table_Voucher.objects.filter(
                Series=voucher.series, CStatus='R'
            ).order_by('-VoucherNo').first()
            if last_serial:
                next_serial_numbers[voucher.series] = str(last_serial.VoucherNo)
            else:
                next_serial_numbers[voucher.series] = voucher.serial_no

        table_acntchildren = Table_Acntchild.objects.select_related('account_master').filter(
            account_master__category__in=['Bank', 'Cashbook']
        )

        return render(request, self.template_name, {
            'vouchers': vouchers,
            'accountmas': accountmas,
            'head_accounts': head_accounts,
            'next_serial_numbers': next_serial_numbers,
            'table_acntchildren': table_acntchildren,
            'user_id': request.user.id,
        })

    def post(self, request, *args, **kwargs):
        try:
            series = request.POST.get('Series')
            vdate = request.POST.get('Vdate')
            headcode = request.POST.get('Headcode')
            user_id = request.user.id
            fy_code = '2024-2025'
            coid = 'C'
            branch_id = '1'

            accountcodes = request.POST.getlist('Accountcode[]')
            narrations = request.POST.getlist('Narration[]')
            vtypes = request.POST.getlist('VType[]')
            payments = request.POST.getlist('payment[]')

            if not (len(accountcodes) == len(narrations) == len(vtypes) == len(payments)):
                raise ValueError("Mismatched input lengths in form data.")

            total_amount = sum(float(payment) for payment in payments)

            voucher_config = VoucherConfiguration.objects.get(series=series, category='receipt')
            current_serial_no = int(voucher_config.serial_no)
            voucher_no = current_serial_no

            with transaction.atomic():
                for accountcode, narration, vtype, payment in zip(accountcodes, narrations, vtypes, payments):
                    Table_Voucher.objects.create(
                        Series=series,
                        VoucherNo=voucher_no,
                        Vdate=vdate,
                        Accountcode=accountcode,
                        Headcode=headcode,
                        payment=payment,
                        VAmount=total_amount,
                        VType=vtype,
                        Narration=narration,
                        CStatus='R',
                        UserID=user_id,
                        FYCode=fy_code,
                        Coid=coid,
                        Branch_ID=branch_id
                    )

                voucher_config.serial_no = voucher_no + 1
                voucher_config.save()

            return redirect('success_url_name')
        except Exception as e:
            return render(request, self.template_name, {
                'error': str(e),
                'vouchers': VoucherConfiguration.objects.filter(category='receipt'),
                'accountmas': Table_Accountsmaster.objects.filter(category__in=['Cashbook', 'Bank']),
                'head_accounts': Table_Accountsmaster.objects.exclude(category__in=['Cashbook', 'Bank']),
                'table_acntchildren': Table_Acntchild.objects.select_related('account_master').filter(
                    account_master__category__in=['Bank', 'Cashbook']
                ),
                'user_id': request.user.id,
            })
        

class PaymentEnterAmountView(View):
    template_name = 'web/accounts/payment/payment.html'

    def get(self, request, *args, **kwargs):
        vouchers = VoucherConfiguration.objects.filter(category='payment')
        accountmas = Table_Accountsmaster.objects.filter(category__in=['Cashbook', 'Bank'])
        head_accounts = Table_Accountsmaster.objects.exclude(category__in=['Cashbook', 'Bank'])

        next_serial_numbers = {}
        for voucher in vouchers:
            last_serial = Table_Voucher.objects.filter(
                Series=voucher.series
            ).order_by('-VoucherNo').first()
            if last_serial:
                next_serial_numbers[voucher.series] = str(int(last_serial.VoucherNo) + 1)
            else:
                next_serial_numbers[voucher.series] = voucher.serial_no

        table_acntchildren = Table_Acntchild.objects.select_related('account_master').filter(
            account_master__category__in=['Bank', 'Cashbook']
        )

        return render(request, self.template_name, {
            'vouchers': vouchers,
            'accountmas': accountmas,
            'head_accounts': head_accounts,
            'next_serial_numbers': next_serial_numbers,
            'table_acntchildren': table_acntchildren,
            'user_id': request.user.id,
        })

    def post(self, request, *args, **kwargs):
        try:
            series = request.POST.get('Series')
            vdate = request.POST.get('Vdate')
            headcode = request.POST.get('Headcode')
            user_id = request.user.id
            fy_code = '2024-2025'
            coid = 'C'
            branch_id = '1'

            accountcodes = request.POST.getlist('Accountcode[]')
            narrations = request.POST.getlist('Narration[]')
            vtypes = request.POST.getlist('VType[]')
            payments = request.POST.getlist('payment[]')

            # Ensure all lists are of the same length
            if not (len(accountcodes) == len(narrations) == len(vtypes) == len(payments)):
                raise ValueError("Mismatched input lengths in form data.")

            # Calculate the total amount
            total_amount = sum(float(payment) for payment in payments)

            # Fetch or initialize the current serial number for the selected series
            voucher_config = VoucherConfiguration.objects.get(series=series, category='payment')
            current_serial_no = voucher_config.serial_no

            # Increment the serial number for this form submission
            voucher_no = current_serial_no + 1

            with transaction.atomic():
                for accountcode, narration, vtype, payment in zip(accountcodes, narrations, vtypes, payments):
                    Table_Voucher.objects.create(
                        Series=series,
                        VoucherNo=voucher_no,
                        Vdate=vdate,
                        Accountcode=accountcode,
                        Headcode=headcode,
                        payment=payment,
                        VAmount=total_amount,  # Save the total amount
                        VType=vtype,
                        Narration=narration,
                        CStatus='P',
                        UserID=user_id,
                        FYCode=fy_code,
                        Coid=coid,
                        Branch_ID=branch_id
                    )

                    # Update Table_Acntchild with FYCode and Coid
                    account_child = Table_Acntchild.objects.get(account_code=accountcode)
                    account_child.fyc_code = fy_code
                    account_child.company_id = coid
                    account_child.branch_id = branch_id
                    account_child.save()

                # Update the serial number in VoucherConfiguration for the next use
                voucher_config.serial_no = voucher_no
                voucher_config.save()

            print("Payment saved successfully!")
            return redirect('success_url_name')  # Redirect to success page after saving
        except Exception as e:
            print("Error saving payment: ", e)
            return render(request, self.template_name, {
                'error': str(e),
                'vouchers': VoucherConfiguration.objects.filter(category='payment'),
                'accountmas': Table_Accountsmaster.objects.filter(category__in=['Cashbook', 'Bank']),
                'head_accounts': Table_Accountsmaster.objects.exclude(category__in=['Cashbook', 'Bank']),
                'table_acntchildren': Table_Acntchild.objects.select_related('account_master').filter(
                    account_master__category__in=['Bank', 'Cashbook']
                ),
                'user_id': request.user.id,
            })


class ReceiptListTable(ListView):
    model = Table_Voucher
    template_name = 'web/accounts/receipt/receipt_list.html'
    context_object_name = "vouchers"

    def get_queryset(self):
        # Get all series related to the receipt category from VoucherConfiguration
        receipt_series = VoucherConfiguration.objects.filter(category='receipt').values_list('series', flat=True)
        
        # Filter Table_Voucher based on the series related to the receipt category and CStatus being 'R'
        return Table_Voucher.objects.filter(Series__in=receipt_series, CStatus='R')


class PaymentListTable(ListView):
    model = Table_Voucher
    template_name = 'web/accounts/payment/payment_list.html'
    context_object_name = "vouchers"

    def get_queryset(self):
        # Get all series related to the payment category from VoucherConfiguration
        payment_series = VoucherConfiguration.objects.filter(category='payment').values_list('series', flat=True)
        
        # Filter Table_Voucher based on the series related to the payment category and CStatus being 'R'
        return Table_Voucher.objects.filter(Series__in=payment_series, CStatus='P')


class ModifyPaymentTableView(TemplateView):
    template_name = 'web/accounts/payment/payment_modify.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['series_options'] = VoucherConfiguration.objects.filter(category='payment').values('series')
        return context

    def post(self, request, *args, **kwargs):
        series = request.POST.get('series')
        voucher_no = request.POST.get('voucher_no')  # Change from serial_no to VoucherNo

        if series and voucher_no:
            # Check if the voucher number exists
            if Table_Voucher.objects.filter(Series=series, VoucherNo=voucher_no, CStatus='R').exists():
                return redirect(reverse('core:account_debit_note', kwargs={'series': series, 'voucher_no': voucher_no}))
            else:
                context = self.get_context_data(**kwargs)
                context['error'] = 'This voucher number does not exist or does not match the criteria.'
                return render(request, self.template_name, context)
        
        context = self.get_context_data(**kwargs)
        context['error'] = 'Please enter both series and voucher number.'
        return render(request, self.template_name, context)


class VoucherConfigurationTable(ListView):
    model = VoucherConfiguration
    template_name = 'web/accounts/voucher-configuration/voucher_search.html'
    context_object_name = "voucherconfiguration"


class AccountDebitNoteView(TemplateView):
    template_name = 'web/accounts/debit-note/debit-note.html'
    success_url = reverse_lazy('core:account_debit_note')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        series = self.kwargs.get('series')
        serial_no = self.kwargs.get('serial_no')
        context['series_options'] = VoucherConfiguration.objects.filter(category='Debit Note').values('series', 'serial_no')
        excluded_categories = ['Bank', 'Cashbook']
        head_options = Table_Accountsmaster.objects.exclude(category__in=excluded_categories).values('head', 'account_code')
        context['head_options'] = head_options
        context['drcrnotes'] = Table_DrCrNote.objects.filter(ntype='D')  # Only get Debit notes
        context['series'] = series
        context['serial_no'] = serial_no

        # Check if the series and serial_no match an entry
        if series and serial_no:
            matched_notes = Table_DrCrNote.objects.filter(series=series, noteno=serial_no, ntype='D')
            if matched_notes.exists():
                # Assuming the matched_notes contains two entries for Dr and Cr respectively
                matched_note_dr = matched_notes.filter(dramount__gt=0).first()
                matched_note_cr = matched_notes.filter(cramount__gt=0).first()

                if matched_note_dr:
                    matched_note_dr.head = Table_Accountsmaster.objects.get(account_code=matched_note_dr.accountcode).head
                if matched_note_cr:
                    matched_note_cr.head = Table_Accountsmaster.objects.get(account_code=matched_note_cr.accountcode).head

                if matched_note_dr:
                        matched_note_dr.ndate = matched_note_dr.ndate.strftime('%Y-%m-%d')  # Ensure date format matches HTML input type


                context['matched_note_dr'] = matched_note_dr
                context['matched_note_cr'] = matched_note_cr

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        series = request.POST.get('series')
        serial_no = request.POST.get('serial_no')
        date = request.POST.get('date')
        total_amount = request.POST.get('total_amount')
        head1 = request.POST.get('head1')
        narration1 = request.POST.get('narration1')
        debit1 = request.POST.get('debit1')
        head2 = request.POST.get('head2')
        narration2 = request.POST.get('narration2')
        credit2 = request.POST.get('credit2')

        try:
            # Check if the series and serial_no match an entry
            if series and serial_no:
                matched_notes = Table_DrCrNote.objects.filter(series=series, noteno=serial_no)
                if matched_notes.exists():
                    # Update existing entries
                    dr_note = matched_notes.filter(dramount__gt=0).first()
                    cr_note = matched_notes.filter(cramount__gt=0).first()
                    if dr_note:
                        dr_note.ndate = date
                        dr_note.accountcode = head1
                        dr_note.narration = narration1
                        dr_note.dramount = debit1
                        dr_note.userid = request.user.username
                        dr_note.save()
                    if cr_note:
                        cr_note.ndate = date
                        cr_note.accountcode = head2
                        cr_note.narration = narration2
                        cr_note.cramount = credit2
                        cr_note.userid = request.user.username
                        cr_note.save()
                    messages.success(request, 'Debit note updated successfully.')
                else:
                    # Create new entries if no existing match
                    self.create_new_entries(request, series, date, head1, narration1, debit1, head2, narration2, credit2)
            else:
                # Create new entries if no series or serial_no provided
                self.create_new_entries(request, series, date, head1, narration1, debit1, head2, narration2, credit2)

            return redirect(self.success_url)

        except Exception as e:
            messages.error(request, f'Failed to save debit note: {str(e)}')
            return redirect(self.success_url)

    def create_new_entries(self, request, series, date, head1, narration1, debit1, head2, narration2, credit2):
        # Fetch the current serial number and increment by 1
        voucher_config = get_object_or_404(VoucherConfiguration, series=series)
        current_serial_no = voucher_config.serial_no
        next_serial_no = current_serial_no + 1

        # Update the serial number in VoucherConfiguration
        voucher_config.serial_no = next_serial_no
        voucher_config.save()

        # Fetch company details (example: you need to modify this based on your model)
        coid_entry = Table_companyDetailschild.objects.first()
        fycode_entry = Table_companyDetailschild.objects.first()
        coid = coid_entry.company_id if coid_entry else 'C'
        fycode = fycode_entry.fycode if coid_entry else 'NON'

        # Create new Table_DrCrNote objects
        Table_DrCrNote.objects.create(
            series=series,
            ndate=date,
            noteno=current_serial_no,
            accountcode=head1,
            narration=narration1,
            dramount=debit1,
            cramount='0',
            ntype='D',
            userid=request.user.username,
            coid=coid,
            fycode=fycode,
            brid='1'
        )

        Table_DrCrNote.objects.create(
            series=series,
            ndate=date,
            noteno=current_serial_no,
            accountcode=head2,
            narration=narration2,
            dramount='0',
            cramount=credit2,
            ntype='D',
            userid=request.user.username,
            coid=coid,
            fycode=fycode,
            brid='1'
        )

        messages.success(request, 'Debit note created successfully.')


class DeleteDebitNoteView(DeleteView):
    model = Table_DrCrNote
    success_url = reverse_lazy("core:search_debit_note")

    def get_object(self, queryset=None):
        pk1 = self.kwargs.get('pk1')
        pk2 = self.kwargs.get('pk2')
        obj = get_object_or_404(Table_DrCrNote, id=pk1, noteno=pk2)
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()

        # Assuming matched_note_dr refers to the second object to delete
        pk2 = self.kwargs.get('pk2')
        obj2 = get_object_or_404(Table_DrCrNote, noteno=pk2)
        obj2.delete()

        return HttpResponseRedirect(success_url)


class AccountDebitTableView(ListView):
    model = Table_DrCrNote
    template_name = 'web/accounts/debit-note/debit-table.html'
    context_object_name = "drcrnotes"

    def get_queryset(self):
        return super().get_queryset().filter(ntype='D')  # Only show Debit notes in the table


class SearchDebitTableView(TemplateView):
    template_name = 'web/accounts/debit-note/debit-search-box.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['series_options'] = VoucherConfiguration.objects.filter(category='Debit Note').values('series')
        return context

    def post(self, request, *args, **kwargs):
        series = request.POST.get('series')
        serial_no = request.POST.get('serial_no')

        if series and serial_no:
            # Check if the serial number exists
            if Table_DrCrNote.objects.filter(series=series, noteno=serial_no, ntype='D').exists():
                return redirect(reverse('core:account_debit_note', kwargs={'series': series, 'serial_no': serial_no}))
            else:
                context = self.get_context_data(**kwargs)
                context['error'] = 'This serial number does not exist.'
                return render(request, self.template_name, context)
        
        context = self.get_context_data(**kwargs)
        context['error'] = 'Please enter both series and serial number.'
        return render(request, self.template_name, context)
    

class EditDebitTableView(View):
    template_name = 'web/accounts/debit-note/edit-debit-note.html'


class AccountCreditTableView(ListView):
    model = Table_DrCrNote
    template_name = 'web/accounts/credit-note/credit-table.html'
    context_object_name = "drcrnotesss"

    def get_queryset(self):
        return super().get_queryset().filter(ntype='C')  # Only show Debit notes in the table


class AccountCreditNoteView(TemplateView):
    template_name = 'web/accounts/credit-note/credit-note.html'
    success_url = reverse_lazy('core:account_credit_note')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        series = self.kwargs.get('series')
        serial_no = self.kwargs.get('serial_no')
        context['series_options'] = VoucherConfiguration.objects.filter(category='Credit Note').values('series', 'serial_no')
        excluded_categories = ['Bank', 'Cashbook']
        head_options = Table_Accountsmaster.objects.exclude(category__in=excluded_categories).values('head', 'account_code')
        context['head_options'] = head_options
        context['drcrnotes'] = Table_DrCrNote.objects.filter(ntype='C')  # Only get Debit notes
        context['series'] = series
        context['serial_no'] = serial_no

        # Check if the series and serial_no match an entry
        if series and serial_no:
            matched_notes = Table_DrCrNote.objects.filter(series=series, noteno=serial_no, ntype='C')
            if matched_notes.exists():
                # Assuming the matched_notes contains two entries for Dr and Cr respectively
                matched_note_dr = matched_notes.filter(dramount__gt=0).first()
                matched_note_cr = matched_notes.filter(cramount__gt=0).first()

                if matched_note_dr:
                    matched_note_dr.head = Table_Accountsmaster.objects.get(account_code=matched_note_dr.accountcode).head
                if matched_note_cr:
                    matched_note_cr.head = Table_Accountsmaster.objects.get(account_code=matched_note_cr.accountcode).head

                if matched_note_dr:
                        matched_note_dr.ndate = matched_note_dr.ndate.strftime('%Y-%m-%d')  # Ensure date format matches HTML input type

                context['matched_note_dr'] = matched_note_dr
                context['matched_note_cr'] = matched_note_cr

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        series = request.POST.get('series')
        serial_no = request.POST.get('serial_no')
        date = request.POST.get('date')
        total_amount = request.POST.get('total_amount')
        head1 = request.POST.get('head1')
        narration1 = request.POST.get('narration1')
        debit2 = request.POST.get('debit2')
        head2 = request.POST.get('head2')
        narration2 = request.POST.get('narration2')
        credit1 = request.POST.get('credit1')

        try:
            # Check if the series and serial_no match an entry
            if series and serial_no:
                matched_notes = Table_DrCrNote.objects.filter(series=series, noteno=serial_no)
                if matched_notes.exists():
                    # Update existing entries
                    dr_note = matched_notes.filter(cramount__gt=0).first()
                    cr_note = matched_notes.filter(dramount__gt=0).first()
                    if dr_note:
                        dr_note.ndate = date
                        dr_note.accountcode = head1
                        dr_note.narration = narration1
                        dr_note.cramount = credit1
                        dr_note.userid = request.user.username
                        dr_note.save()
                    if cr_note:
                        cr_note.ndate = date
                        cr_note.accountcode = head2
                        cr_note.narration = narration2
                        cr_note.dramount = debit2
                        cr_note.userid = request.user.username
                        cr_note.save()
                    messages.success(request, 'Credit note updated successfully.')
                else:
                    # Create new entries if no existing match
                    self.create_new_entries(request, series, date, head1, narration1, credit1, head2, narration2, debit2)
            else:
                # Create new entries if no series or serial_no provided
                self.create_new_entries(request, series, date, head1, narration1,credit1, head2, narration2, debit2)

            return redirect(self.success_url)

        except Exception as e:
            messages.error(request, f'Failed to save credit note: {str(e)}')
            return redirect(self.success_url)

    def create_new_entries(self, request, series, date, head1, narration1, credit1, head2, narration2,  debit2):
        # Fetch the current serial number and increment by 1
        voucher_config = get_object_or_404(VoucherConfiguration, series=series)
        current_serial_no = voucher_config.serial_no
        next_serial_no = current_serial_no + 1

        # Update the serial number in VoucherConfiguration
        voucher_config.serial_no = next_serial_no
        voucher_config.save()

        # Fetch company details (example: you need to modify this based on your model)
        coid_entry = Table_companyDetailschild.objects.first()
        fycode_entry = Table_companyDetailschild.objects.first()
        coid = coid_entry.company_id if coid_entry else 'NON'
        fycode = fycode_entry.fycode if coid_entry else 'NON'

        # Create new Table_DrCrNote objects
        Table_DrCrNote.objects.create(
            series=series,
            ndate=date,
            noteno=current_serial_no,
            accountcode=head1,
            narration=narration1,
            dramount='0',
            cramount=credit1,
            ntype='C',
            userid=request.user.username,
            coid=coid,
            fycode=fycode,
            brid='1'
        )

        Table_DrCrNote.objects.create(
            series=series,
            ndate=date,
            noteno=current_serial_no,
            accountcode=head2,
            narration=narration2,
            dramount=debit2,
            cramount='0',
            ntype='C',
            userid=request.user.username,
            coid=coid,
            fycode=fycode,
            brid='1'
        )

        messages.success(request, 'Credit note created successfully.')


class SearchCreditTableView(TemplateView):
    template_name = 'web/accounts/credit-note/credit-search-box.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['series_options'] = VoucherConfiguration.objects.filter(category='Credit Note').values('series')
        return context

    def post(self, request, *args, **kwargs):
        series = request.POST.get('series')
        serial_no = request.POST.get('serial_no')

        if series and serial_no:
            # Check if the serial number exists
            if Table_DrCrNote.objects.filter(series=series, noteno=serial_no, ntype='C').exists():
                return redirect(reverse('core:account_credit_note', kwargs={'series': series, 'serial_no': serial_no}))
            else:
                context = self.get_context_data(**kwargs)
                context['error'] = 'This serial number does not exist.'
                return render(request, self.template_name, context)
        
        context = self.get_context_data(**kwargs)
        context['error'] = 'Please enter both series and serial number.'
        return render(request, self.template_name, context)


class DeleteCreditNoteView(DeleteView):
    model = Table_DrCrNote
    success_url = reverse_lazy("core:search_credit_note")

    def get_object(self, queryset=None):
        pk1 = self.kwargs.get('pk1')
        pk2 = self.kwargs.get('pk2')
        obj = get_object_or_404(Table_DrCrNote, id=pk1, noteno=pk2)
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()

        # Assuming matched_note_dr refers to the second object to delete
        pk2 = self.kwargs.get('pk2')
        obj2 = get_object_or_404(Table_DrCrNote, noteno=pk2)
        obj2.delete()

        return HttpResponseRedirect(success_url)


class SearchPaymentView(View):
    template_name = 'web/accounts/payment/payment_modify.html'

    def get(self, request, *args, **kwargs):
        vouchers = VoucherConfiguration.objects.filter(category='payment')
        return render(request, self.template_name, {'vouchers': vouchers})


class EditPaymentView(View):
    template_name = 'web/accounts/payment/edit_payment.html'

    def get(self, request, *args, **kwargs):
        series = request.GET.get('Series')
        voucher_no = request.GET.get('VoucherNo')

        vouchers = VoucherConfiguration.objects.filter(category='payment')
        accountmas = Table_Accountsmaster.objects.filter(category__in=['Cashbook', 'Bank'])
        head_accounts = Table_Accountsmaster.objects.exclude(category__in=['Cashbook', 'Bank'])
        table_acntchildren = Table_Acntchild.objects.select_related('account_master').filter(
            account_master__category__in=['Bank', 'Cashbook']
        )

        # Fetch voucher entries for the given series and voucher number
        voucher_entries = Table_Voucher.objects.filter(Series=series, VoucherNo=voucher_no)

        if not voucher_entries:
            return redirect('core:search_payment')  # Ensure this matches the name in urls.py

        return render(request, self.template_name, {
            'vouchers': vouchers,
            'accountmas': accountmas,
            'head_accounts': head_accounts,
            'table_acntchildren': table_acntchildren,
            'voucher_entries': voucher_entries,
            'user_id': request.user.id,
        })

    def post(self, request, *args, **kwargs):
        voucher_entries = []  # Initialize voucher_entries to avoid reference issues
        try:
            series = request.POST.get('Series')
            vdate = request.POST.get('Vdate')
            headcode = request.POST.get('Headcode')
            user_id = request.user.id
            fy_code = '2024-2025'
            coid = 'C'
            branch_id = '1'

            accountcodes = request.POST.getlist('Accountcode[]')
            narrations = request.POST.getlist('Narration[]')
            vtypes = request.POST.getlist('VType[]')
            payments = request.POST.getlist('payment[]')
            voucher_no = request.POST.get('VoucherNo')

            # Ensure all lists are of the same length
            if not (len(accountcodes) == len(narrations) == len(vtypes) == len(payments)):
                raise ValueError("Mismatched input lengths in form data.")

            # Calculate the total amount
            total_amount = sum(float(payment) for payment in payments)

            with transaction.atomic():
                # Handle edit case
                if voucher_no:
                    Table_Voucher.objects.filter(Series=series, VoucherNo=voucher_no).delete()

                for accountcode, narration, vtype, payment in zip(accountcodes, narrations, vtypes, payments):
                    Table_Voucher.objects.create(
                        Series=series,
                        VoucherNo=voucher_no,
                        Vdate=vdate,
                        Accountcode=accountcode,
                        Headcode=headcode,
                        payment=payment,
                        VAmount=total_amount,  # Save the total amount
                        VType=vtype,
                        Narration=narration,
                        CStatus='P',
                        UserID=user_id,
                        FYCode=fy_code,
                        Coid=coid,
                        Branch_ID=branch_id
                    )

                    # Update Table_Acntchild with FYCode and Coid
                    account_child = Table_Acntchild.objects.get(account_code=accountcode)
                    account_child.fyc_code = fy_code
                    account_child.company_id = coid
                    account_child.branch_id = branch_id
                    account_child.save()

                # Update the serial number in VoucherConfiguration for the next use if not editing
                if not voucher_no:
                    voucher_config = VoucherConfiguration.objects.get(series=series, category='payment')
                    voucher_config.serial_no += 1
                    voucher_config.save()

            print("Payment saved successfully!")
            return redirect('success_url_name')  # Redirect to success page after saving
        except Exception as e:
            print("Error saving payment: ", e)

            vouchers = VoucherConfiguration.objects.filter(category='payment')
            accountmas = Table_Accountsmaster.objects.filter(category__in=['Cashbook', 'Bank'])
            head_accounts = Table_Accountsmaster.objects.exclude(category__in=['Cashbook', 'Bank'])
            table_acntchildren = Table_Acntchild.objects.select_related('account_master').filter(
                account_master__category__in=['Bank', 'Cashbook']
            )

            return render(request, self.template_name, {
                'error': str(e),
                'vouchers': vouchers,
                'accountmas': accountmas,
                'head_accounts': head_accounts,
                'table_acntchildren': table_acntchildren,
                'user_id': request.user.id,
                'voucher_entries': voucher_entries,
            })
        

class SearchReceiptView(View):
    template_name = 'web/accounts/receipt/receipt_modify.html'

    def get(self, request, *args, **kwargs):
        vouchers = VoucherConfiguration.objects.filter(category='receipt')
        return render(request, self.template_name, {'vouchers': vouchers})
    

class EditReceiptView(View):
    template_name = 'web/accounts/receipt/edit_receipt.html'

    def get(self, request, *args, **kwargs):
        series = request.GET.get('Series')
        voucher_no = request.GET.get('VoucherNo')

        vouchers = VoucherConfiguration.objects.filter(category='receipt')
        accountmas = Table_Accountsmaster.objects.filter(category__in=['Cashbook', 'Bank'])
        head_accounts = Table_Accountsmaster.objects.exclude(category__in=['Cashbook', 'Bank'])
        table_acntchildren = Table_Acntchild.objects.select_related('account_master').filter(
            account_master__category__in=['Bank', 'Cashbook']
        )

        # Fetch voucher entries for the given series and voucher number
        voucher_entries = Table_Voucher.objects.filter(Series=series, VoucherNo=voucher_no)

        if not voucher_entries:
            return redirect('core:search_receipt')  # Ensure this matches the name in urls.py

        return render(request, self.template_name, {
            'vouchers': vouchers,
            'accountmas': accountmas, 
            'head_accounts': head_accounts,
            'table_acntchildren': table_acntchildren,
            'voucher_entries': voucher_entries,
            'user_id': request.user.id,
        }) 

    def post(self, request, *args, **kwargs):
        voucher_entries = []  # Initialize voucher_entries to avoid reference issues
        try:
            series = request.POST.get('Series')
            vdate = request.POST.get('Vdate')
            headcode = request.POST.get('Headcode')
            user_id = request.user.id
            fy_code = '2024-2025'
            coid = 'C'
            branch_id = '1'

            accountcodes = request.POST.getlist('Accountcode[]')
            narrations = request.POST.getlist('Narration[]')
            vtypes = request.POST.getlist('VType[]')
            payments = request.POST.getlist('payment[]')
            voucher_no = request.POST.get('VoucherNo')

            # Ensure all lists are of the same length
            if not (len(accountcodes) == len(narrations) == len(vtypes) == len(payments)):
                raise ValueError("Mismatched input lengths in form data.")

            # Calculate the total amount
            total_amount = sum(float(payment) for payment in payments)

            with transaction.atomic():
                # Handle edit case
                if voucher_no:
                    Table_Voucher.objects.filter(Series=series, VoucherNo=voucher_no).delete()

                for accountcode, narration, vtype, payment in zip(accountcodes, narrations, vtypes, payments):
                    Table_Voucher.objects.create(
                        Series=series,
                        VoucherNo=voucher_no,
                        Vdate=vdate,
                        Accountcode=accountcode,
                        Headcode=headcode,
                        payment=payment,
                        VAmount=total_amount,  # Save the total amount
                        VType=vtype,
                        Narration=narration,
                        CStatus='R',
                        UserID=user_id,
                        FYCode=fy_code,
                        Coid=coid,
                        Branch_ID=branch_id
                    )

                    # Update Table_Acntchild with FYCode and Coid
                    account_child = Table_Acntchild.objects.get(account_code=accountcode)
                    account_child.fyc_code = fy_code
                    account_child.company_id = coid
                    account_child.branch_id = branch_id
                    account_child.save()

                # Update the serial number in VoucherConfiguration for the next use if not editing
                if not voucher_no:
                    voucher_config = VoucherConfiguration.objects.get(series=series, category='receipt')
                    voucher_config.serial_no += 1
                    voucher_config.save()

            print("Receipt saved successfully!")
            return redirect('success_url_name')  # Redirect to success page after saving
        except Exception as e:
            print("Error saving receipt: ", e)

            vouchers = VoucherConfiguration.objects.filter(category='receipt')
            accountmas = Table_Accountsmaster.objects.filter(category__in=['Cashbook', 'Bank'])
            head_accounts = Table_Accountsmaster.objects.exclude(category__in=['Cashbook', 'Bank'])
            table_acntchildren = Table_Acntchild.objects.select_related('account_master').filter(
                account_master__category__in=['Bank', 'Cashbook']
            )

            return render(request, self.template_name, {
                'error': str(e),
                'vouchers': vouchers,
                'accountmas': accountmas,
                'head_accounts': head_accounts,
                'table_acntchildren': table_acntchildren,
                'user_id': request.user.id,
                'voucher_entries': voucher_entries,
               })