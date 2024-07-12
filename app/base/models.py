from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('account.User', on_delete=models.PROTECT, related_name='%(class)s_created_by')
    updated_by = models.ForeignKey('account.User', on_delete=models.PROTECT, related_name='%(class)s_updated_by', null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, force=False):
        if force:
            super().delete(using=using, keep_parents=keep_parents)
        else:
            self.is_deleted = True
            self.is_active = False
            self.deleted_at = timezone.now()
            self.save(update_fields=['is_deleted', 'deleted_at', 'is_active'])
