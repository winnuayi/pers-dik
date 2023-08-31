from django.db import models


class Pangkat(models.Model):
    nama = models.CharField(max_length=20, unique=True)
    counter = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Pangkat'

    def __str__(self):
        return self.nama


class Korps(models.Model):
    nama = models.CharField(max_length=10, unique=True)


class Jabatan(models.Model):
    nama = models.CharField(max_length=200, unique=True)


class SumberPa(models.Model):
    nama = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Sumber PA'

    def __str__(self):
        return self.nama


class Dikmilti(models.Model):
    nama = models.CharField(max_length=50, unique=True)


class Dikbangspes(models.Model):
    nama = models.CharField(max_length=50, unique=True)


class Personil(models.Model):
    nama = models.CharField(max_length=100)
    nrp = models.CharField(max_length=30)
    tgl_lahir = models.DateField(null=True, blank=True)
    pangkat = models.ForeignKey(Pangkat, on_delete=models.CASCADE,
                                null=True, blank=True)
    jabatan = models.ForeignKey(Jabatan, on_delete=models.CASCADE,
                                null=True, blank=True,
                                related_name='personil')
    korps = models.ForeignKey(Korps, on_delete=models.CASCADE,
                              null=True, blank=True)

    def __str__(self):
        pangkat = self.pangkat.nama if self.pangkat is not None else None
        return "{} {}".format(self.nama, pangkat)


class PersonilSumberPa(models.Model):
    personil = models.ForeignKey(Personil, on_delete=models.CASCADE,
                                 related_name='personil_sumber_pa')
    sumber_pa = models.ForeignKey(SumberPa, on_delete=models.CASCADE)
    tahun = models.IntegerField()


class PersonilDikbangspes(models.Model):
    personil = models.ForeignKey(Personil, on_delete=models.CASCADE,
                                 related_name='personil_dikbangspes')
    dikbangspes = models.ForeignKey(Dikbangspes, on_delete=models.CASCADE)


class PersonilDikmilti(models.Model):
    personil = models.ForeignKey(Personil, on_delete=models.CASCADE,
                                 related_name='personil_dikmilti')
    dikmilti = models.ForeignKey(Dikmilti, on_delete=models.CASCADE)
    tahun = models.IntegerField(null=True, blank=True)
