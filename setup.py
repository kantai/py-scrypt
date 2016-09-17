#!/usr/bin/env python
from setuptools import setup, Extension

import sys
import platform

includes = []
library_dirs = []
extra_sources = []
CFLAGS = []


if sys.platform.startswith('linux'):
    define_macros = [('HAVE_CLOCK_GETTIME', '1'),
                     ('HAVE_LIBRT', '1'),
                     ('HAVE_POSIX_MEMALIGN', '1'),
                     ('HAVE_STRUCT_SYSINFO', '1'),
                     ('HAVE_STRUCT_SYSINFO_MEM_UNIT', '1'),
                     ('HAVE_STRUCT_SYSINFO_TOTALRAM', '1'),
                     ('HAVE_SYSINFO', '1'),
                     ('HAVE_SYS_SYSINFO_H', '1'),
                     ('_FILE_OFFSET_BITS', '64')]
    libraries = ['crypto', 'rt']
    CFLAGS.append('-O2')
elif sys.platform.startswith('win32'):
    define_macros = [('inline', '__inline')]
    libraries = ['libeay32', 'advapi32']
    extra_sources = ['scrypt-windows-stubs/gettimeofday.c']

    if platform.machine().endswith('64'):
        library_dirs = ['c:\OpenSSL-Win64\lib']
        includes = ['c:\OpenSSL-Win64\include', 'scrypt-windows-stubs/include']
    else:
        library_dirs = ['c:\OpenSSL-Win32\lib']
        includes = ['c:\OpenSSL-Win32\include', 'scrypt-windows-stubs/include']

elif sys.platform.startswith('darwin') and platform.mac_ver()[0] < '10.6':
    define_macros = [('HAVE_SYSCTL_HW_USERMEM', '1')]
    libraries = ['crypto']
else:
    define_macros = [('HAVE_POSIX_MEMALIGN', '1'),
                     ('HAVE_SYSCTL_HW_USERMEM', '1')]
    libraries = ['crypto']

scrypt_module = Extension(
    '_scrypt',
    sources=['src/scrypt.c',
             'scrypt-1.1.6/lib/crypto/crypto_aesctr.c',
             'scrypt-1.1.6/lib/crypto/crypto_scrypt-nosse.c',
             'scrypt-1.1.6/lib/crypto/sha256.c',
             'scrypt-1.1.6/lib/scryptenc/scryptenc.c',
             'scrypt-1.1.6/lib/scryptenc/scryptenc_cpuperf.c',
             'scrypt-1.1.6/lib/util/memlimit.c',
             'scrypt-1.1.6/lib/util/warn.c'] + extra_sources,
    include_dirs=['scrypt-1.1.6',
                  'scrypt-1.1.6/lib',
                  'scrypt-1.1.6/lib/scryptenc',
                  'scrypt-1.1.6/lib/crypto',
                  'scrypt-1.1.6/lib/util'] + includes,
    define_macros=[('HAVE_CONFIG_H', None)] + define_macros,
    extra_compile_args=CFLAGS,
    library_dirs=library_dirs,
    libraries=libraries)

setup(name='scrypt',
      version='0.7.1',
      description='Bindings for the scrypt key derivation function library',
      author='Magnus Hallin',
      author_email='mhallin@gmail.com',
      url='http://bitbucket.org/mhallin/py-scrypt',
      py_modules=['scrypt'],
      ext_modules=[scrypt_module],
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Topic :: Security :: Cryptography',
                   'Topic :: Software Development :: Libraries'],
      license='2-clause BSD',
      long_description=open('README.rst').read(),
      test_suite='tests.all_tests')
