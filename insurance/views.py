from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import User
from customer import models as CMODEL
from customer import forms as CFORM
from datetime import datetime
from django.contrib import messages
from insurance.models import Contact

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'insurance/index.html')


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

@login_required(login_url='login')
def afterlogin_view(request):
    if is_customer(request.user):
        messages.success(request,'Logged in successfully !!')    
        return redirect('customer/customer-dashboard')
    else:
        messages.success(request,'Logged in successfully !!') 
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('login')


@login_required(login_url='login')
def admin_dashboard_view(request):
    dict={
        'total_user':CMODEL.Customer.objects.all().count(),
        'total_policy':models.Policy.objects.all().count(),
        'total_category':models.Category.objects.all().count(),
        'total_question':models.Question.objects.all().count(),
        'total_policy_holder':models.PolicyRecord.objects.all().count(),
        'approved_policy_holder':models.PolicyRecord.objects.all().filter(status='Approved').count(),
        'disapproved_policy_holder':models.PolicyRecord.objects.all().filter(status='Disapproved').count(),
        'waiting_policy_holder':models.PolicyRecord.objects.all().filter(status='Pending').count(),
    }
    return render(request,'insurance/admin_dashboard.html',context=dict)



@login_required(login_url='login')
def admin_view_customer_view(request):
    customers= CMODEL.Customer.objects.all()
    return render(request,'insurance/admin_view_customer.html',{'customers':customers})



@login_required(login_url='login')
def update_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=CMODEL.User.objects.get(id=customer.user_id)
    userForm=CFORM.CustomerUserForm(instance=user)
    customerForm=CFORM.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=CFORM.CustomerUserForm(request.POST,instance=user)
        customerForm=CFORM.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'insurance/update_customer.html',context=mydict)



@login_required(login_url='login')
def delete_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return HttpResponseRedirect('/admin-view-customer')


@login_required(login_url='login')
def admin_category_view(request):
    return render(request,'insurance/admin_category.html')
@login_required(login_url='login')
def admin_add_category_view(request):
    categoryForm=forms.CategoryForm() 
    if request.method=='POST':
        categoryForm=forms.CategoryForm(request.POST)
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('admin-view-category')
    return render(request,'insurance/admin_add_category.html',{'categoryForm':categoryForm})
@login_required(login_url='login')
def admin_view_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'insurance/admin_view_category.html',{'categories':categories})
@login_required(login_url='login')
def admin_delete_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'insurance/admin_delete_category.html',{'categories':categories})
@login_required(login_url='login')   
def delete_category_view(request,pk):
    category = models.Category.objects.get(id=pk)
    category.delete()
    return redirect('admin-delete-category')
@login_required(login_url='login')
def admin_update_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'insurance/admin_update_category.html',{'categories':categories})

@login_required(login_url='login')
def update_category_view(request,pk):
    category = models.Category.objects.get(id=pk)
    categoryForm=forms.CategoryForm(instance=category)
    
    if request.method=='POST':
        categoryForm=forms.CategoryForm(request.POST,instance=category)
        
        if categoryForm.is_valid():

            categoryForm.save()
            return redirect('admin-update-category')
    return render(request,'insurance/update_category.html',{'categoryForm':categoryForm})
  

@login_required(login_url='login')
def admin_policy_view(request):
    return render(request,'insurance/admin_policy.html')

@login_required(login_url='login')
def admin_add_policy_view(request):
    policyForm=forms.PolicyForm() 
    
    if request.method=='POST':
        policyForm=forms.PolicyForm(request.POST)
        if policyForm.is_valid():
            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)
            
            policy = policyForm.save(commit=False)
            policy.category=category
            policy.save()
            return redirect('admin-view-policy')
    return render(request,'insurance/admin_add_policy.html',{'policyForm':policyForm})
@login_required(login_url='login')
def admin_view_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,'insurance/admin_view_policy.html',{'policies':policies})


@login_required(login_url='login')
def admin_update_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,'insurance/admin_update_policy.html',{'policies':policies})

@login_required(login_url='login')
def update_policy_view(request,pk):
    policy = models.Policy.objects.get(id=pk)
    policyForm=forms.PolicyForm(instance=policy)
    
    if request.method=='POST':
        policyForm=forms.PolicyForm(request.POST,instance=policy)
        
        if policyForm.is_valid():

            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)
            
            policy = policyForm.save(commit=False)
            policy.category=category
            policy.save()
           
            return redirect('admin-update-policy')
    return render(request,'insurance/update_policy.html',{'policyForm':policyForm})
  
@login_required(login_url='login') 
def admin_delete_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,'insurance/admin_delete_policy.html',{'policies':policies})
@login_required(login_url='login')   
def delete_policy_view(request,pk):
    policy = models.Policy.objects.get(id=pk)
    policy.delete()
    return redirect('admin-delete-policy')
@login_required(login_url='login')
def admin_view_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all()
    return render(request,'insurance/admin_view_policy_holder.html',{'policyrecords':policyrecords})
@login_required(login_url='login')
def admin_view_approved_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='Approved')
    return render(request,'insurance/admin_view_approved_policy_holder.html',{'policyrecords':policyrecords})
@login_required(login_url='login')
def admin_view_disapproved_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='Disapproved')
    return render(request,'insurance/admin_view_disapproved_policy_holder.html',{'policyrecords':policyrecords})
@login_required(login_url='login')
def admin_view_waiting_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='Pending')
    return render(request,'insurance/admin_view_waiting_policy_holder.html',{'policyrecords':policyrecords})
@login_required(login_url='login')
def approve_request_view(request,pk):
    policyrecords = models.PolicyRecord.objects.get(id=pk)
    policyrecords.status='Approved'
    policyrecords.save()
    return redirect('admin-view-policy-holder')
@login_required(login_url='login')
def disapprove_request_view(request,pk):
    policyrecords = models.PolicyRecord.objects.get(id=pk)
    policyrecords.status='Disapproved'
    policyrecords.save()
    return redirect('admin-view-policy-holder')

@login_required(login_url='login')
def admin_question_view(request):
    questions = models.Question.objects.all()
    return render(request,'insurance/admin_question.html',{'questions':questions})
@login_required(login_url='login')
def update_question_view(request,pk):
    question = models.Question.objects.get(id=pk)
    questionForm=forms.QuestionForm(instance=question)
    
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST,instance=question)
        
        if questionForm.is_valid():

            admin_comment = request.POST.get('admin_comment')
            
            
            question = questionForm.save(commit=False)
            question.admin_comment=admin_comment
            question.save()
           
            return redirect('admin-question')
    return render(request,'insurance/update_question.html',{'questionForm':questionForm})


def aboutus_view(request):
    return render(request,'insurance/aboutus.html')

def contactus_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date = datetime.today())
        contact.save()
        # messages.success(request,'Your message has been sent!')
        return render(request,'insurance/contactussuccess.html')
    return render(request,'insurance/contact.html')  

def delete_contact_list(request,pk):
    question=Contact.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/contact_list')

def contact_list(request):
    x=Contact.objects.all()
    context={'x':x}
    
    return render(request,'insurance/contact_list.html',context)
