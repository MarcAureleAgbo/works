from .forms import ApprovalForm 
from rest_framework import viewsets 
from rest_framework.decorators import api_view 
from django.core import serializers 
from rest_framework.response import Response 
from rest_framework import status 
from django.http import JsonResponse 
from rest_framework.parsers import JSONParser 
from .models import approvals 
from .serializer import ApprovalsSerializers 

import pickle, joblib
import json 
import numpy as np 
from sklearn import preprocessing 
import pandas as pd 
from django.shortcuts import render, redirect 
from django.contrib import messages 

class ApprovalsView(viewsets.ModelViewSet): 
    queryset = approvals.objects.all() 
    serializer_class = ApprovalsSerializers  

def approvereject(request):
    try:
        path_to_artifacts = "/home/maa/Documents/GitHub/works/rcAPI/pickle/"
        features_columns =  joblib.load(path_to_artifacts+"features_columns.pickle")
        encoders = joblib.load(path_to_artifacts+"encoder_cat_col.pickle")
        model = joblib.load(path_to_artifacts+"model.pickle")
        mediane_loan_int_rate_ones = joblib.load(path_to_artifacts+
            "mediane_loan_int_rate_ones.pickle"
            )
        mediane_loan_int_rate_zeros = joblib.load(path_to_artifacts+
            "mediane_loan_int_rate_zeros.pickle"
            )

        mydata = request.dict()
        # JSON to pandas DataFrame
        input_data = pd.DataFrame(mydata, index=[0])
        input_data.to_csv('./input_data_before_preprocess.csv')
        # ?* fill missing values
        input_data.loc[
            (input_data.loan_int_rate.isnull()), # & (input_data.loan_status == 0),
            'loan_int_rate'
            ] = (mediane_loan_int_rate_zeros + mediane_loan_int_rate_ones) / 2

        categorical_columns = [
            'cb_person_default_on_file', 'loan_grade', 'loan_intent', 'person_home_ownership'
            ]
        input_data[categorical_columns] = input_data[categorical_columns].apply(encoders.fit_transform)

        input_data.to_csv('./input_data_after_preprocess.csv')

        input_data = input_data[features_columns]
        y_pred = model.predict(input_data)[0]
        # newdf = 'Rejected' if y_pred else 'Approved'
        newdf = pd.DataFrame(np.array([y_pred]), columns=['Status'])
        newdf = newdf.replace({0: 'Approved', 1: 'Rejected'})
        return newdf['Status'][0]
        # return JsonResponse('Your Status is {}'.format(newdf['Status'][0]), safe=False)
    except ValueError as err:
        print(err)
        return Response(err.args[0], status.HTTP_400_BAD_REQUEST)


def FormView(request):
    if request.method=='POST':
        form = ApprovalForm(request.POST)
        if form.is_valid():
            form.save()
            #ApprovalForm = form.save()
            
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            person_age = form.cleaned_data['person_age']
            person_home_ownership = form.cleaned_data['person_home_ownership']
            person_emp_length = form.cleaned_data['person_emp_length']
            loan_intent = form.cleaned_data['loan_intent']
            loan_grade = form.cleaned_data['loan_grade']
            loan_amnt = form.cleaned_data['loan_amnt']
            loan_int_rate = form.cleaned_data['loan_int_rate']
            loan_percent_income = form.cleaned_data['loan_percent_income']
            cb_person_default_on_file = form.cleaned_data['cb_person_default_on_file']
            cb_person_cred_hist_length = form.cleaned_data['cb_person_cred_hist_length']
            mydict = (request.POST)
            # df = pd.DataFrame(mydict, index=[0])
            answer = approvereject(mydict)
            if loan_amnt < 25000:
                messages.success(request, f'Application Status: {answer}')
            else:
                messages.success(request, 'Invalid: Your Loan Request Exceeds the Limit of 25000')
                    
            return render(request, 'status.html', {"data": answer})             
    form=ApprovalForm()
    return render(request, 'form.html', {'form':form})