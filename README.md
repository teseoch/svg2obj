# svg2obj

A simple script to convert any SVG into an obj (which contains the sampled paths as edges) and a JSON containing the curves.

Installation
------------

Clone this repository and remember to get the submodules!

```bash
git submodule update --init --recursive
```

The libary requires python 3 and:

- `numpy`
- `svgwrite`

Note: the aforementioned dependencies are all available trough conda.

Example
-------

run `python parse_svg.py file.svg out` to generate `out.obj` and `out.json`

The obj contains lines and the JSON has this format:

```
[
    {
        "v_ids": [ ... ],       list vertex ids mapping to the vertex id in the obj file
        "paras": [ ... ],       list of parametric values where to evaluate the curve to obtain the vertex positions (same length as v_ids)
        "curve_id": 0,          curve id, incremental
        "type": "BezierCurve",  type of the curve, can be BezierCurve, Line, and RationalBezier
        "degree": 3,            degree of the curve, 2 or 3
        "poles": [              list of control points in global coordinates
            [ 30.203, 9.331],
            [ 29.277, 9.509],
            [ 28.956, 11.307],
            [ 29.328, 11.8624]
        ]
    },
    ...
]
```
