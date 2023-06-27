from django.db import models


class Pangkat(models.Model):
    nama = models.CharField(max_length=20)


class Korps(models.Model):
    nama = models.CharField(max_length=5)


class Jabatan(models.Model):
    nama = models.CharField(max_length=200)


class SumberPA(models.Model):
    nama = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Sumber PA'

    def __str__(self):
        return self.nama


class Dikmilti(models.Model):
    nama = models.CharField(max_length=50)


class DikbangSpes(models.Model):
    nama = models.CharField(max_length=50)


class Personil(models.Model):
    nama = models.CharField(max_length=100)
    nrp = models.CharField(max_length=30)
    tgl_lahir = models.DateField()
    pangkat = models.ForeignKey(Pangkat, on_delete=models.CASCADE)
    jabatan = models.ForeignKey(Jabatan, on_delete=models.CASCADE)
    korps = models.ForeignKey(Korps, on_delete=models.CASCADE)


class PersonilSumberPA(models.Model):
    personil = models.ForeignKey(Personil, on_delete=models.CASCADE)
    sumber_pa = models.ForeignKey(SumberPA, on_delete=models.CASCADE)
    tahun = models.IntegerField()


class PersonilDikbangSpes(models.Model):
    personil = models.ForeignKey(Personil, on_delete=models.CASCADE)
    dikbangspes = models.ForeignKey(DikbangSpes, on_delete=models.CASCADE)
    tahun = models.IntegerField()


class PersonilDikmilti(models.Model):
    personil = models.ForeignKey(Personil, on_delete=models.CASCADE)
    dikmilti = models.ForeignKey(Dikmilti, on_delete=models.CASCADE)
    tahun = models.IntegerField()
