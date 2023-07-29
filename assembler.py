from argparse import ArgumentParser
import os.path as path
from time import perf_counter as pc


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
    start = pc()
    if verbose:
        print("Creating translation tables...")
    if verbose:
        print("Creating translation table for instructions...")
    if verbose:
        print("Creating translation table for instructions > constants...")
    LABEL = 0
    VALUE = 1
    REGISTER = 2
    if verbose:
        print("Creating translation table for instructions > table...")
    trtabinst = {
        "nop": [b'\x00', []],
        "jmp": [b'\x01', [LABEL]],
        "mov": [b'\x02', [VALUE, REGISTER]],
        "inc": [b'\x03', [REGISTER]],
        "dec": [b'\x04', [REGISTER]],
        "add": [b'\x05', [REGISTER, VALUE]],
        "sub": [b'\x06', [REGISTER, VALUE]],
        "mul": [b'\x07', [REGISTER, VALUE]],
        "div": [b'\x08', [REGISTER, VALUE]],
        "cmp": [b'\x09', [VALUE, VALUE]],
        "je":  [b'\x0a', [LABEL]],
        "jne": [b'\x0b', [LABEL]],
        "jz":  [b'\x0c', [LABEL]],
        "jnz": [b'\x0d', [LABEL]],
        "jl":  [b'\x0e', [LABEL]],
        "jg":  [b'\x0f', [LABEL]],
        "jnl": [b'\x10', [LABEL]],
        "jng": [b'\x11', [LABEL]],
        "out": [b'\x12', [VALUE]],
    }

    out = b''

    with open(ifile, 'r') as i:
        if verbose:
            print("Reading source...")
        source = i.read()

    for line in source.split('\n'):
        tokens = line.split()
        out += trtabinst[tokens[0]][0]
        args = trtabinst[tokens[0]][1]
        for arg in enumerate(args):
            if arg[1] == VALUE:
                out += int(tokens[arg[1]]).to_bytes()

    with open(ofile, 'wb') as o:
        if verbose:
            print("Writing binary...")
        o.write(out)

    print("Assembled in {:.3}ms".format((pc() - start) * 1000))


if __name__ == "__main__":
    main()
