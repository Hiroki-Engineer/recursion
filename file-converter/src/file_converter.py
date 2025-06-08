import sys

import markdown

from model import Args


def main() -> None:
    args = Args.from_argv(sys.argv)

    with args.inputfile.open("r") as f:
        content = f.read()

    html = markdown.markdown(content)

    with args.outputfile.open("w") as f:
        f.write(html)


if __name__ == "__main__":
    main()
