"""
Contains user-defined parser classes.
"""
import collections


class CSVParser():
    """
    CSVParser - Parses a CSV formatted in-memory loaded file.

    Attributes:
        file: in-memory loaded file
        delimiter: delimiter character
    """

    def __init__(self, file, delimiter):
        """
        Creates a `CSVParser` instance.

        Parameters:
            file: in-memory loaded file
            delimiter: delimiter character
        """
        self.file = file.read().decode('utf-8').splitlines()
        self.delimiter = delimiter

    def parse(self):
        """
        parse - Parses its file member and returs a list of dictionaries
        containing its resulting data.
        """
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
