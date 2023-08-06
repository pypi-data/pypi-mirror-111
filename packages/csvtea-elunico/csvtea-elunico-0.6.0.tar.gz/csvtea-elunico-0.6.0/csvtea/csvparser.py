from typing import TextIO, Optional, Union

from csvtea.cells import CellParser, DefaultCellParser, ParseError
from csvtea.format import DefaultCellFormatter, CellFormatter


class CSVParser:
    @classmethod
    def fromfile(cls, file: TextIO, parser: CellParser = DefaultCellParser(),
                 formatter: CellFormatter = DefaultCellFormatter(), *, debug: bool = False):
        return cls(file.read().strip('\r\n') + '\0', parser, formatter, debug=debug)

    @classmethod
    def from_filename(cls, filename: str, parser: CellParser = DefaultCellParser(),
                      formatter: CellFormatter = DefaultCellFormatter(), *, debug: bool = False):
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
        self.parser = parser
        self.formatters = list(formatter) if isinstance(formatter, (tuple, list)) else [formatter]
        self.debug = debug

        self.text = string

    def parse(self) -> list[list[str]]:
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
