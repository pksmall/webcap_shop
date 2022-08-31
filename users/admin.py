from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import User


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
  form = MyUserChangeForm

  ordering = ('email',)

  list_display = ('email', 'role', 'is_active')
  list_filter = ('role', 'is_active')
  readonly_fields = ('date_joined', )

  fieldsets = (
      (None, {'fields':
                (
                  'email', 'password', 'role', 'first_name', 'last_name', 'is_active', 'is_deleted',
                  'date_joined', 'created_date', 'modified_date', 'created_by', 'modified_by'
                 )
              }
       ),
  )


admin.site.register(User, MyUserAdmin)
