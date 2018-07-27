import os

get_test_fpath = lambda x: os.path.join(os.path.dirname(__file__), 'inputs', x)
get_tmp_fpath = lambda x='': os.path.join(os.path.dirname(__file__), 'tmp', x)
if not os.path.isdir(get_tmp_fpath()): os.mkdir(get_tmp_fpath())

def clean_tmp_files(*fnames):
    """
    Deletes the file specified in the tmp folder
    Usage: clean_tmp_files('file1.txt', 'file2.txt')
    """
    # check all files are in tmp folder before starting deleting any
    for fname in fnames:
        assert os.path.isfile(get_tmp_fpath(fname))

    for fname in fnames:
        fpath = get_tmp_fpath(fname)
        os.remove(fpath)
