from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

UserAdmin.fieldsets[2][1]['fields'] = (
                                        'phonenumber',
                                        'cardnumber',
                                        'idnumber',
                                        'is_active', 
                                        'is_staff', 
                                        'is_superuser', 
                                        'is_author',
                                        'is_supervisor',  
                                        'groups',
                                        'user_permissions',
                                    )
UserAdmin.list_display += ('is_author','is_supervisor','phonenumber','cardnumber','idnumber')

admin.site.register(User, UserAdmin)