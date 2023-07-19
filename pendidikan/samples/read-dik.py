from datetime import datetime
import os
import sys

# standalone django
import django
sys.path.append('../../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.db import IntegrityError, transaction

from pendidikan.models import Dikbangspes, Dikmilti, Jabatan, Korps, Pangkat, \
    Personil, PersonilDikbangspes, PersonilDikmilti, PersonilSumberPa, SumberPa

import xlrd


DEBUG = False

FILENAME = 'dik-v2.xls'

NUM_IGNORE_ROWS = 7

COL_URUT = 0
COL_BAG = 1
COL_GOL = 2
COL_SAT_JAB = 3
COL_PEJABAT = 4
COL_PANGKAT = 5
COL_NRP = 6
COL_SUMBER_PA = 7
COL_DIKMILTI = 8
COL_TGL_LAHIR = 9
COL_DIKBANG_SPES = 10

MODE_1900_BASED = 0


class Extractor:
    def __init__(self, filename):
        self.book = xlrd.open_workbook(filename)

    def clean_nrp(self, nrp):
        # untuk NRP dengan format float, convert jadi str
        if type(nrp) == float:
            nrp = "%.0f" % nrp

        return nrp

    def clean_pangkat(self, pangkat):
        if pangkat == '':
            return

        s = pangkat.split()

        pangkat = s[0]

        korps = None

        # untuk pati
        if len(s) > 1 and s[1] == 'TNI':
            pangkat = "{} {}".format(s[0], s[1])
        # untuk selain pati
        elif len(s):
            korps = ' '.join(s[1:])

        # utk kondisi hanya 1 kata (pangkat tanpa korps), langsung pass

        return [pangkat, korps]

    def clean_sumber_pa(self, sumber_pa):
        return sumber_pa.split()

    def clean_dikmilti(self, dikmilti):
        if not dikmilti:
            return

        s = dikmilti.split()

        if len(s) == 3:
            s = [' '.join(s[:2])] + s[2:]

        # contoh sesko tni tanpa tahun
        if len(s) == 2 and s[1].isalpha():
            s = [' '.join(s[:2])]

        return s

    def clean_tgl_lahir(self, tgl_lahir):
        """Konversi XLRD Date menjadi Python Date"""
        if not tgl_lahir:
            return

        if type(tgl_lahir) == str and '-' in tgl_lahir:
            # ada tanggal lahir dengan spasi. ada tanggal lahir diawali '
            tgl_lahir = tgl_lahir.strip().lstrip("'")
            tgl_lahir = datetime.strptime(tgl_lahir.strip(), "%d-%m-%Y")
            return tgl_lahir.date()

        # terkadang sudah dg format dd/mm/yyyy, type str bukan type xldate
        if type(tgl_lahir) == str and '/' in tgl_lahir:
            tgl_lahir = datetime.strptime(tgl_lahir.strip(), "%d/%m/%Y")
            return tgl_lahir.date()

        d = xlrd.xldate_as_datetime(tgl_lahir, MODE_1900_BASED)

        return d.date()

    def clean_dikbang_spes(self, dikbang_spes):
        return dikbang_spes.split('\n')

    def process(self):
        result = []

        for sheet in self.book.sheets():
            for index, row in enumerate(sheet):
                try:
                    # abaikan baris 0 hingga N+1
                    if index in range(NUM_IGNORE_ROWS): continue

                    # abaikan baris tanpa NRP
                    # if row[COL_NRP].value == '': continue
                    if row[COL_URUT].value == '': continue

                    nrp = self.clean_nrp(row[COL_NRP].value)
                    pangkat = self.clean_pangkat(row[COL_PANGKAT].value)
                    tgl_lahir = self.clean_tgl_lahir(row[COL_TGL_LAHIR].value)
                    sumber_pa = self.clean_sumber_pa(row[COL_SUMBER_PA].value)
                    dikmilti = self.clean_dikmilti(row[COL_DIKMILTI].value)
                    dikbang_spes = self.clean_dikbang_spes(row[COL_DIKBANG_SPES].value)

                    if DEBUG:
                        print('{:>15} {} {} {:43} {} {} {} {}' \
                            .format(nrp,
                                    pangkat,
                                    row[COL_SAT_JAB].value,
                                    row[COL_PEJABAT].value,
                                    sumber_pa,
                                    dikmilti,
                                    tgl_lahir,
                                    dikbang_spes))

                    result.append({
                        'nrp': nrp,
                        'pangkat': pangkat,
                        'sat_jab': row[COL_SAT_JAB].value,
                        'pejabat': row[COL_PEJABAT].value,
                        'sumber_pa': sumber_pa,
                        'dikmilti': dikmilti,
                        'tgl_lahir': tgl_lahir,
                        'dikbang_spes': dikbang_spes,
                    })
                except Exception:
                    print(sheet)
                    print(row)
                    sys.exit()

        return result


class Transformer:
    def __init__(self, data):
        self.data = data

    def get_pangkat(self):
        pangkat_list = list(filter(lambda x: x['pangkat'] is not None, self.data))
        pangkat_list = list(map(lambda x: x['pangkat'][0], pangkat_list))

        return list(set(pangkat_list))

    def get_korps(self):
        # ['Letda', 'Inf']
        # abaikan data berisi None, hanya pangkat tanpa korps, dan jenderal tanpa korps
        korps_list = list(filter(lambda x: x['pangkat'] is not None
                                               and len(x['pangkat']) > 1
                                               and x['pangkat'][1] is not None
                                               and x['pangkat'][1] != '',
                                 self.data))

        # title() untuk memastikan semua korps diawali huruf besar
        korps_list = list(map(lambda x: x['pangkat'][1].title(), korps_list))

        return list(set(korps_list))

    def get_sumber_pa(self):
        # ['Capa', 19]
        sumber_pa_list = list(map(lambda x: x['sumber_pa'][0]
                                            if len(x['sumber_pa']) > 0
                                            else None,
                              self.data))
        # buang None
        sumber_pa_list = list(filter(lambda x: x is not None and x.isalpha(),
                                     sumber_pa_list))

        return list(set(sumber_pa_list))

    def get_dikmilti(self):
        dikmilti_list = list(map(lambda x: x['dikmilti'][0]
                                           if x['dikmilti'] is not None
                                           else None, self.data))

        dikmilti_list = list(filter(lambda x: x is not None, dikmilti_list))

        return list(set(dikmilti_list))

    def get_dikbangspes(self):
        dikbang_spes_list = list(map(lambda x: x['dikbang_spes'], self.data))
        dikbang_spes_list = list(filter(lambda x: x[0] != '', dikbang_spes_list))

        result = set()
        for dikbang_spes in dikbang_spes_list:
            for dik in dikbang_spes:
                if dik == '': continue
                result.add(dik)

        return list(result)


class Loader:
    def save_jabatan(self, dik_list):
        jabatan_objects = list()
        for row in dik_list:
            objects = Jabatan(nama=row['sat_jab'])
            jabatan_objects.append(objects)

        try:
            with transaction.atomic():
                Jabatan.objects.bulk_create(jabatan_objects)
        except IntegrityError:
            print("Jabatan is duplicate.")

    def save_pangkat(self, pangkat_list):
        pangkat_objects = list()
        for pangkat in pangkat_list:
            objects = Pangkat(nama=pangkat)
            pangkat_objects.append(objects)

        try:
            with transaction.atomic():
                Pangkat.objects.bulk_create(pangkat_objects)
        except IntegrityError:
            print("Pangkat is duplicate.")

    def save_korps(self, korps_list):
        korps_objects = list()
        for korps in korps_list:
            objects = Korps(nama=korps)
            korps_objects.append(objects)

        try:
            with transaction.atomic():
                Korps.objects.bulk_create(korps_objects)
        except IntegrityError:
            print("Korps is duplicate.")

    def save_sumber_pa(self, sumber_pa_list):
        sumber_pa_objects = list()
        for sumber_pa in sumber_pa_list:
            objects = SumberPa(nama=sumber_pa)
            sumber_pa_objects.append(objects)

        try:
            with transaction.atomic():
                SumberPa.objects.bulk_create(sumber_pa_objects)
        except IntegrityError:
            print("SumberPA is duplicate.")

    def save_dikmilti(self, dikmilti_list):
        dikmilti_objects = list()
        for dikmilti in dikmilti_list:
            objects = Dikmilti(nama=dikmilti)
            dikmilti_objects.append(objects)

        try:
            with transaction.atomic():
                Dikmilti.objects.bulk_create(dikmilti_objects)
        except IntegrityError:
            print("Dikmilti is duplicate.")


    def save_dikbangspes(self, dikbangspes_list):
        dikbangspes_objects = list()
        for dikbangspes in dikbangspes_list:
            objects = Dikbangspes(nama=dikbangspes)
            dikbangspes_objects.append(objects)

        try:
            with transaction.atomic():
                Dikbangspes.objects.bulk_create(dikbangspes_objects)
        except IntegrityError:
            print("Dikbangspes is duplicate.")

    def save_personil(self, dik_list):
        personil_objects = list()
        personil_sumber_pa_objects = list()
        personil_dikmilti_objects = list()
        personil_dikbangspes_objects = list()

        for personil in dik_list:
            # abaikan jabatan yang tidak ada pejabatnya
            if personil['pejabat'] in ["Kosong", "Orgas Baru", "Validasi Orgas"]:
                continue

            print(personil)

            # dapatkan pangkat object
            pangkat = None
            if personil['pangkat'] is not None:
                pangkat = Pangkat.objects.get(nama=personil['pangkat'][0])

            # dapatkan korps object. set None untuk pejabat tanpa korps
            korps = None
            if personil['pangkat'] is not None \
                    and personil['pangkat'][1] is not None \
                    and len(personil['pangkat'][1]) > 0 \
                    and personil['pangkat'][1] != '':
                korps_str = personil['pangkat'][1].title()
                korps = Korps.objects.get(nama=korps_str)

            # dapatkan jabatan object. most likely semua row ada jabatan
            jabatan = None
            if personil['sat_jab'] is not None:
                jabatan = Jabatan.objects.get(nama=personil['sat_jab'])

            object = Personil(nama=personil['pejabat'],
                              nrp=personil['nrp'],
                              tgl_lahir=personil['tgl_lahir'],
                              pangkat=pangkat,
                              jabatan=jabatan,
                              korps=korps)

            personil_objects.append(object)

            # row dengan sumber_pa tidak diisi, diabaikan
            if len(personil['sumber_pa']) > 0 \
                    and personil['sumber_pa'][0].isalpha():
                sumber_pa = SumberPa.objects.get(nama=personil['sumber_pa'][0])
                sumber_pa_tahun = int(personil['sumber_pa'][1])

                personil_sumber_pa_object = PersonilSumberPa(personil=object,
                                                            sumber_pa=sumber_pa,
                                                            tahun=sumber_pa_tahun)

                personil_sumber_pa_objects.append(personil_sumber_pa_object)

            # row dengan dikmilti, diproses
            if personil['dikmilti'] is not None:
                dikmilti = Dikmilti.objects.get(nama=personil['dikmilti'][0])

                dikmilti_tahun = None
                if len(personil['dikmilti']) > 1:
                    dikmilti_tahun = int(personil['dikmilti'][1])

                dikmilti_object = PersonilDikmilti(personil=object,
                                                   dikmilti=dikmilti,
                                                   tahun=dikmilti_tahun)

                personil_dikmilti_objects.append(dikmilti_object)

            # row bisa memiliki lebih dari 1 dikbangspes
            if personil['dikbang_spes'] is not None:
                for dikbangspes in personil['dikbang_spes']:
                    # abaikan jika isian dikbangspes adalah empty string
                    if dikbangspes == '': continue

                    dikbangspes = Dikbangspes.objects.get(nama=dikbangspes)
                    dikbangspes_object = PersonilDikbangspes(personil=object,
                                                             dikbangspes=dikbangspes)

                    personil_dikbangspes_objects.append(dikbangspes_object)

        try:
            with transaction.atomic():
                Personil.objects.bulk_create(personil_objects)
                PersonilSumberPa.objects.bulk_create(personil_sumber_pa_objects)
                PersonilDikmilti.objects.bulk_create(personil_dikmilti_objects)
                PersonilDikbangspes.objects.bulk_create(personil_dikbangspes_objects)
        except IntegrityError as e:
            print("Error when saving personil: {}".format(e))



if __name__ == '__main__':
    # ekstrak excel file ke python object
    dik_list = Extractor(FILENAME).process()

    # rapikan agar menjadi terstruktur
    pangkat_list = Transformer(dik_list).get_pangkat()
    korps_list = Transformer(dik_list).get_korps()
    sumber_pa_list = Transformer(dik_list).get_sumber_pa()
    dikmilti_list = Transformer(dik_list).get_dikmilti()
    dikbangspes_list = Transformer(dik_list).get_dikbangspes()

    # simpan ke database
    Loader().save_jabatan(dik_list)
    Loader().save_pangkat(pangkat_list)
    Loader().save_korps(korps_list)
    Loader().save_sumber_pa(sumber_pa_list)
    Loader().save_dikmilti(dikmilti_list)
    Loader().save_dikbangspes(dikbangspes_list)
    Loader().save_personil(dik_list)
