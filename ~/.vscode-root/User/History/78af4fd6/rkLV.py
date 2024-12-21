from django import forms
from .models import User
from django.core.exceptions import ValidationError

def LoginForm(request):
    if request.user.is_authenticated:
        return redirect('customer_dashboard')  # تغییر به مسیر مناسب

    if request.method == 'POST':
        form = LoginForm(request.POST)  # فقط request.POST باید به فرم داده شود
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('customer_dashboard')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})



class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label="Confirm Password",
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role']  # Add fields based on your model

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2
