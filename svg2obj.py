from parse_svg import convert_svg, parse_args


def main():
    args = parse_args()
    convert_svg(args.image, args.output)


if __name__ == '__main__':
    main()
