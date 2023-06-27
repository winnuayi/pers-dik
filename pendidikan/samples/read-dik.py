from datetime import datetime
import os
import sys

# standalone django
import django
sys.path.append('../../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from account.models import CustomUser

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
        # self.sheet = self.book.sheet_by_name('GOL IV KOL')

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
        print(set(pangkat_list))

    def get_korps(self):
        # abaikan data berisi None, hanya pangkat tanpa korps, dan jenderal tanpa korps
        korps_list = list(filter(lambda x: x['pangkat'] is not None
                                           and len(x['pangkat']) > 1
                                           and x['pangkat'][1] is not None,
                                 self.data))

        korps_list = list(map(lambda x: x['pangkat'][1], korps_list))

        print(set(korps_list))

    def get_sumber_pa(self):
        sumber_pa_list = list(map(lambda x: x['sumber_pa'][0]
                                            if len(x['sumber_pa']) > 0
                                            else None,
                              self.data))

        print(set(sumber_pa_list))

    def get_dikmilti(self):
        dikmilti_list = list(map(lambda x: x['dikmilti'][0]
                                           if x['dikmilti'] is not None
                                           else None, self.data))

        print(set(dikmilti_list))

    def get_dikbang_spes(self):
        dikbang_spes_list = list(map(lambda x: x['dikbang_spes'], self.data))
        dikbang_spes_list = list(filter(lambda x: x[0] != '', dikbang_spes_list))

        result = set()
        for dikbang_spes in dikbang_spes_list:
            for dik in dikbang_spes:
                if dik == '': continue
                result.add(dik)

        print(list(result))


if __name__ == '__main__':
    dik_list = Extractor(FILENAME).process()
    Transformer(dik_list).get_pangkat()
