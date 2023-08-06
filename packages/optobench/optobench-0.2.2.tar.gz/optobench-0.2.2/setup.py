# import sysconfig
from distutils.core import setup, Extension

try:
    import numpy as np
    numpy_include_dir = np.get_include()
except ImportError:
    numpy_include_dir = '/usr/lib/python3/dist-packages/numpy/core/include'

# extra_compile_args = sysconfig.get_config_var('CXXFLAGS').split()
extra_compile_args = []
extra_compile_args += ['-std=c++17', '-Wall', '-Wextra']
extra_link_args = []
optobench_module = Extension('optobench',
    ['cbench.cc', 'bss.cc'],
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    include_dirs=[numpy_include_dir],
    libraries=['stdc++'],
    language='c++17'
)


CLASSIFIERS = """\
Development Status :: 2 - Pre-Alpha
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Programming Language :: C++
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Topic :: Software Development :: Libraries
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Artificial Intelligence
Topic :: Scientific/Engineering :: Mathematics
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: POSIX :: Linux
Operating System :: Unix
Operating System :: MacOS
"""


def get_long_description():
  description = ''
  with open('README.md', 'rt') as fd:
      description = fd.read()
  return description


def get_requirements():
  reqs = ''
  with open('requirements.txt', 'rt') as fd:
      reqs = fd.readlines()
  return reqs


setup(name='optobench',
      version='0.2.2',
      author='K. Voss',
      author_email='k.voss@usask.ca',
      url='https://github.com/kvoss/optobench',
      download_url='https://github.com/kvoss/optobench/releases',
      license='BSD 3-Clause License',
      description='Benchmark Functions for Optimization',
      long_description=get_long_description(),
      long_description_content_type='text/markdown',
      keywords='optimization benchmark',
      classifiers=[cs for cs in CLASSIFIERS.split('\n') if cs],
      platforms=['Windows', 'Linux', 'Solaris', 'Mac OS-X', 'Unix'],
      install_requires=get_requirements(),
      python_requires='>=3.6',
      ext_modules=[optobench_module]
)
