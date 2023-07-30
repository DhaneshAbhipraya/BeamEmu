from argparse import ArgumentParser
import os.path as path
from time import perf_counter as pc


def main():
    args = parseargs()
    try:
        nargs = normargs(args)
        if args[2]:
            print(f"Normalize args: {nargs}")
        aargs = validateargs(nargs)
        if args[2]:
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
    parser.add_argument(
        '-vs', '--verbose-short', help="Output short verbose info", dest="_verbose_short_", action="store_true")

    args = parser.parse_args()

    return [args._if_, args._of_, args._verbose_ or args._verbose_short_, args._verbose_short_]


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


def start_asm(ifile, ofile, verbose, verbose_short):
    print(f"Assembling {path.basename(ifile)} to {path.basename(ofile)}...")
    start = pc()
    if verbose:
        print("create trtab"if verbose_short else"Creating translation tables...", end=' | ')
    if verbose:
        print("create trtabinst"if verbose_short else"Creating translation table for instructions...", end=' | ')
    if verbose:
        print("create trtabinst>const"if verbose_short else"Creating translation table for instructions > constants...", end=' | ')
    LABEL = 0
    VALUE = 1
    REGISTER = 2
    if verbose:
        print("create trtabinst>table"if verbose_short else"Creating translation table for instructions > table...", end=' | ')
    trtabinst = {
        "nop": [b'\x00', []],
        "jmp": [b'\x01', [LABEL]],
        "mov": [b'\x02', [REGISTER, VALUE]],
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
    if verbose:
        print("create trtabreg"if verbose_short else"Creating translation table for registers...", end=' | ')
    trtabreg = {
        "eax": 0x00,
        "ebx": 0x01,
        "ecx": 0x02,
        "edx": 0x02,
    }
    if verbose:
        print("create labels"if verbose_short else"Creating label map...", end=' | ')
    labels = {}

    out = b''

    with open(ifile, 'r') as i:
        if verbose:
            print("read source"if verbose_short else"Reading source...", end=' | ')
        source = i.read()

    for _line in enumerate(source.split('\n')):
        line = _line[1].strip()
        tokens = line.split()
        if tokens[0].endswith(':'):
            labels.update({tokens[0].removesuffix(':'): _line[0]})
    for _line in source.split('\n'):
        line = _line.strip()
        tokens = line.split()
        if tokens[0].endswith(':'):
            continue
        if len(tokens) < 1:
            continue
        out += trtabinst[tokens[0]][0]
        args = trtabinst[tokens[0]][1]
        for arg in enumerate(args):
            toadd = None
            if arg[1] == VALUE:
                if tokens[arg[0]+1] in trtabreg:
                    toadd = trtabreg[tokens[arg[0]+1]].to_bytes(1, "little")
                else:
                    lit = tokens[arg[0]+1]
                    if tokens[arg[0]+1].startswith('0x'):
                        lit = tokens[arg[0]+1].removeprefix('0x')
                    toadd = int(lit).to_bytes(2, "little")
                    if tokens[arg[0]+1].startswith('0x'):
                        int(lit).real
            if arg[1] == LABEL:
                toadd = int(labels[tokens[arg[0]+1]]).to_bytes(2, 'little')

            if toadd:
                out += toadd

    with open(ofile, 'wb') as o:
        if verbose:
            print("write bin"if verbose_short else"Writing binary...", end=' | ')
        o.write(out)

    print("done\nAssembled in {:.3}ms".format((pc() - start) * 1000))


if __name__ == "__main__":
    main()
