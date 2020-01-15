from setuptools import setup

setup(
    name='svg2obj',
    version='0.1',
    author='Teseo Schneider',
    description='Convert SVG files to OBJ',
    url='https://github.com/teseoch/svg2obj',
    packages=['svgpathtools', 'svgpathtools.svgpathtools'],
    py_modules=['svg2obj', 'parse_svg', 'RationalBezier'],
    entry_points={
        'console_scripts': [
            'svg2obj = svg2obj:main',
        ],
    },
    install_requires=[
        'numpy',
        'svgwrite',
    ]
)
