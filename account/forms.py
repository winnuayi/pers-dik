from django import forms
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.forms import ModelForm

from account.models import CustomUser


class ProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email',]

        error_messages = {
            'email': {
                'required': "Mohon diisi."
            },
            # 'fullname': {
            #     'required': "Mohon diisi."
            # },
        }


# class PasswordUpdateForm(forms.Form):
class PasswordUpdateForm(forms.ModelForm):
    MIN_LENGTH = 8

    """A form for changing password"""
    old_password = forms.CharField()
    confirm_password = forms.CharField()
    # old_password = forms.CharField(error_messages={'required': "Mohon diisi."})
    # confirm_password = forms.CharField(error_messages={'required': "Mohon diisi."})

    class Meta:
        model = CustomUser
        fields = ['password']

        # error messages khusus field yang ada di model
        # error_messages = {
        #     'password': {
        #         'required': "Mohon diisi.",
        #         'password_too_common': "Password terlalu umum.",
        #         'password_entirely_numeric': "Password tidak boleh semuanya angka",
        #     },
        # }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        super(PasswordUpdateForm, self).__init__(*args, **kwargs)

        # cek settings.AUTH_PASSWORD_VALIDATION untuk modifikasi validator
        password = self.fields['password']
        password.validators.append(validate_password)

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not check_password(old_password, self.request.user.password):
            raise forms.ValidationError("Old password is wrong")
        return old_password

    def clean(self):
        cleaned_data = super(PasswordUpdateForm, self).clean()

        if 'password' not in cleaned_data or 'password' not in cleaned_data:
            return

        confirm_password = cleaned_data['confirm_password']
        password = cleaned_data['password']

        if confirm_password != password:
            self.add_error('confirm_password', "New password does not match with password confirmation")

    def save(self, commit=True):
        user = super(PasswordUpdateForm, self).save(commit=False)

        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user
