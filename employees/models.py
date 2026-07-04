from django.db import models

class Employee(models.Model):
    DEPARTMENT_CHOICES = [
        ('HR', 'Human Resources'),
        ('IT', 'Information Technology'),
        ('Finance', 'Finance'),
        ('Marketing', 'Marketing'),
        ('Operations', 'Operations'),
        ('Sales', 'Sales'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=150, help_text="Enter employee's full name.")
    email = models.EmailField(unique=True, help_text="Enter employee's email address.")
    phone = models.CharField(max_length=20, help_text="Enter employee's contact number.")
    department = models.CharField(
        max_length=50, 
        choices=DEPARTMENT_CHOICES, 
        default='IT',
        help_text="Select employee's department."
    )
    designation = models.CharField(max_length=100, help_text="Enter job title / designation.")
    salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Enter employee's monthly salary."
    )
    joining_date = models.DateField(help_text="Select date of joining.")
    status = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES, 
        default='Active',
        help_text="Current employment status."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def employee_id(self):
        """Returns the auto-generated ID formatted as EMP-XXXX"""
        if self.id:
            return f"EMP-{self.id:04d}"
        return "EMP-NEW"
