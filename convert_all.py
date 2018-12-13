import os
import random

import parse_svg as ps

if __name__ == '__main__':
    data_folder = 'svg'
    working_folder = 'working'
    done_folder = 'done'
    out_folder = 'out'
    current_folder = os.getcwd()

    while True:
        svg = None
        try:
            svg = random.choice(os.listdir(os.path.join(current_folder, data_folder)))
        except:
            break

        basename = os.path.splitext(os.path.basename(svg))[0]

        print(basename)

        working = os.path.join(current_folder, working_folder, basename + ".svg")
        done = os.path.join(current_folder, done_folder, basename + ".svg")
        out = os.path.join(current_folder, out_folder, basename)
        svg = os.path.join(current_folder, data_folder, basename + ".svg")

        os.rename(svg, working)

        if os.path.exists(out + ".obj"):
            print("\texists, skipping")
        else:
            ps.convert_svg(working, out)
        os.rename(working, done)
        print('-----------------\n\n')
