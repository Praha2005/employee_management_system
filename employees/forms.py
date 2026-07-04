from django import forms
from .models import Employee
import re

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'phone', 'department', 'designation', 'salary', 'joining_date', 'status']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Skip joining_date as it's already set in widgets
            if field_name == 'joining_date':
                continue
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None and salary <= 0:
            raise forms.ValidationError("Salary must be a positive number.")
        return salary

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Simple phone regex to allow numbers, optional + prefix, and spaces/dashes
        if phone:
            pattern = r'^\+?1?[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{4}$|^\+?\d{7,15}$'
            # Let's check format; if it contains letters, raise validation error
            if re.search(r'[a-zA-Z]', phone):
                raise forms.ValidationError("Phone number must only contain digits, spaces, dashes, or a '+' prefix.")
        return phone
