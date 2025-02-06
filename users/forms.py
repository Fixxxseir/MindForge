from django import forms
from django.contrib.auth.forms import UserCreationForm


from users.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ("email", "username", "phone_number", "country", "password1", "password2")
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"placeholder": "Введите почту"})
        self.fields["username"].widget.attrs.update({"placeholder": "Введите никнейм"})
        self.fields["phone_number"].widget.attrs.update({"placeholder": "Введите номер телефона"})
        self.fields["country"].widget.attrs.update({"placeholder": "Введите ваш город"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Введите ваш пароль"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Введите ваш пароль повторно"})


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "phone_number", "country", "avatar")