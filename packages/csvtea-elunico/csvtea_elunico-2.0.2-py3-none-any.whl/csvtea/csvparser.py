from typing import TextIO, Optional, Union

from csvtea.cell import CellParser, DefaultCellParser, ParseError
from csvtea.format import DefaultCellFormatter, CellFormatter


class CSVParser:
    """
    Main class for parsing CSV Files. Allows pluggable behavior by letting the user inject a custom parser (see
    CellParser in the cells module) and a custom formatter (see formatter in the format module). These change the way
    the text of the CSV is parsed and the values that are stored in the cells (respectively) allowing you to adapt
    this to--for one example--parse a tab separated file and convert None's to nulls, regularize capitalization, etc.

    The normal constructor uses a string and then the parser and formatter. Setting debug to True in the constructor
    will produce *MUCH* more verbose exceptions

    Values returned by parse are primitives to make manipulation easy. Also adapters (see adapter module) take the shape
    of data retuned by the parse method. It is recommended, if you do not have a custom adapter to use, that you use the
    CSVTableOutputAdapter to get a CSVTable object, as this makes manipulating the table much easier
    """
    @classmethod
    def fromfile(cls, file: TextIO, parser: CellParser = DefaultCellParser(),
                 formatter: CellFormatter = DefaultCellFormatter(), *, debug: bool = False):
        """
        Create a parser from a file. note that the parsing, and resulting data is not available until parse() is called
        :param file: file object that can read the CSV
        :param parser: the CellParser object to parse with (see cells module)
        :param formatter: the CellFormatter object to format parsed cells with (see format module)
        :param debug: when debug is True, MUCH more verbose errors are produced
        :return: initialized instance
        """
        return cls(file.read().strip('\r\n') + '\0', parser, formatter, debug=debug)

    @classmethod
    def from_filename(cls, filename: str, parser: CellParser = DefaultCellParser(),
                      formatter: CellFormatter = DefaultCellFormatter(), *, debug: bool = False):
        """
        The same as CSVParser.fromfile() but will safely open the file with `filename` for reading before calling
        fromfile(). note that the parsing, and resulting data is not available until parse() is called
        :param filename: filename to open, read, and parse
        :param parser: the CellParser object to parse with (see cells module)
        :param formatter: the CellFormatter object to format parsed cells with (see format module)
        :param debug: when debug is True, MUCH more verbose errors are produced
        :return: initialized instance
        """
        with open(filename) as f:
            return cls.fromfile(f, parser, formatter, debug=debug)

    def __init__(
            self,
            string: str,
            parser: CellParser = DefaultCellParser(),
            formatter: Union[CellFormatter, list[CellFormatter]] = DefaultCellFormatter(),
            *,
            debug: bool = False
    ):
        """
        create a parser from a string. note that the parsing, and resulting data is not available until parse() is called
        :param string: string to parse
        :param parser: the CellParser object to parse with (see cells module)
        :param formatter: the CellFormatter object to format parsed cells with (see format module)
        :param debug: when debug is True, MUCH more verbose errors are produced
        :return: initialized instance
        """
        self.parser = parser
        self.formatters = list(formatter) if isinstance(formatter, (tuple, list)) else [formatter]
        self.debug = debug

        self.text = string

    def parse(self) -> list[list[str]]:
        """
        Parse the data using the specified parameters and return the resulting data.
        :return: the parsed data
        """
        cells = []
        row = []
        text = self.text
        while text:
            try:
                cell, cell_end, row_done = self.parser.parse(text)
            except ParseError as e:
                if self.debug:
                    error = ParseError(f'Error in parse. Cannot match quoted key. '
                                       f'Text is {text!r}\ncells length is {len(cells)}\n'
                                       f'row length is {len(row)}')
                    raise error from e
                else:
                    raise
            for formatter in self.formatters:
                cell = formatter.format(cell)
            row.append(cell)
            if row_done:
                cells.append(row)
                row = []
            text = text[cell_end:]
        return cells
