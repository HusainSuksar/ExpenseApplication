from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import login_view, home, AccountCreateView, AccountListView, AccountListJson, AccountUpdateView, \
    RequestCreateView, RequestUpdateView, RequestListView, RequestListJson, UpdateEmployee, RequestStatus

app_name = 'accounts'

urlpatterns = [
    # login and logout Urls
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # home url
    path('', home, name='home'),
    # Manager Urls
    path('employees/add/', AccountCreateView.as_view(), name='account_add'),
    path('employees/update/<int:pk>/', AccountUpdateView.as_view(), name='account_update'),
    path('employees/', AccountListView.as_view(), name='account_list'),
    path('employees/data/', AccountListJson.as_view(), name='account_list_data'),
    path('requests/<int:pk>/', RequestStatus.as_view(), name='request_status'),

    # Employee Url
    path('requests/add/', RequestCreateView.as_view(), name='request_add'),
    path('requests/update/<int:pk>/', RequestUpdateView.as_view(), name='request_update'),
    path('requests/', RequestListView.as_view(), name='request_list'),
    path('requests/data/', RequestListJson.as_view(), name='request_list_data'),


    # To edit your account
    path('update-info/', UpdateEmployee.as_view(), name='update-info'),
]
