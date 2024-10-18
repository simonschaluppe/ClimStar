def create_tilemap(colors, block_dictionary):
    tilemap = [
        (pos, colors[block.get_type_name()], block.blocktype)
        for pos, block in block_dictionary.items()
    ]
    return tilemap
