# Benchmark Functions for Optimization

Fast benchmarks for testing numerical optimization methods with Python interface.

This project provides a Python module with C++ implementations of benchmark functions for optimization.
These functions often are the most time-consuming part of evaluating new
optimization methods, so any improvements to this part help speed-up such
research.


## Quick Start

```python
import optobench as ob

xs = [.1, .2, .3, .4, .5]
print(ob.michalewicz(xs))


import numpy as np

nxs = np.array(xs)
print(ob.michalewicz(nxs))

nxss = np.array(
    [[0.4 , 0.31 , 0.445, 0.218, 0.581, 0.171, 0.532, 0.24 ],
    [0.265, 0.43 , 0.568, 0.144, 0.4  , 0.333, 0.188, 0.402],
    [0.191, 0.366, 0.234, 0.272, 0.307, 0.436, 0.203, 0.361],
    [0.262, 0.254, 0.407, 0.254, 0.254, 0.335, 0.169, 0.265],
    [0.362, 0.097, 0.167, 0.269, 0.395, 0.659, 0.234, 0.127]])
print(ob.michalewicz(nxss))
```

### Requirements

- Python 3.8
- numpy>=1.18
- g++ / clang with support for C++17


### Installation

```sh
# First, load your python environment

# Next
pip install optobench
```


#### From source
```sh
# First, load your python environment

# Next
make          # build loadable module in a local directory
make install  # build module and install in current environment
make test     # run tests
```


## List of functions

```
x ackley
x alpine
x bohachevsky1
x bohachevsky2
x bohachevsky3
x bukin_f6
x cross_in_tray
x dejong5
x eggholder
x gramacy_lee
x holder_table
x langermann
x levy
x levy13
x six_hump_camel_back
x deceptive3
x drop_wave
x easom
x penalty1
x griewank
x goldstein_price
x axis_parallel_hyperellipsoid
x rotated_hyperellipsoid
x sum_powers
x sum_squares # alias for axis_parallel_hyperellipsoid
x trid
x michalewicz
x perm0db
x permdb
x noncontinuous_rastrigin
x rastrigin
x parabola # alias for sphere
x rosenbrock
x schaffers_f2
x schaffers_f4
x schaffers_f6
x schwefels
x schwefels_p222
x shubert
x sphere
x step
x tripod
x trefethen4
x three_hump_camel_back
x dixon_price
x beale
x branin
x colville
x styblinski_tang
x powell
x shekel
x forrester
x hartmann_3d
x hartmann_4d
x hartmann_6d
x booth
x matyas
x mccormick
x power_sum
x zakharov
```

## Contributions

After forking the repo and cloning it locally, use `make && make test`.

`make test` runs the `testit.sh` script, which evaluates functions and dumps the result to `sanity-test-instance.log` file.
Next, that result is compared against golden results in `sanity-test-golden.log`.

When your changes are ready and golden data updated, submit a pull request.


## References

- [K.Voss 2016](https://harvest.usask.ca/handle/10388/7746)
    pythOPT: A problem-solving environment for optimization methods

- [Momin Jamil, Xin-She Yang 2013](https://arxiv.org/abs/1308.4008)
    A Literature Survey of Benchmark Functions For Global Optimization Problems

- [Optimization Test Problems, SFU](https://www.sfu.ca/~ssurjano/optimization.html)

- [Extending Python](https://docs.python.org/3/extending/extending.html)

- [C++ cmath](https://www.cplusplus.com/reference/cmath/)

- [CppCoreGuidelines](https://github.com/isocpp/CppCoreGuidelines/blob/master/CppCoreGuidelines.md)

- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
