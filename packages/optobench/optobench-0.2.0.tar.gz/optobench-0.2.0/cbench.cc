#define PY_SSIZE_T_CLEAN  /* Make "s#" use Py_ssize_t rather than int. */
#include "Python.h"
#include <stdexcept>

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include "numpy/arrayobject.h"
// #include "numpy/arrayscalars.h"

#include "bss.h"

static PyObject *
handle_list(PyObject *lst, double (*fun)(const std::vector<double>&))
{
    Py_ssize_t len = PyList_Size(lst);
    if (len < 1) {
        PyErr_SetString(PyExc_ValueError, "Expected a list of length >=1");
        return NULL;
    }

    std::vector<double> xs;
    xs.reserve(len);
    for (Py_ssize_t idx = 0; idx < len; ++idx) {
        PyObject *px = PyList_GetItem(lst, idx);
        double d = PyFloat_AsDouble(px);
        xs.push_back(d);
    }
    try {
        double ret = fun(xs);
        PyObject *v = PyFloat_FromDouble(ret);
        return v;
    } catch (const std::out_of_range& e) {
        PyErr_SetString(PyExc_ValueError, "invalid argument: check minimal vector size");
    } catch ( ... ) {
        PyErr_SetString(PyExc_ValueError, "invalid argument");
    }
    return NULL;
}

static PyObject *
handle_numpy(PyObject *lst, double (*fun)(const std::vector<double>&))
{
    PyArrayObject* arr = reinterpret_cast<PyArrayObject*>(lst);

    int is_cont = PyArray_IS_C_CONTIGUOUS(arr);
    if (!is_cont) {
        PyErr_SetString(PyExc_ValueError, "Expected continuous C array");
        return NULL;
    }
    // int nd_flags = PyArray_FLAGS(arr);
    // int is_carr = PyArray_ISCARRAY(arr);

    int arr_type = PyArray_TYPE(arr);
    if (arr_type != NPY_FLOAT64) {
        PyErr_SetString(PyExc_ValueError, "Expected float64 array type");
        return NULL;
    }

    const double *p = (double*)PyArray_DATA(arr);
    int ND = (int) PyArray_NDIM(arr);
    if (ND == 1) {
        int N = (int) PyArray_DIM(arr, 0);
        std::vector<double>xs;
        xs.assign(p, p+N);
        double ret = nan("");
        try {
            ret = fun(xs);
            PyObject *v = PyFloat_FromDouble(ret);
            return v;
        } catch ( ... ) {
            PyErr_SetString(PyExc_ValueError, "invalid argument");
        }
    } else if (ND == 2) {
        int N = (int) PyArray_DIM(arr, 1);
        int n_rows = (int) PyArray_DIM(arr, 0);
        double *buf = new double[n_rows];  // XXX: TODO: check for memory leaks
        for (int idx=0; idx<n_rows; ++idx) {
            std::vector<double> xs;
            xs.assign(p+idx*N, p+N+idx*N);
            double ret = nan("");
            try {
                ret = fun(xs);
            } catch ( ... ) {
                // TODO: inform user
            }
            buf[idx] = ret;
        }
        npy_intp dims[1] = { n_rows };
        PyObject* array = PyArray_SimpleNewFromData(
                1, dims,  NPY_FLOAT64, (void*)buf);
        if (!array) throw std::runtime_error("Unknown failure in py_bench");
        // ((PyArrayObject*)array)->flags |= NPY_OWNDATA;
        return array;
    } else {
        PyErr_SetString(PyExc_ValueError, "Unexpected array shape; try 1d or 2d float64 arrays");
    }
    return NULL;
}

static PyObject *
py_bench(PyObject *, PyObject *args, double (*fun)(const std::vector<double>&))
{
    PyObject *lst;
    if (!PyArg_ParseTuple(args, "O", &lst))
        return NULL;

    bool is_list = PyList_Check(lst);
    if (is_list)
        return handle_list(lst, fun);

    bool is_array = PyArray_Check(lst);
    if (is_array)
        return handle_numpy(lst, fun);

    PyErr_SetString(PyExc_TypeError, "Expected a list or a numpy array");
    return NULL;
}

#ifndef PYWRAP
#define PYWRAP( name ) static PyObject *py_ ## name (PyObject *self, PyObject *args) {return py_bench(self, args, name);}
#endif

PYWRAP(ackley);
PYWRAP(alpine);
PYWRAP(bohachevsky1);
PYWRAP(bohachevsky2);
PYWRAP(bohachevsky3);
PYWRAP(bukin_f6);
PYWRAP(cross_in_tray);
PYWRAP(eggholder);
PYWRAP(gramacy_lee);
PYWRAP(holder_table);
PYWRAP(langermann);
PYWRAP(levy);
PYWRAP(levy13);
PYWRAP(six_hump_camel_back);
PYWRAP(dejong5);
PYWRAP(deceptive3);
PYWRAP(drop_wave);
PYWRAP(easom);
PYWRAP(penalty1);
PYWRAP(michalewicz);
PYWRAP(perm0db);
PYWRAP(permdb);
PYWRAP(non_cont_rastrigin);
PYWRAP(rastrigin);
PYWRAP(rosenbrock);
PYWRAP(griewank);
PYWRAP(goldstein_price);
PYWRAP(axis_parallel_hyperellipsoid);
PYWRAP(rotated_hyperellipsoid);
PYWRAP(sum_powers);
PYWRAP(trid);
PYWRAP(step);
PYWRAP(schaffers_f2);
PYWRAP(schaffers_f4);
PYWRAP(schaffers_f6);
PYWRAP(schwefels);
PYWRAP(schwefels_p222);
PYWRAP(shubert);
PYWRAP(sphere);
PYWRAP(tripod);
PYWRAP(trefethen4);
PYWRAP(three_hump_camel_back);
PYWRAP(dixon_price);
PYWRAP(beale);
PYWRAP(branin);
PYWRAP(colville);
PYWRAP(styblinski_tang);
PYWRAP(powell);
PYWRAP(shekel);
PYWRAP(forrester);
PYWRAP(hartmann_3d);
PYWRAP(hartmann_4d);
PYWRAP(hartmann_6d);
PYWRAP(booth);
PYWRAP(matyas);
PYWRAP(mccormick);
PYWRAP(power_sum);
PYWRAP(zakharov);

static PyMethodDef
CBenchMethods[] = {
    {"ackley", py_ackley, METH_VARARGS, "Ackley function"},
    {"alpine", py_alpine, METH_VARARGS, "Alpine function"},
    {"bohachevsky1", py_bohachevsky1, METH_VARARGS, "bohachevsky1 function"},
    {"bohachevsky2", py_bohachevsky2, METH_VARARGS, "bohachevsky2 function"},
    {"bohachevsky3", py_bohachevsky3, METH_VARARGS, "bohachevsky3 function"},
    {"bukin_f6", py_bukin_f6, METH_VARARGS, "Bukin function 6"},
    {"cross_in_tray", py_cross_in_tray, METH_VARARGS, "cross_in_tray function"},
    {"eggholder", py_eggholder, METH_VARARGS, "eggholder function"},
    {"gramacy_lee", py_gramacy_lee, METH_VARARGS, "Gramacy Lee function"},
    {"holder_table", py_holder_table, METH_VARARGS, "holder table function"},
    {"langermann", py_langermann, METH_VARARGS, "langermann function"},
    {"levy", py_levy, METH_VARARGS, "levy function"},
    {"levy13", py_levy13, METH_VARARGS, "levy13 function"},
    {"six_hump_camel_back", py_six_hump_camel_back, METH_VARARGS, "six_hump_camel_back function"},
    // {"dejong2", py_sphere, METH_VARARGS, "dejong5 (sphere) function"},
    {"dejong5", py_dejong5, METH_VARARGS, "dejong5 function"},
    {"deceptive3", py_deceptive3, METH_VARARGS, "deceptive3 function"},
    {"drop_wave", py_drop_wave, METH_VARARGS, "drop_wave function"},
    {"easom", py_easom, METH_VARARGS, "easom function"},
    {"penalty1", py_penalty1, METH_VARARGS, "penalty1 function"},
    {"parabola", py_sphere, METH_VARARGS, "parabola (sphere) function"},
    {"michalewicz", py_michalewicz, METH_VARARGS, "michalewicz function"},
    {"perm0db", py_perm0db, METH_VARARGS, "perm0db function"},
    {"permdb", py_permdb, METH_VARARGS, "perm d beta function"},
    {"non_cont_rastrigin", py_non_cont_rastrigin, METH_VARARGS, "non-continuous rastrigin function"},
    {"rastrigin", py_rastrigin, METH_VARARGS, "rastrigin function"},
    {"rosenbrock", py_rosenbrock, METH_VARARGS, "rosenbrock function"},
    {"griewank", py_griewank, METH_VARARGS, "griewank function"},
    {"goldstein_price", py_goldstein_price, METH_VARARGS, "griewank function"},
    {"axis_parallel_hyperellipsoid", py_axis_parallel_hyperellipsoid, METH_VARARGS, "axis_parallel_hyperellipsoid function"},
    {"sum_squares", py_axis_parallel_hyperellipsoid, METH_VARARGS, "sum_squares (axis_parallel_hyperellipsoid) function"},
    {"rotated_hyperellipsoid", py_rotated_hyperellipsoid, METH_VARARGS, "rotated_hyperellipsoid function"},
    {"sum_powers", py_sum_powers, METH_VARARGS, "sum_powers function"},
    {"trid", py_trid, METH_VARARGS, "trid function"},
    {"step", py_step, METH_VARARGS, "step function"},
    {"schaffers_f2", py_schaffers_f2, METH_VARARGS, "schaffers_f2 function"},
    {"schaffers_f4", py_schaffers_f4, METH_VARARGS, "schaffers_f4 function"},
    {"schaffers_f6", py_schaffers_f6, METH_VARARGS, "schaffers_f6 function"},
    {"schwefels", py_schwefels, METH_VARARGS, "schwefels function"},
    {"schwefels_p222", py_schwefels_p222, METH_VARARGS, "schwefels_p222 function"},
    {"shubert", py_shubert, METH_VARARGS, "shubert function"},
    {"sphere", py_sphere, METH_VARARGS, "sphere function"},
    {"tripod", py_tripod, METH_VARARGS, "tripod function"},
    {"trefethen4", py_trefethen4, METH_VARARGS, "trefethen4 function"},
    {"three_hump_camel_back", py_three_hump_camel_back, METH_VARARGS, "three hump camel function"},
    {"dixon_price", py_dixon_price, METH_VARARGS, "dixon price function"},
    {"beale", py_beale, METH_VARARGS, "Beale function"},
    {"branin", py_branin, METH_VARARGS, "Branin function"},
    {"colville", py_colville, METH_VARARGS, "Colville function"},
    {"styblinski_tang", py_styblinski_tang, METH_VARARGS, "Styblinski_tang function"},
    {"powell", py_powell, METH_VARARGS, "Powell function"},
    {"shekel", py_shekel, METH_VARARGS, "Shekel function"},
    {"forrester", py_forrester, METH_VARARGS, "Forrester function"},
    {"hartmann_3d", py_hartmann_3d, METH_VARARGS, "Hartmann_3d function"},
    {"hartmann_4d", py_hartmann_4d, METH_VARARGS, "Hartmann_4d function"},
    {"hartmann_6d", py_hartmann_6d, METH_VARARGS, "Hartmann_6d function"},
    {"booth", py_booth, METH_VARARGS, "Booth function"},
    {"matyas", py_matyas, METH_VARARGS, "Matyas function"},
    {"mccormick", py_mccormick, METH_VARARGS, "McCormick function"},
    {"power_sum", py_power_sum, METH_VARARGS, "power_sum function"},
    {"zakharov", py_zakharov, METH_VARARGS, "Zakharov function"},
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef
cModPyDem = {
    PyModuleDef_HEAD_INIT,
    "optobench", /* name of the module */
    "Python interface for the C++ benchmark optimization functions",  /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    CBenchMethods
};


// Module initialization
// Python 3.x
PyMODINIT_FUNC
PyInit_optobench(void)
{
    PyObject *module = PyModule_Create(&cModPyDem);
    PyModule_AddStringConstant(module, "__version__", "0.2.0");
    import_array();     // initialize NumPy C-API
                        // PyError if not successful
    return module;
}

// Python 2.x
// PyMODINIT_FUNC
// initcbench(void)
// {
//     (void) Py_InitModule("cbench", CBenchMethods);
// }

