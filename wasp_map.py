def parse_wasp_map(fpath):
    """Reads and parses the WAsP map into """
    with open(fpath, 'r') as f: 
        content = f.readlines()

    lines = []
    metadata_dict = {}
    pairs_to_next_metadata_line = 0

    header = ''.join(content[:4])
    for l in content[4:]:
        if pairs_to_next_metadata_line == 0:
            if metadata_dict: lines.append(metadata_dict)
            metadata = l.split()
            metadata_dict = {'n_points': float(metadata.pop()), 'pairs':[]}
            if len(metadata) > 1:
                metadata_dict['r_left'] = float(metadata.pop(0))
                metadata_dict['r_right'] = float(metadata.pop(0))
            if metadata: 
                metadata_dict['elev'] = float(metadata.pop(0))
            assert not metadata  # nothing left
            pairs_to_next_metadata_line = metadata_dict['n_points']
        else:
            coords = l.split()
            pairs = [(float(i),float(j)) for i,j in zip(coords[::2], coords[1::2])]
            metadata_dict['pairs'].extend(pairs)
            pairs_to_next_metadata_line -= len(pairs)

    if metadata_dict: lines.append(metadata_dict)
        
    return header, lines
