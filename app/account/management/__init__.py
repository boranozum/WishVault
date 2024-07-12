# from django.db.models import signals
#
# from account.permissions import create_admin_user
#
# # Disable django default permission creation
# signals.post_migrate.disconnect(dispatch_uid="django.contrib.auth.management.create_permissions")
#
#
# # Create Global Permissions
# signals.post_migrate.connect(create_admin_user, dispatch_uid="common.permissions.create_permission")