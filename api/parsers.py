from io import BytesIO
import collections


class CSVParser():

    def __init__(self, file, delimiter):
        self.file = file.read().decode('utf-8').splitlines()
        self.delimiter = delimiter

    def parse(self):
        data = []
        record = collections.OrderedDict()
        line_count = 0

        for row in self.file:
            if line_count == 0:
                for field in row.split(self.delimiter):
                    record[field] = ""
                line_count += 1
            else:
                new = collections.OrderedDict(record)
                keys = list(record.keys())
                for index, value in enumerate(row.split(self.delimiter)):
                    new[keys[index]] = value
                data.append(new)
                line_count += 1

        data = [dict(record) for record in data]
        return data
