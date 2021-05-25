from django.contrib import admin
from safedelete import HARD_DELETE
from safedelete.admin import SafeDeleteAdmin


class UserRoleFilterQuerysetAdminMixin(admin.ModelAdmin):
    def get_queryset(self, request):
        user = request.user
        if user.is_staff and user.is_superuser:
            queryset = super(UserRoleFilterQuerysetAdminMixin, self).get_queryset(request)
            return queryset
        elif user.is_staff:
            queryset = super(UserRoleFilterQuerysetAdminMixin, self).get_queryset(request)
            filtered_queryset = queryset.filter(deleted=None)
            return filtered_queryset
        else:
            return None

class UserRoleActionPermissionMixin(admin.ModelAdmin):
    actions = [
        'delete_permanently'
    ] + list(SafeDeleteAdmin.actions)

    def delete_permanently(self, request, queryset):
        for query in queryset:
            query.delete(force_policy=HARD_DELETE)
        self.message_user(request, '{} objects deleted permanently.'.format(queryset.count()))
    delete_permanently.short_description = 'Delete permanently'

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_permanently']
        return actions
