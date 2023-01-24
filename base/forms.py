from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import Project, TargetFloor, ActualFloor, Block, Floor, Zone
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {'start_date': forms.DateInput(
            attrs={'type': 'date'}), 'due_date': forms.DateInput(
            attrs={'type': 'date'})}


class TargetFloorForm(ModelForm):
    class Meta:
        model = TargetFloor
        fields = '__all__'
        exclude = ("target_start_date",)


class UpdateTargetFloorForm(ModelForm):
    class Meta:
        model = TargetFloor
        fields = '__all__'
        exclude = ("target_start_date",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["project"].disabled = True
        self.fields["block"].disabled = True
        self.fields["zone"].disabled = True
        self.fields["floor"].disabled = True


class ActualFloorForm(ModelForm):
    class Meta:
        model = ActualFloor
        fields = '__all__'
        exclude = ("actual_start_date",)


class UpdateActualFloorForm(ModelForm):
    class Meta:
        model = ActualFloor
        fields = '__all__'
        exclude = ('actual_start_date',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["project"].disabled = True
        self.fields["block"].disabled = True
        self.fields["zone"].disabled = True
        self.fields["floor"].disabled = True


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        def save(self, commit=True):
            user = super(UserForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = User()
        fields = ['new_password1', 'new_password2']
