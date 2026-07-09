from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from django.db import IntegrityError
from django.core.exceptions import ValidationError

from .forms import UserRegistrationForm, UserProfileForm, PasswordChangeForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        # Crear instancia sin guardar para poder ejecutar full_clean() (invoca model.clean)
        user = form.save(commit=False)
        try:
            # Ejecuta validaciones del modelo (clean). Levanta ValidationError si hay problemas.
            user.full_clean()
            # Guardar (puede lanzar IntegrityError por unique constraints)
            user.save()
            # Guardar m2m si el form tiene (UserCreationForm normalmente no, pero por si acaso)
            try:
                form.save_m2m()
            except AttributeError:
                pass

        except ValidationError as e:
            # Convertir ValidationError en errores del formulario para que se muestren en la plantilla
            if hasattr(e, 'message_dict'):
                for field, msgs in e.message_dict.items():
                    for msg in msgs:
                        form.add_error(field, msg)
            else:
                # error general (no field)
                form.add_error(None, e)
            return self.form_invalid(form)

        except IntegrityError:
            # Caso de carrera o duplicado inesperado (e.g., student_id ya existe)
            # Asegúrate que 'student_id' es un campo del form; si no, cámbialo por el campo correcto.
            form.add_error('student_id', 'Este número ya está en uso (error de base de datos).')
            return self.form_invalid(form)

        # Si todo OK: iniciar sesión y redirigir
        login(self.request, user)
        messages.success(self.request, '¡Registro exitoso! Bienvenido a biUNestar.')
        return redirect(self.success_url)


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def change_password_view(request):
    # Nota: PasswordChangeForm requiere 'user' como primer argumento
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Mantiene la sesión activa después de cambiar la contraseña
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Contraseña cambiada exitosamente.')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})
