#!/usr/bin/env pipenv-run

import sys

print("lol={}".format(sys.stdin.read().splitlines()))

print("ans=0")
print("exec(\"ans{}=0\".format(\"\".join(hex(ord(x)) for x in str(0))))")
print("while True:")
print("\tans=eval(\"ans{}\".format(lol[0]))")
print("\tprint((str(ans)+\"\\n\")[:eval(\"None if \\\"ans{}\\\" in locals() else 0\".format(\"\".join(hex(ord(x)) for x in str(ans)), \"\".join(hex(ord(x)) for x in str(ans))))], end=\"\")")
print("\texec(\"ans{}=1/ans{} if \\\"ans{}\\\" in locals() else 0\".format(\"\".join(hex(ord(x)) for x in str(ans)), \"\".join(hex(ord(x)) for x in str(ans)), \"\".join(hex(ord(x)) for x in str(ans))))")
print("\tlol=lol[1:]+lol[:1]")
