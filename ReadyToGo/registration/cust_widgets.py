import django.forms.widgets as wdts


class CustDateInput(wdts.DateInput):
    template_name = 'cust_widgets/date.html'


class CustSelect(wdts.Select):
    template_name = 'cust_widgets/select.html'
    