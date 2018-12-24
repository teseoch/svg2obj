import svgpathtools.svgpathtools as svg
import json
import argparse
import RationalBezier as rb


SAMPLE_MAX_DEPTH = 5
SAMPLE_ERROR = 1e-3


def complex_to_point(p):
    return [p.real, p.imag]


def complex_to_vect(p):
    return [p.real, p.imag]


def compute_samples(curve, start=0, end=1, error=SAMPLE_ERROR, max_depth=SAMPLE_MAX_DEPTH, depth=0):
    return compute_samples_aux(curve, 0, 1, curve.point(start), curve.point(end), error, max_depth, depth)


def compute_samples_aux(curve, start, end, start_point, end_point, error, max_depth, depth):
    """Recursively approximates the length by straight lines"""
    mid = (start + end)/2
    mid_point = curve.point(mid)
    length = abs(end_point - start_point)
    first_half = abs(mid_point - start_point)
    second_half = abs(end_point - mid_point)


    length2 = first_half + second_half

    res = [start, mid, end]

    if abs(length) < 1e-10:
        return []

    if (abs(length2 - length) > error) and (depth <= max_depth):
        depth += 1
        res1 = compute_samples_aux(curve, start, mid, start_point, mid_point, error, max_depth, depth)
        res2 = compute_samples_aux(curve, mid, end, mid_point, end_point, error, max_depth, depth)
        return sorted(set(res1 + res2))
    else:
        # This is accurate enough.
        return res


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("image",  type=str, help="path to the input svg image")
    parser.add_argument("output", type=str, help="path to the output file without extension")
    return parser.parse_args()


def convert_svg(input_svg, output):
    doc = svg.Document(input_svg)
    paths = doc.flatten_all_paths()

    vertices = ""
    lines = ""
    json_data = []

    v_index = 1
    c_index = 0
    for ii in range(len(paths)):
        tmp = paths[ii]
        path = tmp.path

        print(str(ii+1) + "/" + str(len(paths)) + " n sub paths: " + str(len(path)))

        for pieces in path:
            if isinstance(pieces, svg.path.Arc):
                if abs(abs(pieces.delta)-180) < 1e-5:
                    pieces = [rb.RationalBezier(pieces, tstart=0, tend=0.5), rb.RationalBezier(pieces, tstart=0.5, tend=1)]
                else:
                    pieces = [rb.RationalBezier(pieces)]
            else:
                pieces = [pieces]

            for piece in pieces:
                ts = compute_samples(piece)

                if len(ts) <= 0:
                    continue


                param_ts = []

                iprev = None

                for param_t in ts:
                    param_ts.append(param_t)
                    p = piece.point(param_t)
                    xy = complex_to_point(p)

                    if not iprev:
                        istart = v_index

                    vertices += "v " + str(xy[0]) + " " + str(xy[1]) + " 0\n"

                    if iprev:
                        lines += "l " + str(iprev) + " " + str(v_index) + "\n"

                    iprev = v_index

                    v_index += 1

                json_obj = {}
                json_obj["v_ids"] = list(range(istart-1, v_index-1))
                istart = None
                json_obj["paras"] = param_ts
                json_obj["curve_id"] = c_index
                c_index += 1

                is_set = False

                if isinstance(piece, svg.path.Line):
                    json_obj["type"] = "Line"
                    json_obj["start"] = complex_to_point(piece.start)
                    json_obj["end"] = complex_to_point(piece.end)

                    is_set = True
                elif isinstance(piece, svg.path.QuadraticBezier):
                    json_obj["type"] = "BezierCurve"
                    json_obj["degree"] = 2

                    json_obj["poles"] = [complex_to_point(piece.start), complex_to_point(piece.control), complex_to_point(piece.end)]

                    is_set = True
                elif isinstance(piece, svg.path.CubicBezier):
                    json_obj["type"] = "BezierCurve"
                    json_obj["degree"] = 3
                    json_obj["poles"] = [complex_to_point(piece.start), complex_to_point(piece.control1), complex_to_point(piece.control2), complex_to_point(piece.end)]

                    is_set = True
                elif isinstance(piece, rb.RationalBezier):
                    json_obj["type"] = "RationalBezier"
                    json_obj["poles"] = [complex_to_point(piece.start), complex_to_point(piece.control), complex_to_point(piece.end)]
                    json_obj["weigths"] = [piece.weights[0], piece.weights[1], piece.weights[2]]

                    is_set = True

                if is_set:
                    json_data.append(json_obj)
                else:
                    print(type(piece))
                    print(piece)
                    assert(False)

        lines += "\n"


    with open(output + ".obj", "w") as file:
        file.write(vertices)
        file.write(lines)

    with open(output + ".json", "w") as file:
        file.write(json.dumps(json_data, indent=4))


if __name__ == '__main__':
    args = parse_args()
    convert_svg(args.image, args.output)
