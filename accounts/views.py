from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django_datatables_view.base_datatable_view import BaseDatatableView

from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView

from accounts.forms import CustomUserAdminCreationForm, UserAdminChangeForm, UserChangeForm
from accounts.models import User, Country, LeaveRequest


def is_manager(user):
    if user.type == user.MANAGER:
        return True
    else:
        return False


def is_employee(user):
    if user.type == user.EMPLOYEE:
        return True
    else:
        return False


# delete function used in list Views for multiple deletion
def multi_delete(request, model):
    ids = request.POST.get('deleteIds', None)
    if ids:
        ids = ids.split(',')
        mod = model.objects.filter(pk__in=ids)
        if mod:
            for m in mod:
                m.delete()


def login_view(request):
    form = AuthenticationForm()
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            user = get_user_model().objects.filter(username=username).first()
            if user is not None:
                user = authenticate(username=user.email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.GET:
                    if request.GET.get('next', None):
                        return redirect(request.GET.get('next'))
                else:
                    return redirect('accounts:home')
        else:
            form = AuthenticationForm(data=request.POST)
    if request.user.is_authenticated:
        return redirect('accounts:home')
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def home(request):
    return render(request, 'index.html')


# Manager View
@method_decorator(user_passes_test(is_manager), name='dispatch')
class AccountCreateView(LoginRequiredMixin, CreateView):
    model = User
    template_name = 'account_manage/form.html'
    form_class = CustomUserAdminCreationForm

    # to edit form fields that class generate
    def get_form(self, form_class=None):
        form = super(AccountCreateView, self).get_form()
        form.fields['country'] = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label='Choice Country')
        form.fields['gender'] = forms.ChoiceField(choices=User.GENDER)
        return form

    def post(self, request, *args, **kwargs):
        temp = super(AccountCreateView, self).post(request, *args, **kwargs)
        if self.object is None:
            return temp
        user = self.object
        if user.type == 0:
            user.manager = request.user
            user.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        if self.request.POST.get('another', None):
            return reverse_lazy('accounts:account_add')
        return reverse_lazy('accounts:account_list')


@method_decorator(user_passes_test(is_manager), name='dispatch')
class AccountListView(LoginRequiredMixin, TemplateView):
    template_name = 'account_manage/list.html'

    # for post request in delete
    def post(self, request):
        multi_delete(request, User)
        return redirect('accounts:account_list')


@method_decorator(user_passes_test(is_manager), name='dispatch')
class AccountListJson(LoginRequiredMixin, BaseDatatableView):
    columns = ['id', 'username', 'email', 'full_name', 'birth_date', 'is_active', 'image']
    order_columns = ['id', 'username', 'email', 'full_name', 'birth_date', 'is_active', 'image']
    max_display_length = 30
    model = User

    def render_column(self, row, column):
        if column == 'image':
            if row.image:
                return str(row.image.url)
        elif column == 'full_name':
            return str(row.get_full_name())
        else:
            return super().render_column(row, column)

    def get_initial_queryset(self):
        return User.objects.filter(type=User.EMPLOYEE)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        is_active = self.request.GET.get('columns[6][search][value]', None)
        if not is_active:
            is_active = self.request.GET.get('columns[5][search][value]', None)
        if search:
            qs = qs.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(birth_date__icontains=search)
            )
        if is_active:
            qs = qs.filter(is_active=is_active)
        return qs


@method_decorator(user_passes_test(is_manager), name='dispatch')
class AccountUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserAdminChangeForm
    model = User
    template_name = 'account_manage/form.html'
    context_object_name = 'account'

    def get_object(self, queryset=None):
        obj = super(AccountUpdateView, self).get_object(queryset=None)
        if obj.type == 0:
            return obj
        else:
            raise Http404("No User With This Id")

    def get_success_url(self):
        return reverse_lazy('accounts:account_list')


@method_decorator(user_passes_test(is_manager), name='dispatch')
class RequestStatus(LoginRequiredMixin, DetailView):
    model = LeaveRequest
    template_name = 'leave_requests/detail.html'
    context_object_name = 'leave_request'

    def get_object(self, queryset=None):
        obj = super(RequestStatus, self).get_object(queryset)
        if obj.user.manager == self.request.user:
            return obj
        else:
            raise Http404("No Request With This Id")

    def post(self, request, pk):
        obj = self.get_object()
        status = request.POST.get('status', None)
        if status:
            obj.status = status
            obj.save()
            return redirect('accounts:request_status', pk=obj.pk)
        else:
            raise Http404("No Request With This Id")

    def get_success_url(self):
        return reverse_lazy('accounts:request_list')


# Employee View
@method_decorator(user_passes_test(is_employee), name='dispatch')
class RequestCreateView(LoginRequiredMixin, CreateView):
    model = LeaveRequest
    template_name = 'leave_requests/form.html'
    fields = ['reason']

    def post(self, request, *args, **kwargs):
        reason = request.POST.get('reason', None)
        if reason:
            self.object = LeaveRequest(reason=reason, user=request.user)
            self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('accounts:request_update', kwargs={'pk': self.object.pk})


@method_decorator(user_passes_test(is_employee), name='dispatch')
class RequestUpdateView(LoginRequiredMixin, UpdateView):
    model = LeaveRequest
    template_name = 'leave_requests/form.html'
    fields = ['reason']

    def get_object(self, queryset=None):
        obj = super(RequestUpdateView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("Request does not exist")
        else:
            return obj

    def post(self, request, *args, **kwargs):
        reason = request.POST.get('reason', None)
        if reason:
            self.object = self.get_object()
            self.object.reason = reason
            self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('accounts:request_update', kwargs={'pk': self.object.pk})


# for both manager and employee
class RequestListView(LoginRequiredMixin, TemplateView):
    template_name = 'leave_requests/list.html'

    # for post request in delete
    def post(self, request):
        multi_delete(request, LeaveRequest)
        return redirect('accounts:request_list')


class RequestListJson(LoginRequiredMixin, BaseDatatableView):
    columns = ['id', 'user', 'reason', 'status', 'created_at', 'modified_date']
    order_columns = ['id', 'user', 'reason', 'status', 'created_at', 'modified_date']
    max_display_length = 30
    model = LeaveRequest

    def get_initial_queryset(self):
        if self.request.user.type == self.request.user.EMPLOYEE:
            return LeaveRequest.objects.filter(user=self.request.user)
        else:
            return LeaveRequest.objects.filter(user__manager=self.request.user)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        status = self.request.GET.get('columns[4][search][value]', None)
        if search:
            qs = qs.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(created_at__icontains=search) |
                Q(modified_date__icontains=search)
            )
        if status:
            qs = qs.filter(status=status)
        return qs


class UpdateEmployee(LoginRequiredMixin, UpdateView):
    form_class = UserChangeForm
    model = User
    template_name = 'account_manage/form.html'
    context_object_name = 'account'

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse_lazy('accounts:update-info')
