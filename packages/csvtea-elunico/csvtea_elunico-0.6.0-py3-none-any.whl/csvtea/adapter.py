import abc
from typing import TypeVar, Optional, TextIO


class OutputAdapter(abc.ABC):
    """
    Output adapters take the output of CSVParser and adapt it to a particular format. They are NOT passed into the
    CSVParser but can be instantiated and used outside of the class. They should implement a `adapt` method that
    takes a single list[list[str]] as is returned from the `parse` method of CSVParser. It can return any type.
    """

    def __init__(self):
        pass

    T = TypeVar('T')

    @abc.abstractmethod
    def adapt(self, output: list[list[str]]) -> T:
        """
        takes a single list[list[str]] as is returned from the `parse` method of CSVParser. It can return any type.
        :param output: the output from the CSVParser to be adapted
        :return: The transformed data
        """
        pass


class DictOutputAdapter(OutputAdapter):
    """
    Transforms the CSV output into a list of dictionaries. Each dictionary in the list has the same keys which correspond
    to the values in the first row of the CSV (the header row) and whose keys are one of the entries in the CSV file
    """

    def adapt(self, output: list[list[str]]) -> list[dict[str, str]]:
        headers = output[0]
        entries = output[1:]
        result = []
        for entry in entries:
            result.append({k: v for k, v in zip(headers, entry)})
        return result


def slow(fn):
    """
    Decorator used to indicate that a method or function is SLOW and may be inefficient to call and should not be called
    in a loop. Attaches an `is_slow` method that returns True
    """
    setattr(fn, 'is_slow', lambda *args, **kwargs: True)
    return fn


class InvalidCSVTable(ValueError):
    pass


class CSVTable:
    def __init__(self, data: list[list[str]]):
        self.rows: list[list[str]] = data[1:]
        self.headers: list[str] = data[0]

        for index, row in enumerate(self.rows):
            if len(row) != len(self.headers):
                raise InvalidCSVTable("Column Count Mismatch: row {} has {} entries "
                                      "but headers has {} entries. ".format(index, len(row), len(self.headers)))

    def index_for_name(self, name: str) -> Optional[int]:
        try:
            return self.headers.index(name)
        except ValueError:
            return None

    def name_for_index(self, index: int) -> Optional[str]:
        try:
            return self.headers[index]
        except IndexError:
            return None

    def concat(self, destination: str, source: str, separator: str = ' ') -> 'CSVTable':
        dest_column_idx = self.index_for_name(destination)
        if dest_column_idx is None:
            raise ValueError('No such header for destination named: {}'.format(destination))

        src_column_idx = self.index_for_name(source)
        if src_column_idx is None:
            raise ValueError('No such header for appendant named: {}'.format(source))

        for index, row in enumerate(self.rows):
            row[dest_column_idx] = row[dest_column_idx] + separator + row[src_column_idx]
            # cutting off headers so we need to go up 1 index
            # self.rows[index + 1] = row
        return self

    def delete(self, column: str) -> 'CSVTable':
        column_idx = self.index_for_name(column)
        if column_idx is None:
            raise ValueError('No such header to delete named: {}'.format(column))

        for index, row in enumerate(self.rows):
            del row[column_idx]
            # data[index] = row

        del self.headers[column_idx]
        return self

    def write(self, file: TextIO) -> int:
        def escape(cell):
            return '"{}"'.format(cell) if ',' in cell else cell

        count = 0
        with file:
            for line in [self.headers] + self.rows:
                count += file.write('{}\n'.format(','.join([escape(i) for i in line])))
        return count

    def unwrap(self) -> list[list[str]]:
        return [self.headers] + self.rows

    @slow
    def remove_empty(self) -> 'CSVTable':
        will_remove = []
        for col_idx in range(len(self.headers)):
            if all(row[col_idx] == '' for row in self.rows):
                will_remove.append(col_idx)

        while will_remove:
            header_idx = will_remove.pop(0)
            self.delete(self.headers[header_idx])
            will_remove = [i - 1 for i in will_remove]

        return self


class CSVTableOutputAdapter(OutputAdapter):
    def adapt(self, output: list[list[str]]) -> CSVTable:
        return CSVTable(output)
