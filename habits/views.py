from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Habit
from .forms import HabitForm
from .models import Habit, HabitLog
from django.utils import timezone

@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user)
    total_habits = habits.count()

    context = {
        'total_habits': total_habits,
        'habits': habits,
    }
    return render(request, 'habits/dashboard.html', context)

@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'habits/habit_list.html', {'habits': habits})

@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, '¡Hábito creado exitosamente!')
            return redirect('dashboard')
    else:
        form = HabitForm()

    return render(request, 'habits/habit_form.html', {'form': form})

@login_required
def habit_update(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)

    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Hábito actualizado exitosamente!')
            return redirect('dashboard')
    else:
        form = HabitForm(instance=habit)

    return render(request, 'habits/habit_form.html', {'form': form, 'habit': habit})

@login_required
def habit_log(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)

    HabitLog.objects.create(
        habit=habit,
        value=1
    )

    messages.success(request, f'¡Progreso registrado para "{habit.name}"!')

    return redirect('habit_list')

@login_required
def reports(request):
    habits = Habit.objects.filter(user=request.user)

    completed_today = HabitLog.objects.filter(
        habit__user=request.user,
        completed_at__date=timezone.now().date()
    ).count()

    context = {
        'habits': habits,
        'total_habits': habits.count(),
        'completed_today': completed_today,
        'current_streak': completed_today,  # Temporal
    }

    return render(request, 'habits/reports.html', context)

@login_required
def habit_detail(request, pk):
    habit = get_object_or_404(Habit, pk=pk)

    context = {
        "habit": habit
    }

    return render(
        request,
        "habits/habit_detail.html",
        context
    )
    
@login_required
def toggle_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk)

    habit.is_active = not habit.is_active
    habit.save()

    return redirect("habit_list")