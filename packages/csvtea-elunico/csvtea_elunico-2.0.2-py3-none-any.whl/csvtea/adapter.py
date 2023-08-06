import abc
from typing import TypeVar, Optional, TextIO, Union, Callable, Any, Iterable


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
    """
    Class that represents the data in a CSV file. Allows you to ask for indices and header names, concatenate columns,
    remove columns, append rows and write to files

    Constructed from a list[list[str]] where each list[str] in the outer list represents a row in the CSV and each
    str in that list represents an entry cell in the CSV.

    **Important!** This class will occasionally use a row number or row index, when indexing into the rows the
    FIRST ROW OF DATA is the 0th element. Even thought the headers are the top row, indexing considers the first row
    of data to be index 0

    This is the shape of data returned by CSVParser

    CSV *must* have header columns to work with this class.
    """

    def __init__(self, data: list[list[str]]):
        self._rows: list[list[str]] = data[1:]
        self._headers: list[str] = data[0]

        for index, row in enumerate(self._rows):
            if len(row) != len(self._headers):
                raise InvalidCSVTable("Column Count Mismatch: row {} has {} entries "
                                      "but headers has {} entries. ".format(index, len(row), len(self._headers)))

    @property
    def headers(self) -> Iterable[str]:
        """
        Return a list of strings that describe the columns of the table, aka the header row of the table.
        These values can be used anywhere column names are needed
        :return: the table headers (column names)
        """
        return self._headers[:]

    @property
    def rows(self) -> Iterable[list[str]]:
        """
        Returns a list of all the rows where each row is represented as a list[str]
        :return: list of rows
        """
        return self._rows[:]

    @property
    def columns(self) -> Iterable[list[str]]:
        """
        Return a list of columns where a column is a list of str. This is different as each list[str] in the list
        returned by this method represents the cell values across ALL ROWS but only for a particular column. It is
        essentially the transposition of the `rows` property
        :return: list of columns in the table
        """
        result = []
        for column in self._headers:
            result.append(self.column_cells(column))
        return result

    def index_for_name(self, name: str) -> Optional[int]:
        """
        Return the index (0-based) of the name of a column header in the CSV
        :param name: the name of the column to find the index of
        :return: the index of the column with that name or None if no such column exists
        """
        try:
            return self._headers.index(name)
        except ValueError:
            return None

    def name_for_index(self, index: int) -> Optional[str]:
        """
        Return the header name for the column at the given index
        :param index: the index of the column (0-based)
        :return: the name of the column at that index or None if it is out of range
        """
        try:
            return self._headers[index]
        except IndexError:
            return None

    def __getitem__(self, column: str, row: Optional[int] = None) -> Union[list[str], str]:
        """
        Return data from the table. If row is None, then return an ordered list of all the values in every row
        for the given column name. If row is an int, then return the content of the cell in the column named `column`
        and in the row `row`.

        :param column: name of the column to get
        :param row: row index to get
        :return: the list of values for a column or the value of a column on a particular row
        """
        idx = self.index_for_name(column)
        if idx is None:
            raise IndexError("No such column {} ".format(column))

        if row is not None:
            return self._rows[row][idx]
        else:
            return self.column_cells(column)

    def __setitem__(self, column: str, row: int, value: str):
        """
        Set the content of the cell in row `row` under the column with the header name `column` to the value `value`
        :param column: name of the column to edit
        :param row: row index to edit
        :param value: new value to place in the table
        :return: None
        """
        name = self.index_for_name(column)
        if name is None:
            raise IndexError("No such column {} ".format(column))
        self._rows[row][name] = value

    def create_column(self, name: str, default_value: Optional[str] = '') -> 'CSVTable':
        """
        Create a new column at the end of the CSV with the name `name`.
        You can provide a default_value to put into all the rows for the new column

        :param name: header name of the column to create
        :param default_value: the value to fill in all the rows of the new column
        :return: self
        """
        self._headers.append(name)
        for row in self._rows:
            row.append(default_value)
        return self

    def concat(self, destination: str, source: str, separator: str = ' ') -> 'CSVTable':
        """
        Concatenates the content of every cell in the column with the name passed as `source` to the
        content of every cell in the column with the name `destination` separated by `separator`. The concatenated
        value is then written back to the column named destination, OVERWRITING what was originally there.

        If you want to concat two columns into a new columns, first use `create_column` to make the column then
        do 2 concats into the now empty column

        Will raise a ValueError if either the destionation or source do not refer to a column name
        :param destination: the destination cell (first part of the concat) and place where the concatenation is written
        :param source: the source cell (concat'd to the content of destination)
        :param separator: string separating the content of destination and source
        :raises ValueError: if no columns with the name given in destination or source exist
        :return: self
        """
        dest_column_idx = self.index_for_name(destination)
        if dest_column_idx is None:
            raise ValueError('No such header for destination named: {}'.format(destination))

        src_column_idx = self.index_for_name(source)
        if src_column_idx is None:
            raise ValueError('No such header for appendant named: {}'.format(source))

        for index, row in enumerate(self._rows):
            row[dest_column_idx] = row[dest_column_idx] + separator + row[src_column_idx]
            # cutting off headers so we need to go up 1 index
            # self._rows[index + 1] = row
        return self

    def delete(self, column: str) -> 'CSVTable':
        """
        Deletes the column named 'column' and all the data in the all the rows in the column
        :param column: the name of the column to delete
        :return: self
        """
        column_idx = self.index_for_name(column)
        if column_idx is None:
            raise ValueError('No such header to delete named: {}'.format(column))

        for index, row in enumerate(self._rows):
            del row[column_idx]
            # data[index] = row

        del self._headers[column_idx]
        return self

    @slow
    def remove_empty(self) -> 'CSVTable':
        """
        Removes any columns and all associated cells that are completed empty in every row.

        Can be slow as it has to do a lot of iterating to check due to the data structures that hold the CSV data
        :return: self
        """
        will_remove = []
        for col_idx in range(len(self._headers)):
            if all(row[col_idx] == '' for row in self._rows):
                will_remove.append(col_idx)

        while will_remove:
            header_idx = will_remove.pop(0)
            self.delete(self._headers[header_idx])
            will_remove = [i - 1 for i in will_remove]

        return self

    def column_cells(self, column_name: str) -> Optional[list[str]]:
        """
        Returns all the values in all rows for a particular column according to `column_name`. Cell values are in order
        as they appear in rows in the column
        :param column_name: name of the volume whose cell values you want
        :return: list of all the cell values for a column in row order or None if there is no such column name
        """
        idx = self.index_for_name(column_name)
        if idx is None:
            return None

        return [row[idx] for row in self._rows]

    def map_cells(self, transform: Callable[[str], Any]) -> 'CSVTable':
        """
        Iterates through each cell replacing the value of the cell with the result of calling `transform` on the current cell value
        :param transform: the function used to transform each cell
        :return: self
        """
        for row in self._rows:
            for i in range(len(row)):
                row[i] = transform(row[i])
        return self

    def map_column(self, name: str, transform: Callable[[str], Any]) -> 'CSVTable':
        """
        Replaces every row's value for the column specified in `name` with the result of calling `transform` on the current
        value in the cell for that row and column
        :param name: name of the column to transform values in
        :param transform: operation to perform on the column's cells
        :return: self
        """
        idx = self.index_for_name(name)
        for row in self._rows:
            row[idx] = transform(row[idx])
        return self

    def map_columns_where(self, should_map: Callable[[str, list[str]], bool],
                         transform: Callable[[str], Any]) -> 'CSVTable':
        """
        Like map_column, but perform the transformation on ALL columns that match a predicate. `should_map` accepts
        a column name and the list of cells for each row in the column and should return True if the values in that
        column SHOULD be transformed and should return False if the values in that column SHOULD NOT be transformed
        :param should_map: predicate that receives column name and row values and returns True if the values SHOULD be transformed
        :param transform: transformation to perform on values in matching columns
        :return: self
        """
        for idx, column in enumerate(self._headers):
            if should_map(column, self.column_cells(column)):
                self.map_column(column, transform)
        return self

    def count_cells(self, predicate: Callable[[str], bool]) -> int:
        """
        Returns the number of cells whose value matches the given predicate `predicate`
        :param predicate: predicate used to test cell values
        :return: number of cells that match the predicate
        """
        return sum(1 for row in self._rows for cell in row if predicate(cell))

    def append(self, row: list[str]) -> 'CSVTable':
        """
        Append a single extra row to the table. List length should match length of headers of the table
        :param row: row to append
        :return: self
        """
        if len(row) != len(self._headers):
            raise ValueError("Row has the wrong number of entries for table")
        self._rows.append(row)
        return self

    def extend(self, rows: list[list[str]]) -> 'CSVTable':
        """
        Add several rows to the bottom of the csv. Data must match the arity of the headers in the table
        :param rows: additional rows to add
        :return: self
        """
        for i, row in enumerate(rows):
            if len(row) != len(self._headers):
                raise ValueError(
                    'Row {} has {} entries but should have {} entries'.format(i, len(row), len(self._headers)))
        self._rows.extend(rows)
        return self

    def unwrap(self) -> list[list[str]]:
        """
        Return the data of the table in the form of Python primitives--a list[list[str]]. This is the same data that
        is used to construct this class meaning, CSVTable(table.unwrap()) is essentially doing nothing but wasting object allocations
        :return:
        """
        return [self._headers] + self._rows

    def write(self, file: TextIO, row_sep: str = '\n', cell_sep: str = ',', quote_char: str = '"') -> int:
        """
        Write the data to the given file in the CSV format. No validation is done on the containing data. If the parsing
        was customized using CSVParser and does not conform to standard CSV formats, that will not be checked by the class.

        Furthermore, the row separator (normally new line) and the cell separator (normally a comma) and the quote char
        (normally ") can be customized, making it trivial to write a tab-separated file as well

        :param file: file to write to
        :param row_sep: char or string that separates rows in the file
        :param cell_sep: char or string that separates columns in the file
        :param quote_char: char or string that quotes cells with commas in them
        :return: number of bytes written
        """

        def escape(cell):
            return '{}{}{}'.format(quote_char, cell, quote_char) if ',' in cell else cell

        count = 0
        with file:
            for line in [self._headers] + self._rows:
                count += file.write('{}{}'.format(cell_sep.join([escape(i) for i in line]), row_sep))
        return count

    def __str__(self):
        return 'CSVTable[columns={}, rows={}]'.format(len(self._headers), len(self._rows))

    def __repr__(self) -> str:
        return str(self)


class CSVTableOutputAdapter(OutputAdapter):
    """
    Create a CSVTable object from the given output data
    """

    def adapt(self, output: list[list[str]]) -> CSVTable:
        return CSVTable(output)
