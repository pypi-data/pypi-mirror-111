from typing import TextIO


def write_csv(file: TextIO, data: list[list[str]]) -> int:
    def escape(cell):
        return '"{}"'.format(cell) if ',' in cell else cell

    count = 0
    with file:
        for line in data:
            count += file.write('{}\n'.format(','.join([escape(i) for i in line])))
    return count


def concat(data: list[list[str]], destination: str, appendant: str, separator: str = ' ') -> list[list[str]]:
    try:
        dest_column_idx = data[0].index(destination)
    except ValueError:
        raise ValueError('No such header for destination named: {}'.format(destination))
    try:
        src_column_idx = data[0].index(appendant)
    except ValueError:
        raise ValueError('No such header for appendant named: {}'.format(appendant))
    for index, row in enumerate(data[1:]):
        row[dest_column_idx] = row[dest_column_idx] + separator + row[src_column_idx]
        # cutting off headers so we need to go up 1 index
        data[index + 1] = row
    return data


def delete_column(data: list[list[str]], name: str) -> list[list[str]]:
    try:
        column_idx = data[0].index(name)
    except ValueError:
        raise ValueError('No such header to delete named: {}'.format(name))

    for index, row in enumerate(data):
        del row[column_idx]
        # data[index] = row

    return data


def concat_delete(data: list[list[str]], destination: str, deleted: str) -> list[list[str]]:
    return delete_column(concat(data, destination, deleted), deleted)
