import csv

from commons import hd28


class ScnorrSignatureContainer:

    def __init__(self):
        self.file = None
        self.p = 0
        self.g = 0
        self.headers = {}

    def get_results(self):
        return self._process_rows()

    def _process_rows(self):
        if not self.file:
            return

        reader = csv.DictReader(self.file, delimiter=';')
        for row in reader:
            pass

        return self._result_csv()

    def _validate(self, row):
        pass

    def _result_csv(self):
        return


class ScnorrSignature:

    def __init__(self, p, g, a):
        self.p = p
        self.g = g
        self.a = a

    def signature_verification(self, r, s, message):
        """g^s = r * a^h mod p"""

        h = hd28(message + r)
        g_s = pow(self.g, s, self.p)
        a_h = pow(self.a, h, self.p)
        rah = (r * a_h) % self.p
        return g_s == rah