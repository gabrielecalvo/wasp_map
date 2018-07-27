import os

get_test_fpath = lambda x: os.path.join(os.path.dirname(__file__), 'inputs', x)
get_tmp_fpath = lambda x: os.path.join(os.path.dirname(__file__), 'tmp', x)


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

if __name__ == '__main__':
    p=1
    o=3