from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Employee
from .forms import EmployeeForm

@login_required
def dashboard(request):
    """Dashboard view displaying system-wide metrics and recent employees."""
    total_employees = Employee.objects.count()
    # Count distinct departments that have employees
    total_departments = Employee.objects.exclude(department='').values('department').distinct().count()
    recent_employees = Employee.objects.order_by('-created_at')[:5]
    
    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'recent_employees': recent_employees,
    }
    return render(request, 'employees/dashboard.html', context)

@login_required
def employee_list(request):
    """Displays a list of employees with search and pagination features."""
    query = request.GET.get('search', '')
    department_filter = request.GET.get('department', '')
    status_filter = request.GET.get('status', '')
    
    employees = Employee.objects.all()
    
    # Apply search query across Name, Email, Department, and Designation
    if query:
        employees = employees.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(department__icontains=query) |
            Q(designation__icontains=query)
        )
        
    # Apply filters if selected
    if department_filter:
        employees = employees.filter(department=department_filter)
    if status_filter:
        employees = employees.filter(status=status_filter)
        
    # Pagination: 5 employees per page for demonstration/clean layout
    paginator = Paginator(employees, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get distinct departments for filter dropdown
    departments = Employee.DEPARTMENT_CHOICES
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'selected_department': department_filter,
        'selected_status': status_filter,
        'departments': departments,
    }
    return render(request, 'employees/list.html', context)

@login_required
def employee_detail(request, pk):
    """Displays detailed information for a single employee."""
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/detail.html', {'employee': employee})

@login_required
def employee_add(request):
    """View to add a new employee."""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f"Employee '{employee.name}' has been added successfully.")
            return redirect('employee_list')
        else:
            messages.error(request, "Failed to add employee. Please correct the errors below.")
    else:
        form = EmployeeForm()
        
    return render(request, 'employees/form.html', {'form': form, 'action': 'Add'})

@login_required
def employee_edit(request, pk):
    """View to edit an existing employee."""
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f"Employee '{employee.name}' has been updated successfully.")
            return redirect('employee_detail', pk=employee.pk)
        else:
            messages.error(request, "Failed to update employee. Please correct the errors below.")
    else:
        form = EmployeeForm(instance=employee)
        
    return render(request, 'employees/form.html', {'form': form, 'action': 'Edit', 'employee': employee})

@login_required
def employee_delete(request, pk):
    """Deletes an employee. Handles both POST from modal and fallback confirmation page."""
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        name = employee.name
        employee.delete()
        messages.success(request, f"Employee '{name}' was deleted successfully.")
        return redirect('employee_list')
    return render(request, 'employees/confirm_delete.html', {'employee': employee})
