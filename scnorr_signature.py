import csv
import datetime

from commons import hd28


class ScnorrSignatureContainer:

    def __init__(self):
        self.file = None
        self.p = 0
        self.g = 0
        self.headers = {}

    def get_results(self):
        try:
            success = self._process_rows()
        except BaseException:
            success = False
        if success:
            return "Failas nuskaitytas sėkmingai"
        return "Įvyko nenumatyta klaida"

    def _process_rows(self):
        if not self.file:
            return False

        reader = csv.DictReader(self.file, delimiter=';')
        result_rows = []
        for row in reader:
            if not self._validate(row):
                continue
            r = int(row[self.headers["r"]])
            s = int(row[self.headers["s"]])
            message = row[self.headers["message"]]
            public_key = int(row[self.headers["public_key"]])

            signature = ScnorrSignature(self.p, self.g, public_key)
            result = signature.signature_verification(r, s, message)
            row[self.headers["verification"]] = result
            result_rows.append(row)

        if len(result_rows) > 0:
            self._result_csv(result_rows)
            return True
        return False

    def _validate(self, row):
        return (
                self.headers["r"] in row.keys() and
                self.headers["s"] in row.keys() and
                self.headers["message"] in row.keys() and
                self.headers["public_key"] in row.keys()
        )

    def _result_csv(self, rows):
        filename = f'Verification_{datetime.datetime.now().strftime("%Y_%m_%d_%H%M")}.csv'
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)


class ScnorrSignature:

    def __init__(self, p, g, a):
        self.p = p
        self.g = g
        self.a = a

    def signature_verification(self, r, s, message):
        """g^s = r * a^h mod p"""

        h = hd28(message + str(r))
        g_s = pow(self.g, s, self.p)
        a_h = pow(self.a, h, self.p)
        rah = (r * a_h) % self.p
        return g_s == rah