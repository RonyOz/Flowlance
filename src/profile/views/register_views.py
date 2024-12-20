from django.shortcuts import render, redirect
from django.contrib.auth import login
from ..forms import FreelancerRegisterForm, CompanyRegisterForm
from django.db import IntegrityError



def register_freelancer(request):
    registration_successful = False  
    if request.method == 'POST':
        form = FreelancerRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            registration_successful = True  
            return render(request, 'profile/register_freelancer.html', {'form': FreelancerRegisterForm(), 'registration_successful': registration_successful})

    else:
        form = FreelancerRegisterForm()
    return render(request, 'profile/register_freelancer.html', {'form': form, 'registration_successful': registration_successful})



def register_company(request):
    registration_successful = False
    if request.method == 'POST':
        form = CompanyRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                registration_successful = True
                return render(request, 'profile/register_company.html', {
                    'form': CompanyRegisterForm(),
                    'registration_successful': registration_successful
                })
            except IntegrityError:
                form.add_error(None, 'Error al crear el usuario, por favor intenta de nuevo.')
    else:
        form = CompanyRegisterForm()
    
    return render(request, 'profile/register_company.html', {
        'form': form,
        'registration_successful': registration_successful
    })
