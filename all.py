#!/usr/bin/python3

import os
import sys
import gdb


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(script_dir)

# https://sourceware.org/gdb/current/onlinedocs/gdb.html/Writing-a-Pretty_002dPrinter.html
objfile = gdb.current_objfile() or gdb

import dns_name.pp
import dns_rdataclass.pp
import dns_rdatatype.pp
import isc_result.pp
import rbt.pp

dns_name.pp.register_printers(objfile)
dns_rdataclass.pp.register_printers(objfile)
dns_rdatatype.pp.register_printers(objfile)
isc_result.pp.register_printers(objfile)
rbt.pp.register_printers(objfile)
