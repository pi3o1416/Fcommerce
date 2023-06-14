
from django.db import models
from django.apps import apps
from django.contrib import auth
from dirtyfields import DirtyFieldsMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

from services.querysets import TemplateQuerySet
from .validators import UnicodeMerchantNameValidator


class MerchantManager(BaseUserManager):
    use_in_migrations = True

    def _create_merchant(self, name, merchant_id, password, **extra_fields):
        if not name:
            raise ValueError("The given merchant name must be set")
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        name = GlobalUserModel.normalize_username(name)
        merchant = self.model(name=name, merchant_id=merchant_id, password=password, **extra_fields)
        merchant.save()
        return merchant

    def create_user(self, name, merchant_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_merchant(name, merchant_id, password, **extra_fields)

    def create_superuser(self, name, merchant_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_merchant(name, merchant_id, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()

    def get_queryset(self):
        return MerchantQuerySet(model=self.model, using=self._db)

    def filter_from_query_params(self, request):
        return self.get_queryset().filter_from_query_params(request=request)

    def filter_with_related_fields(self, request, related_fields: list):
        return self.get_queryset().filter_with_related_fields(request=request, related_fields=related_fields)


class MerchantQuerySet(TemplateQuerySet):
    pass


class Merchant(DirtyFieldsMixin, AbstractBaseUser, PermissionsMixin):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=200,
        unique=True,
        validators=[UnicodeMerchantNameValidator()]
    )
    merchant_id = models.CharField(
        verbose_name=_('Merchant ID'),
        unique=True,
        max_length=200,
    )
    publish_shop = models.BooleanField(
        verbose_name=_('Publish Shop'),
        default=False
    )
    integrate_facebook = models.BooleanField(
        verbose_name=_('Integrate Facebook'),
        default=False
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created At'),
        auto_now_add=True,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    _password = None
    objects = MerchantManager()
    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = ['merchant_id']

    class Meta:
        verbose_name = _("merchant")
        verbose_name_plural = _("merchants")
        ordering = ['-created_at']
        swappable = "AUTH_USER_MODEL"
