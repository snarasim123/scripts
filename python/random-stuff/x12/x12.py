import random
import sys
import tempfile
from itertools import groupby

import pyx12
from pyx12 import x12file, segment
from pyx12.segment import Segment


def simple_reader(testfile='test.x12'):
    src = pyx12.x12file.X12Reader(testfile)
    isa_id = src.get_isa_id()
    gs_id = src.get_gs_id()
    st_id = src.get_st_id()
    ls_id = src.get_ls_id()
    seg_count = src.get_seg_count()

    for k, g in groupby(get_headers_stream(src), lambda x: x[0]):
        print('-----------------------------------------------------------')
        values_list = []

        for d in g:
            values_list.clear()
            for n in d:
                if type(n) == dict:
                    for j in n.iterator():
                        values_list.append(j[3])
                if type(n) == Segment:
                    for j in n.values_iterator():
                        values_list.append(j[3])
                if type(n) == str:
                    values_list.append(n)
        print(k, values_list)
        # print('-----------------------------------------------------------')


# noinspection PyRedundantParentheses
def get_headers_stream(segments):
    """
    passed a segment enumerable
    yields ()
    """
    st_seg = None
    for seg_data in segments:
        seg_id = seg_data.get_seg_id()
        yield (seg_id, seg_data)


if __name__ == '__main__':
    simple_reader()
