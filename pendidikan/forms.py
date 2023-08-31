from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from pendidikan.models import Personil


class PersonilForm(ModelForm):
    class Meta:
        model = Personil
        fields = [
            'nama', 'nrp', 'tgl_lahir', 'pangkat', 'jabatan', 'korps',
        ]

        # karena di models tidak null=True dan blank=True, ubah seperti ini
        error_messages = {
            'nama': {'required': "Harap diisi"},
            'nrp': {'required': "Harap diisi"},
        }

    # field-field di bawah ini di models null=True dan blank=True
    # agar bisa insert rows dari excel ke database secara manual
    # sehingga mekanisme validasi field di form harus eksplisit seperti di bawah

    def clean_tgl_lahir(self):
        data = self.cleaned_data['tgl_lahir']

        if data is None:
            raise ValidationError("Harap diisi")

        return data

    def clean_pangkat(self):
        data = self.cleaned_data['pangkat']

        if data is None:
            raise ValidationError("Harap diisi")

        return data

    def clean_jabatan(self):
        data = self.cleaned_data['jabatan']

        if data is None:
            raise ValidationError("Harap diisi")

        return data

    def clean_korps(self):
        data = self.cleaned_data['korps']

        if data is None:
            raise ValidationError("Harap diisi")

        return data
