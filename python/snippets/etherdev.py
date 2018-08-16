
# ethernet devices & enumeration
# (linux specific ioctls used, warning)

from fcntl import ioctl as _ioctl
from array import array as _array
from weakref import ref as _weakref
import struct, errno as _errno

IF_NAMESIZE = 16

# ioctls
SIOCGIFNAME = 0x8910
SIOCGIFLINK = 0x8911
SIOCGIFCONF = 0x8912
SIOCGIFFLAGS = 0x8913
SIOCSIFFLAGS = 0x8914
SIOCGIFADDR = 0x8915
SIOCSIFADDR = 0x8916
SIOCGIFBRDADDR = 0x8919
SIOCSIFBRDADDR = 0x891a
SIOCGIFNETMASK = 0x891b
SIOCSIFNETMASK = 0x891c
SIOCGIFMETRIC = 0x891d
SIOCSIFMETRIC = 0x891e
SIOCGIFMTU = 0x8921
SIOCSIFMTU = 0x8922
SIOCGIFHWADDR = 0x8927
SIOCSIFHWADDR = 0x8924
SIOCGIFINDEX = 0x8933
SIOGIFINDEX = SIOCGIFINDEX

interface_flags = {
  0x1: 'UP',
  0x2: 'BROADCAST',
  0x4: 'DEBUG',
  0x8: 'LOOPBACK',
  0x10: 'P-t-P',
  0x20: 'NOTRAILERS',
  0x40: 'RUNNING',
  0x80: 'NOARP',
  0x100: 'PROMISC' }

def _import_with_metaclass (modname, metacls, *members):
    import inspect
    
    class MetaObject (object):
      __metaclass__ = metacls
    dct = {'__module__': modname}
    mod = __import__(modname)

    for k,v in mod.__dict__.items():
      if inspect.isclass(v) and getattr(v,'__module__','') == modname:
        try:
          setattr(mod, k, type(k,(v,MetaObject), dct))
        except TypeError:
          pass

    del dct,inspect

    if members:
      try:
        ml = []
        for m in members:
          ml.append(getattr(mod,m))
        return tuple(ml)
      except AttributeError:
        raise ImportError, m
    return mod

class AllowWeakrefMeta (type):
    def __init__ (cls, name, bases, dct):
      if dct.has_key('__slots__'):
        slots = dct['__slots__']
        if '__weakref__' not in slots:
          if isinstance(slots,list):
            slots.append('__weakref__')
          else:
            dct['__slots__'] = slots + ('__weakref__',)
      elif hasattr(cls,'__slots__'):
        slots = list(cls.__slots__)
        if '__weakref__' not in slots:
          slots.append('__weakref__')
          dct['__slots__'] = tuple(slots)

      super(AllowWeakrefMeta,cls).__init__(name,bases,dct)

_socket, _SocketType = _import_with_metaclass('socket',AllowWeakrefMeta, 
                                              'socket','SocketType')

class EthernetDevice (object):
    IFREQ_SIZE = IF_NAMESIZE + 16

    _struct_ifr_name = ('%ds' % IF_NAMESIZE)
    _struct_sockaddr = 'HHBBBB 8x'
    _struct_sockaddr_arpa = 'H 6B 8x'

    _struct_ifr_map = 'LLHBBB'
    _struct_ifr_flags = 'H'
    _struct_ifr_ifindex = 'i'
    _struct_ifr_metric = 'i'
    _struct_ifr_mtu = 'i'

    # sockaddr is 16 bytes (including padding)
    _struct_ifreq_data = (_struct_ifr_name + ('B' * 16))
    _struct_ifreq_addr = (_struct_ifr_name + _struct_sockaddr)
    _struct_ifreq_bcast = (_struct_ifr_name + _struct_sockaddr)
    _struct_ifreq_netmask = (_struct_ifr_name + _struct_sockaddr)
    _struct_ifreq_hwaddr = (_struct_ifr_name + _struct_sockaddr_arpa)
    _struct_ifreq_cidr = ('>' + _struct_ifr_name + 'HH L')
    
    # simple netmask calculation using bit-wise shift
    _netmasks = [((0xffffffffL << x) & 0xffffffffL) for x in range(33)]
    _netmasks.reverse()

    _ioctl_structs = {
      SIOCGIFNAME:  _struct_ifreq_data,
      SIOCGIFFLAGS: (_struct_ifr_name + _struct_ifr_flags),
      SIOCSIFFLAGS: (_struct_ifr_name + _struct_ifr_flags),
      SIOCGIFADDR: _struct_ifreq_addr,
      SIOCSIFADDR: _struct_ifreq_addr,
      SIOCGIFBRDADDR: _struct_ifreq_bcast,
      SIOCSIFBRDADDR: _struct_ifreq_bcast,
      SIOCGIFNETMASK: _struct_ifreq_netmask,
      SIOCSIFNETMASK: _struct_ifreq_netmask,
      SIOCGIFMETRIC: (_struct_ifr_name + _struct_ifr_metric),
      SIOCSIFMETRIC: (_struct_ifr_name + _struct_ifr_metric),
      SIOCGIFMTU: (_struct_ifr_name + _struct_ifr_mtu),
      SIOCSIFMTU: (_struct_ifr_name + _struct_ifr_mtu),
      SIOCGIFHWADDR: _struct_ifreq_hwaddr,
      SIOCSIFHWADDR: _struct_ifreq_hwaddr,
      SIOGIFINDEX: (_struct_ifr_name + _struct_ifr_ifindex)
    }

    def __init__ (self, name=None, ifreq_struct=None, sock=None):
      self.name = name
      if sock:
        self.sock = sock
      
      if ifreq_struct is not None:
        if isinstance(ifreq_struct,_array):
          ifreq_struct = ifreq_struct.tostring()
          
        ifreq = struct.unpack(self._struct_ifreq_addr, ifreq_struct)
        name = ifreq[0].rstrip('\0')

        if self.name is None and name:
          self.name = name
        self._address = '.'.join(map(str,ifreq[3:]))
      else:
        self._address = None
        if name:
          try:
            self.get_address()
          except IOError, e:
            if e.errno == _errno.ENODEV:
              raise IOError, '%s: ethernet device does not exist' % name
      del sock

    def get_address (self):
      if self._address is None:
        addr = self.ioctl(SIOCGIFADDR)[3:]
        self._address = '.'.join(map(str,addr))
      return self._address

    def get_broadcast (self):
      try:
        if self._broadcast:
          return self._broadcast
      except AttributeError:
        pass

      addr = self.ioctl(SIOCGIFBRDADDR)[3:]
      self._broadcast = '.'.join(map(str,addr))
      return self._broadcast

    def get_netmask (self):
      try:
        if self._netmask:
          return self._netmask
      except AttributeError:
        pass

      addr = self.ioctl(SIOCGIFNETMASK)[3:]
      self._netmask = '.'.join(map(str,addr))
      return self._netmask

    def get_wildcard (self):
      try:
        if self._wildcard:
          return self._wildcard
      except AttributeError:
        pass

      addr = self.ioctl(SIOCGIFNETMASK)[3:]
      self._wildcard = '.'.join(['%d' % (255^x) for x in addr])
      return self._wildcard

    def get_network (self):
      try:
        if self._network:
          return self._network
      except AttributeError:
        pass

      addr = self.ioctl(SIOCGIFBRDADDR)[3:]
      mask = self.ioctl(SIOCGIFNETMASK)[3:]
      net = [ 0, 0, 0, 0 ]
      for i in range(0, 4):
        net[i] = addr[i] ^ (255 ^ mask[i])
      self._network = '.'.join(['%d' % x for x in net])
      return self._network

    def get_cidr (self):
      try:
        if self._cidr:
          return self._cidr
      except AttributeError:
        pass

      netmask = self._ioctl(SIOCGIFNETMASK,self._struct_ifreq_cidr)[3]

      try:
        self._cidr = self._netmasks.index(netmask)
        # or self._netmasks[netmask] if using a dict
      except (IndexError, KeyError):
        # IndexError for list method, KeyError for dict
        raise ValueError, 'device has no valid netmask'
      return self._cidr

    def get_mac_address (self):
      try:
        if self._hwaddr:
          return self._hwaddr
      except AttributeError:
        pass

      addr = self.ioctl(SIOCGIFHWADDR)[2:]
      self._hwaddr = ':'.join(['%02x' % x for x in addr])
      return self._hwaddr

    def get_flags (self):
      flags = self.ioctl(SIOCGIFFLAGS)[1:]

      fl = []
      if flags:
        flags = flags[0]
        for fbits in interface_flags:
          if (flags & fbits) != 0:
            fl.append(interface_flags[fbits])

      return tuple(fl)

    def has_flags (self, flag):
      if not hasattr(self,'_flags'):
        self._flags = self.get_flags()

      return (flag.upper() in self._flags)

    def bound_socket (self, socktype, port=0, proto=None):
      '''Returns a new socket bound to the network device represented
      by the EthernetDevice object.
      '''
      from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
      
      lookup = { 'tcp': SOCK_STREAM, 'udp': SOCK_DGRAM }
      if isinstance(socktype,basestring):
        try:
          socktype = lookup[socktype.lower()]
        except KeyError:
          raise ValueError, 'unknown socket type: %s' % repr(socktype)

      if proto:
        self.sock = s = _socket(AF_INET, socktype, proto)
      else:
        self.sock = s = _socket(AF_INET, socktype)

      s.bind((self.get_address(), port))
      return s
    
    def __repr__ (self):
      try:
        if self.name and self._address:
          s = '%s:%s' % (self.name, self._address)
          if hasattr(self,'_hwaddr'):
            s += ' [%s]' % self._hwaddr
      except AttributeError:
        return super(EthernetDevice,self).__repr__()
      return s

    def _ioctl (self, op, fmt, *args):
      if struct.calcsize(fmt) < self.IFREQ_SIZE:
        fmt += ('%dx' % (self.IFREQ_SIZE - struct.calcsize(fmt)))

      if args and isinstance(args[0], basestring):
        args = args[1:]

      if not args:
        args = struct.unpack(fmt,_array('B', '\0' * self.IFREQ_SIZE))[1:]

      data = _array('B',struct.pack(fmt,self.name,*args))

      r = _ioctl(self.sock, op, data, True)
      if r != 0:
        raise IOError, 'ioctl(%d) failed: %d' % (op,r)

      return struct.unpack(fmt,data.tostring())

    def ioctl (self, op, *args):
      if not self._ioctl_structs.has_key(op):
        raise ValueError, 'ioctl(%s) is not supported' % str(op)
     
      return self._ioctl(op, self._ioctl_structs[op], *args)

    def __getsocket (self):
      from socket import AF_INET, SOCK_DGRAM
      try:
        wr = self.__sockref
      except AttributeError:
        s = _socket(AF_INET, SOCK_DGRAM)
        self.__sockref = _weakref(s)
      except:
        raise
      else:
        s = wr()
        if s is None:
          s = _socket(AF_INET, SOCK_DGRAM)
          self.__sockref = _weakref(s)
        del wr
      return s

    def __setsocket (self, s):
      self.__sockref = _weakref(s)

    def __delsocket (self):
      del self.__sockref

    sock = property(__getsocket, __setsocket, __delsocket)

def enumerate_devices (inactive=False):
    '''Returns an iterator over all active ('UP') ethernet devices in
    the form of EthernetDevice objects.  If the 'inactive' keyword
    evaluates to a true value, inactive devices are included.
    '''
    from socket import AF_INET, SOCK_DGRAM
    s = _socket(AF_INET, SOCK_DGRAM)

    bufsize = 1024
    buf = _array('B', '\0' * bufsize)
    bufptr = buf.buffer_info()[0]

    ifconf = _array('B',struct.pack('iP', bufsize, bufptr))
    
    if _ioctl(s.fileno(),SIOCGIFCONF,ifconf,True) == 0:
      l,bufptr = struct.unpack('iP',ifconf.tostring())
      size = EthernetDevice.IFREQ_SIZE
      fmt = EthernetDevice._struct_ifreq_addr
      while l >= size:
        intf = buf[:size].tostring()
        dev = EthernetDevice(ifreq_struct=intf, sock=s)
        if inactive or dev.has_flags('UP'):
          yield dev
        del dev
        l -= size
        del buf[:size]

    del s, buf, ifconf

def get_device (devname):
    '''Convenience function that returns an EthernetDevice object for the
    device named 'devname'.  If no such device exists, IOError is raised.
    '''
    return EthernetDevice(devname)

