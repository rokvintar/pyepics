"""
   epics python module
   Matthew Newville <newville@cars.uchicago.edu>
   CARS, University of Chicago

   version    :  2.99.0 (working toward 3.0)
   last update:  18-Jan-2010
         
== Overview:
   rewrite of EpicsCA v 2.*, with major goals of:
      a) replacing swig interface with ctypes
      b) better support for thread safety
      c) more complete low-level support to epics channel access interface
      
      
   major classes will be:
      PV -- Process Variable which will work largely as in EpicsCA 2.*
"""


__version__ = '3.0.1'

import time
import ca
import dbr
import pv
import alarm

PV = pv.PV
poll = ca.poll

def __createPV(pvname,timeout=5.0):
    "create PV, wait for connection: "

    t0 = time.time()
    thispv = PV(pvname,use_cache=False)
    if not thispv.connected:
        thispv.connect()
    while not thispv.connected:
        time.sleep(0.001)
        ca.poll()
        if time.time()-t0 > timeout: break
    if not thispv.connected:
        print 'cannot connect to %s' % pvname
        return None

    return thispv

def caput(pvname, value, wait=False, timeout=60):
    """caput(pvname, value, wait=False, timeout=60)
    simple put to a pv's value.
       >>> caput('xx.VAL',3.0)

    to wait for pv to complete processing, use 'wait=True':
       >>> caput('xx.VAL',3.0,wait=True)
    """ 
    pv = __createPV(pvname,timeout=10.0)
    if pv is not None:
        ret = pv.put(value,wait=wait,timeout=timeout)
        ca.poll()
        return ret

def caget(pvname, use_char=False):
    """caget(pvname, use_char=False)
    simple get of a pv's value..
       >>> x = caget('xx.VAL')

    to get the character string representation (formatted double, enum string, etc):
       >>> x = caget('xx.VAL', use_char=True)
    """
    pv = __createPV(pvname,timeout=10.0)
    if pv is not None:
        val = pv.get()
        ca.poll()
        if use_char: return pv.char_value
        return val

def cainfo(pvname,noprint=False):
    """cainfo(pvname,noprint=False)

    print information about pv
       >>>cainfo('xx.VAL')

    will print out a status report for the pv.  If True, the optional  'noprint' flag
    will NOT print the status report, but return the paragraph as a string.
    """
    pv = __createPV(pvname,timeout=10.0)
    if pv is not None:
        info = pv.get_info()
        if noprint: return info
        print info
        return None
    