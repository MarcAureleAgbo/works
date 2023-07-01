from django.db import models


class approvals(models.Model):
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

    firstname = models.CharField(max_length=15)
    lastname = models.CharField(max_length=15)

    person_age = models.IntegerField(default=0)
    person_income = models.IntegerField(default=0)
    person_home_ownership = models.CharField(max_length=15, choices=PERSON_HOME_OWNERSHIP_CHOICES)
    person_emp_length = models.IntegerField(default=0)
    loan_intent = models.CharField(max_length=25, choices=LOAN_INTENT_CHOICES)
    loan_grade = models.CharField(max_length=15, choices=LOAN_GRADE_CHOICES)
    loan_amnt = models.IntegerField(default=0)
    loan_int_rate = models.FloatField(default=0.0)
    loan_percent_income = models.FloatField(default=0.0)
    cb_person_default_on_file = models.CharField(max_length=15, choices=CB_PERSON_DEFAULT_ON_FILE_CHOICES)
    cb_person_cred_hist_length = models.IntegerField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

# {
#  'person_age': 28,
#  'person_income': 52000,
#  'person_home_ownership': 0,
#  'person_emp_length': 11.0,
#  'loan_intent': 3,
#  'loan_grade': 0,
#  'loan_amnt': 6000,
#  'loan_int_rate': 10.59,
#!  'loan_percent_income': 0.12,
#  'cb_person_default_on_file': 5
# }
