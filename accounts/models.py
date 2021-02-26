from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


def manager_validate(value):
    manager = User.objects.filter(pk=value)
    if manager:
        manager = manager.first()
        if manager.type != manager.MANAGER:
            raise ValidationError(
                _('%(value)s is not a manager'),
                params={'value': value},
            )


class Country(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    logo = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    def __str__(self):
        return self.logo + ' ' + self.name_en + ' ' + self.name_ar


class User(AbstractUser):
    EMPLOYEE = MALE = 0
    MANAGER = FEMALE = 1
    TYPE = [(EMPLOYEE, _('Employee')),
            (MANAGER, _('Manager')), ]
    GENDER = [
        (MALE, _('Male')),
        (FEMALE, _('Female'))
    ]
    birth_date = models.DateField(verbose_name=_('Birth Date'), blank=True, null=True)
    image = models.ImageField(upload_to='profile/', blank=True, null=True)
    address = models.CharField(max_length=500, verbose_name=_('Address'), blank=True, null=True)

    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name=_('users'),
                                verbose_name=_('Country'), blank=True, null=True)
    phone = models.CharField(max_length=15, verbose_name=_('Phone'),blank=True, null=True )
    type = models.SmallIntegerField(choices=TYPE, default=0)
    gender = models.SmallIntegerField(choices=GENDER,blank=True, null=True)
    # to log with email
    # email overwrite to be unique
    # removed from required fields list
    email = models.EmailField(_('email address'), unique=True)
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    manager = models.ForeignKey('self', on_delete=models.CASCADE, related_name='employees', blank=True, null=True,
                                validators=[manager_validate])

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class LeaveRequest(models.Model):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2
    STATUS = [
        (PENDING, _('Pending')),
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected'))
    ]
    reason = models.TextField(max_length=1000, verbose_name=_('Reason'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manager_requests', blank=True, null=True,
                                validators=[manager_validate])
    status = models.SmallIntegerField(choices=STATUS, verbose_name=_('Reason'), default=PENDING)
    created_at = models.DateField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
