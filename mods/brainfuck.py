from StringIO import StringIO
import sys,io

from pybrainfuck import BrainFck

a=io.BytesIO("++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.+++.")

fo=StringIO()
bfck = BrainFck(fout=fo)
bfck.run(a)
out="".join(fo.buflist).strip("\n\r")






