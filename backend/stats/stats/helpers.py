from itertools import islice, chain


def chunks(iterable, size: int):
    '''
    Split source iterator by chunks.

    :param iterable: Any iterable sequence
    :param size: Size of chunk
    '''
    i = iter(iterable)
    while True:
        b = islice(i, size)
        yield chain([next(b)], b)
