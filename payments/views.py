from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .forms import CreateInvoiceForm
from .ymoney import get_operation_url, is_operation_success
import uuid
from .tasks import check_payment_task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class CreateInvoiceView(LoginRequiredMixin, CreateView):
    form_class = CreateInvoiceForm
    template_name = 'insta_app/payment.html'

    def form_valid(self, form):
        label = uuid.uuid4()
        form.instance.user = self.request.user.paymentaccount
        form.instance.invoice_label = str(label)
        self.success_url = get_operation_url(form.instance.amount, str(label))
        check_payment_task.delay(label)
        return super().form_valid(form)



