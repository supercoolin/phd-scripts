import argparse as ap
from os.path import join as pjoin
import sys
from random import choice, randint
"""
//Example of code that avoids gcc optimizations, increasing the size of r's
//computation increases the length of the function

static int a[3] = {1, 2, 3};
static int b[3] = {4, 5, 6};
static int r[3] = {0, 0, 0};


void table_tamper() {
    for (int i = 0; i < 3; i++) {
        a[i]++;
        b[i]++;
        r[i]++;
    }
}
int f0(){
    r[0] = a[0] + b[0];
    r[1] = r[0] + a[1] + b[1];
    r[2] = r[1] + a[2] + b[2];
    return r[0] * r[1] * r[2];
}
"""
def _append_loc(code: str, loc: str):
    return code + f"{loc}\n"
    
def gen_headers()->str:
    return ""

def gen_globals(code: str, length: int)->str:
    code = _append_loc(code, f"int a[{length}] = {{" + ",".join([str(1 + i) for i in range(length)]) + "};")
    code = _append_loc(code, f"float b[{length}] = {{" + ",".join([str(1 + length + i) + ".0" for i in range(length)]) + "};")
    code = _append_loc(code, f"float r[{length}] = {{" + ",".join(["0.0" for i in range(length)]) + "};")
    return code

def gen_tampering_code(code: str, length: int) -> str:
    return code + f"""    void table_tamper() {{
        for (int i = 0; i < {length}; i++) {{
            a[i]++;
            b[i]++;
            r[i]++;
        }}
    }}\n"""


def gen_cache_killing_function(code: str, length: int) -> str:
    code = _append_loc(code, "int f0() {")
    code = _append_loc(code,    "r[0] = a[0] + b[0];")
    for i in range(1, length):
        code = _append_loc(code, f"r[{i}] = a[{randint(0, length - 1)}] {choice(['+', '*', '-', '/'])} b[{randint(0, length - 1)}];")
    code = _append_loc(code, f"return {'+'.join([f'r[{i}]' for i in range(length)])};")
    code = _append_loc(code, "}")
    return code


def gen_code(length: int) -> str:
    code = gen_headers()
    code = gen_globals(code, length)
    code = gen_tampering_code(code, length)
    code = gen_cache_killing_function(code, length)
    return code

def main():
    print(gen_code(size))


if __name__ == '__main__':
    size = int(sys.argv[1])
    main()