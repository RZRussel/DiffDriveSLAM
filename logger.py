import csv


class Logger:
    def __init__(self, path):
        self._csvfile = open(path, 'w')
        self._csvwriter = csv.writer(self._csvfile, delimiter=' ')

    def log(self, values):
        self._csvwriter.writerow(values)

    def complete(self):
        self._csvfile.close()

        del self._csvwriter
        del self._csvfile
