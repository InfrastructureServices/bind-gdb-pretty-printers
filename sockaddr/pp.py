#!/usr/bin/env python
#
# Helper pretty printer for GDB. Prints nice and short struct sockaddr for common IPv4 and IPv6 families.

import os
import sys
import socket

def gdb_printer_decorator(fn):
    if __name__ == '__main__':
        gdb.pretty_printers.append(fn)
    return fn

def ntohs(port):
    return int.from_bytes(int(port).to_bytes(2, byteorder='big'), byteorder=sys.byteorder)

def ntohl(ip):
    return int.from_bytes(int(ip).to_bytes(4, byteorder='big'), byteorder=sys.byteorder)

def af_name(af):
    return socket.AddressFamily(int(af)).name


class SockaddrInPrinter(object):
    TYPE = 'struct sockaddr_in'

    def __init__(self, val):
        self.val = val

    def to_string(self):
        family = self.val['sin_family']
        if family != socket.AF_INET:
            return "! NOT sockaddr_in, but " + af_name(family)

        try:
            int_addr = int(self.val['sin_addr']['s_addr'])
            str_addr = socket.inet_ntop(family, int_addr.to_bytes(4, byteorder=sys.byteorder))
            port = ntohs(self.val['sin_port'])
            return f'INET{{{str_addr}:{port}}}'

        except Exception as e:
            errmsg = "! FormErr? %s %s" % (type(e), e)
            return errmsg

class SockaddrIn6Printer(object):
    TYPE = 'struct sockaddr_in6'

    def __init__(self, val):
        self.val = val

    def to_string(self):
        family = self.val['sin6_family']
        if family != socket.AF_INET6:
            return "! NOT sockaddr_in6, but " + af_name(family)

        try:
            byte_addr = self.val['sin6_addr'].bytes
            str_addr = socket.inet_ntop(family, byte_addr)
            scope_str = ''
            flow_str = ''
            port = ntohs(self.val['sin6_port'])
            flowid = ntohl(self.val['sin6_flowinfo'])
            scopeid = ntohl(self.val['sin6_scope_id'])
            if (flowid!=0):
                flow_str = f';flowid={flowid}'
            if scopeid != 0:
                scope_str = f'%{scopeid}'
            return f'INET6{{[{str_addr}{scope_str}]:{port}{flow_str}}}'

        except Exception as e:
            errmsg = "! FormErr? %s %s" % (type(e), e)
            return errmsg

class SockaddrPrinter(object):
    TYPE = 'struct sockaddr'

    def __init__(self, val):
        self.val = val

    def to_string(self):
        family = int(self.val['sa_family'])
        if family == socket.AF_INET:
            newtype = gdb.lookup_type(SockaddrInPrinter.TYPE)
            return SockaddrInPrinter(self.val.cast(newtype)).to_string()
        elif family == socket.AF_INET6:
            newtype = gdb.lookup_type(SockaddrIn6Printer.TYPE)
            return SockaddrIn6Printer(self.val.cast(newtype)).to_string()
        else:
            return '! UNSUPPORTED {0} AF {1}'.format(self.TYPE, af_name(family))



# register pretty printers
@gdb_printer_decorator
def sockaddr_in_printer(val):
    if str(val.type) == 'struct sockaddr_in' or str(val.type) == 'const struct sockaddr_in':
        return SockaddrInPrinter(val)
    elif str(val.type) == 'struct sockaddr_in6' or str(val.type) == 'const struct sockaddr_in6':
        return SockaddrIn6Printer(val)
    elif str(val.type) == SockaddrPrinter.TYPE or str(val.type) == 'const ' + SockaddrPrinter.TYPE:
        return SockaddrPrinter(val)
    return None

def register_printers(objfile):
    objfile.pretty_printers.append(sockaddr_in_printer)

