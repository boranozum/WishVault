from django.db.models import signals

from account.models import create_permissions

# Disable django default permission creation
signals.post_migrate.disconnect(dispatch_uid="django.contrib.auth.management.create_permissions")

# Create custom permissions
signals.post_migrate.connect(create_permissions, dispatch_uid="account.permissions.create_permission")