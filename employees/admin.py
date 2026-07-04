from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # Customize the columns shown in the list page
    list_display = ('get_employee_id', 'name', 'email', 'phone', 'department', 'designation', 'status')
    
    # Filter options in the sidebar
    list_filter = ('department', 'status')
    
    # Search fields
    search_fields = ('name', 'email', 'department', 'designation')
    
    # Ordering
    ordering = ('-created_at',)

    # Display read-only custom employee_id
    def get_employee_id(self, obj):
        return obj.employee_id
    get_employee_id.short_description = 'Employee ID'
