from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import StepRecord
from datetime import date, timedelta
import json

# Register View
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'trackapp/register.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('steps')
    return render(request, 'trackapp/register.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('steps')
        else:
            return render(request, 'trackapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'trackapp/login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Steps View
@login_required
def steps_view(request):
    today = date.today()
    if request.method == 'POST':
        steps = int(request.POST['steps'])
        StepRecord.objects.update_or_create(
            user=request.user,
            date=today,
            defaults={'steps': steps}
        )

    start = today - timedelta(days=6)
    records = StepRecord.objects.filter(user=request.user, date__gte=start).order_by('date')

    # Fill missing days with 0
    full_records = []
    for i in range(7):
        d = start + timedelta(days=i)
        r = records.filter(date=d).first()
        full_records.append({'date': d, 'steps': r.steps if r else 0})

    # Prepare JSON for Chart.js
    labels_json = json.dumps([str(r['date']) for r in full_records])
    data_json = json.dumps([r['steps'] for r in full_records])

    return render(request, 'trackapp/steps.html', {
        'records': full_records,
        'labels_json': labels_json,
        'data_json': data_json,
        
    })
