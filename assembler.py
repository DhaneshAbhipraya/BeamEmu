from argparse import ArgumentParser
import os.path as path


def main():
    args = parseargs()
    try:
        nargs = normargs(args)
        print(f"Normalize args: {nargs}")
        aargs = validateargs(nargs)
        print(f"Validated args: {aargs}")
    except Exception as e:
        print("Error when parsing args." +
              (" Rerun using `-v` to see what was wrong" if not args[2] else ""))
        if args[2]:
            print(f"Error: {e}")
        exit()
    start_asm(*aargs)


def parseargs():
    parser = ArgumentParser()
    parser.add_argument(
        '-if', help="Input file to be assembled; should be a .asm", dest="_if_", required=True)
    parser.add_argument(
        '-of', help="Output file after being assembled; should be a `.bin`, or `!` to use the same file with the .bin file extension [Default: `!`]", dest="_of_", default="!")
    parser.add_argument(
        '-v', '--verbose', help="Output verbose info", dest="_verbose_", action="store_true")

    args = parser.parse_args()

    return [args._if_, args._of_, args._verbose_]


def normargs(args):
    if args[2]:
        print("Normalizing arguments...")
    if args[1] == '!':
        args[1] = path.splitext(args[0])[0]+'.bin'
    return args


def validateargs(args):
    if args[2]:
        print("Validating arguments...")
    v1 = path.exists(args[0]) and not path.isdir(
        args[0]) and path.splitext(args[0])[1] == '.asm'
    if args[2]:
        print(f"-if {'in' if not v1 else ''}validated")
    v2 = path.splitext(args[1])[1] == '.bin'
    if args[2]:
        print(f"-of {'in' if not v2 else ''}validated")
    validation = v1 & v2
    if not validation:
        raise ValueError("Arguments invalidated!")
    return args


def start_asm(ifile, ofile, verbose):
    print(f"Assembling {path.basename(ifile)} to {path.basename(ofile)}...")

    with open(ifile, 'r') as i:
        if verbose:
            print("Reading source...")
        source = i.read()

    with open(ofile, 'wb') as o:
        if verbose:
            print("Writing binary...")
        o.write(b'\x00\x00')


if __name__ == "__main__":
    main()
