from statistics import mode
from django import forms
from .models import approvals

#class ApprovalForm(forms.Form):
class ApprovalForm(forms.ModelForm):
    class Meta:
        model = approvals
        fields = "__all__"
    
    PERSON_HOME_OWNERSHIP_CHOICES = (
        ('RENT', 'RENT'),
        ('OWN', 'OWN'),
        ('MORTGAGE', 'MORTGAGE'),
        ('OTHER', 'OTHER')
    )
    LOAN_INTENT_CHOICES = (
        ('PERSONAL', 'PERSONAL'),
        ('EDUCATION', 'EDUCATION'),
        ('MEDICAL', 'MEDICAL'),
        ('VENTURE', 'VENTURE'),
        ('HOMEIMPROVEMENT', 'HOME IMPROVEMENT'),
        ('DEBTCONSOLIDATION', 'DEBT CONSOLIDATION')
    )

    LOAN_GRADE_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
    )

    CB_PERSON_DEFAULT_ON_FILE_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No')
    )

    firstname = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Entre Firstname'}))
    lastname = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Entre Lastname'}))
    person_age = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Age'}))
    person_income = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Enter Person Income'}))
    person_home_ownership = forms.ChoiceField(choices=PERSON_HOME_OWNERSHIP_CHOICES)
    person_emp_length = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Enter Person Emp Length'}))
    loan_intent = forms.ChoiceField(choices=LOAN_INTENT_CHOICES)
    loan_grade = forms.ChoiceField(choices=LOAN_GRADE_CHOICES)
    loan_amnt = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Loan Amount'}))
    loan_int_rate = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Loan Interest Rate'}))
    loan_percent_income = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Loan Percent Income'}))
    cb_person_default_on_file = forms.ChoiceField(choices=CB_PERSON_DEFAULT_ON_FILE_CHOICES)
    cb_person_cred_hist_length = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter CB Person Credit Hist Length'}))
