import svgpathtools.svgpathtools as svg
import json
import argparse


SAMPLE_MAX_DEPTH = 5
SAMPLE_ERROR = 1e-3


def complex_to_point(p, trafo):
    return [p.real, p.imag]


def complex_to_vect(p, trafo):
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

    if ((abs(length2 - length) > error) and (length2 - length)/length > error) and (depth <= max_depth):
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
        trafo = tmp.transform
        path = tmp.path

        print(str(ii+1) + "/" + str(len(paths)) + " n sub paths: " + str(len(path)))

        xx = 0
        for piece in path:
            # length = piece.length()
            # n_samples = min(max(2, int(round(length)/5)),10000)
            # print(xx, piece)
            xx += 1

            # ts = np.linspace(0, 1, n_samples)
            ts = compute_samples(piece)

            if len(ts) <= 0:
                continue

            # print(xx, len(ts))
            param_ts = []
            # print(piece)

            iprev = None

            for param_t in ts:
                # param_t = piece.ilength(t)
                param_ts.append(param_t)
                p = piece.point(param_t)
                xy = complex_to_point(p, trafo)

                if not iprev:
                    istart = v_index

                # if xy[1] < -1000000:
                #     asd
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
                json_obj["start"] = complex_to_point(piece.start, trafo)
                json_obj["end"] = complex_to_point(piece.end, trafo)

                is_set = True
            elif isinstance(piece, svg.path.QuadraticBezier):
                json_obj["type"] = "BezierCurve"
                json_obj["degree"] = 2

                json_obj["poles"] = [complex_to_point(piece.start, trafo), complex_to_point(piece.control, trafo), complex_to_point(piece.end, trafo)]

                is_set = True
            elif isinstance(piece, svg.path.CubicBezier):
                json_obj["type"] = "BezierCurve"
                json_obj["degree"] = 3
                json_obj["poles"] = [complex_to_point(piece.start, trafo), complex_to_point(piece.control1, trafo), complex_to_point(piece.control2, trafo), complex_to_point(piece.end, trafo)]

                is_set = True
            elif isinstance(piece, svg.path.Arc):
                json_obj["type"] = "Arc"
                json_obj["theta"] = piece.theta
                json_obj["delta"] = piece.delta
                json_obj["rot_matrix"] = complex_to_point(piece.rot_matrix, None)
                json_obj["radius"] = complex_to_vect(piece.radius, trafo)
                json_obj["center"] = complex_to_point(piece.center, trafo)

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
