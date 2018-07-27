import textwrap
from wasp_map import *
from tests import get_test_fpath, get_tmp_fpath, clean_tmp_files


def test_map_from_file():
    fpath_in = get_test_fpath('tst.map')
    wmap = WAsP_Map.from_file(fpath_in)

    assert len(wmap.lines) == 3


def test_map__get_map_string():
    fpath_in = get_test_fpath('tst.map')
    wmap = WAsP_Map.from_file(fpath_in)

    assert wmap._get_map_string() == textwrap.dedent("""\
        + | UTM Z31 WGS-8|WME ver. 11.21.11.28
           0.000000   0.000000   0.000000   0.000000
           1.000000   0.000000   1.000000   0.000000
           1.000000   0.000000
            0.03       0.0        4
             951617.8    5135044.0    951615.4    5135075.0    951658.3    5135078.0    951617.8    5135044.0
            0.05       1.0        200.0      4
             943059.2    5124845.5    943096.6    5124787.0    943071.1    5124692.5    943059.2    5124678.0
            2390.0     2
             956638.0    5139374.0    956644.7    5139386.0
        """)


def test_map_roundtrip():
    fpath_in = get_test_fpath('tst.map')
    fpath_out = get_tmp_fpath('tst2.map')

    wmap = WAsP_Map.from_file(fpath_in)
    wmap.save(fpath_out)
    wmap2 = WAsP_Map.from_file(fpath_out)

    assert wmap == wmap2

    clean_tmp_files('tst2.map')


def test_map_extent():
    fpath_in = get_test_fpath('tst.map')
    wmap = WAsP_Map.from_file(fpath_in)

    assert wmap.extent.min_x == 943059.2
    assert wmap.extent.max_x == 956644.7
    assert wmap.extent.min_y == 5124678.0
    assert wmap.extent.max_y == 5139386.0


def test_map_save_partials_only():
    fpath_in = get_test_fpath('tst.map')
    fpath_out = get_tmp_fpath('tst2.map')
    wmap = WAsP_Map.from_file(fpath_in)

    wmap.save(fpath_out, elevation=False)
    wmap2 = WAsP_Map.from_file(fpath_out)
    assert len(wmap2.lines) == 2
    assert wmap2.lines[0].elev is None
    assert wmap2.lines[1].elev is None

    wmap.save(fpath_out, roughness=False)
    wmap2 = WAsP_Map.from_file(fpath_out)
    assert len(wmap2.lines) == 2
    assert wmap2.lines[0].r_left is None
    assert wmap2.lines[1].r_left is None

    clean_tmp_files('tst2.map')
