import argparse
import json


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("json",  type=str, help="path to the input json file")
    parser.add_argument("output", type=str, help="path to the output geo file")
    return parser.parse_args()


def convert_json(json_file, out_file):
    with open(json_file, 'r') as f:
        json_data = json.load(f)

    points = ""
    curves = ""

    point_index = 1
    curve_index = 1
    for curve in json_data:
        if curve["type"] == "BezierCurve":
            for pole in curve["poles"]:
                points += "//+\n"
                points += "Point({}) = {{{}, {}, 0, 1.0}};\n".format(point_index, pole[0], pole[1])
                point_index += 1

            curves += "//+\n"
            if curve["degree"] == 3:
                curves += "Bezier({}) = {{{}, {}, {}, {}}};\n".format(curve_index, point_index-4, point_index-3, point_index-2, point_index-1)
            else:
                curves += "Bezier({}) = {{{}, {}, {}};\n".format(curve_index, point_index-3, point_index-2, point_index-1)
            curve_index += 1

        # print(curve)


    with open(out_file, 'w') as f:
        f.write(points)
        f.write(curves)
        f.write("//+\nCoherence;")


if __name__ == '__main__':
    args = parse_args()
    convert_json(args.json, args.output)
