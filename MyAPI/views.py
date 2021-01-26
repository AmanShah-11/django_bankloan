from django.shortcuts import render
from .forms import ApprovalsForm
# from . forms import MyForm
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.contrib import messages
from .models import approvals
from .serializers import approvalsSerializers
import pickle
# from sklearn.externals import joblib
import joblib
import json
import numpy as np
from sklearn import preprocessing
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Create your views here.


class ApprovalsView(viewsets.ModelViewSet):
    # gets all the objects from the request
    queryset = approvals.objects.all()
    serializer_class = approvalsSerializers

def ohevalue(df):
    ohe_col = joblib.load('C:\\Users\\Aman\\Documents\\pickle file\\allcol.pkl')
    cat_columns = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area']
    df_processed = pd.get_dummies(df, columns=cat_columns)
    newdict = {}
    for i in ohe_col:
        if i in df_processed.columns:
            newdict[i] = df_processed[i].values
        else:
            newdict[i] = 0
    newdf = pd.DataFrame(newdict)
    return newdf


# Handles all of the post requests by itself from the decorators
# @api_view
def approvereject(unit):
    try:
        mdl = joblib.load('C:\\Users\\Aman\\Documents\\pickle file\\loan_model.pkl')
        # The data comes in a dictionary so it must be converted

        # mydata = unit.data
        # unit = np.array(list(mydata.values()))
        # unit = unit.rephase(1,-1)
        # this line below might be wrong
        scalers = joblib.load("C:\\Users\\Aman\\Documents\\pickle file\\scalers.pkl")
        X = scalers.transform(unit)
        # parameter should be X but it's not working because i don't have the correct scalers.pkl file
        print("Starting to predict")
        print(unit)
        print("----------------------")
        # Something is wrong with the model
        y_pred = mdl.predict(X)
        print("Predicting")
        y_pred = (y_pred > 0.58)
        print("scaling")
        newdf = pd.DataFrame(y_pred, columns=['Status'])
        print("Selecting column")
        newdf = newdf.replace({True:"Approved", False:"Rejected"})
        print("Using dictionary")
        return (newdf.values[0][0],X[0])
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

def cxcontact(request):
    if (request.method == "POST"):
        form = ApprovalsForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            Dependents = form.cleaned_data['Dependents']
            ApplicantIncome = form.cleaned_data['ApplicantIncome']
            CoapplicantIncome = form.cleaned_data['CoapplicantIncome']
            LoanAmount = form.cleaned_data['LoanAmount']
            Loan_Amount_Term = form.cleaned_data['Loan_Amount_Term']
            Credit_History = form.cleaned_data['Credit_History']
            Gender = form.cleaned_data['Gender']
            Married = form.cleaned_data['Married']
            Education = form.cleaned_data['Education']
            Self_Employed = form.cleaned_data['Self_Employed']
            Property_Area = form.cleaned_data['Property_Area']
            # one hot encodes the entire thing since our machine learning model is one hot encoded
            myDict = (request.POST).dict()
            df = pd.DataFrame(myDict, index=[0])
            answer = approvereject(ohevalue(df))[0]
            Xscalers = approvereject(ohevalue(df))[1]
            if int(df['LoanAmount']) < 25000:
                messages.success(request, 'Application Status: {}'.format(answer))
            else:
                messages.success(request, 'Invalid: Your Loan Request Exceeds $25,000 Limit')

    form = ApprovalsForm()

    return render(request, "myform/cxform.html", {'form':form})
