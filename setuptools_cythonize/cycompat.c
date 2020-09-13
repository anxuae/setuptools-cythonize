/*
 * check_signals
 * =============
 *
 * Use this function in your cythonized application if it setup some signals
 * handlers thanks to the 'signal' module). It periodically checks for pending
 * signals an run signal handlers (this includes raising KeyboardInterrupt if
 * necessary). check_signals is pretty fast, it's OK to call it often.
 *
 * Example:
 * --------
 *
 * Call it every Nth iteration of an infinite loop:
 *
 * def run(self):
 *     while True:
 *         # Do some work here
 *         check_signals()
 *
 * Note: it should be called from the main thread, because Python runs signal
 * handlers in the main thread. Calling it from worker threads has no effect.
 *
 * Explanations:
 * -------------
 *
 * Since signals are delivered asynchronously at unpredictable times, it is
 * problematic to run any meaningful code directly from the signal handler.
 * Therefore, Python queues incoming signals. The queue is processed later as
 * part of the interpreter loop.
 *
 * If your code is fully compiled, interpreter loop is never executed and Python
 * has no chance to check and run queued signal handlers.
 */

#include <Python.h>

static PyObject *check_signals() {
    return Py_BuildValue("i", PyErr_CheckSignals());
}

static PyMethodDef module_methods[] = {
    { "check_signals", check_signals, METH_VARARGS, "Check for pending signals and run signal handlers installed with signal module." },
    { NULL, NULL, 0, NULL }
};

#if PY_MAJOR_VERSION >= 3
/* Module initialization Python version 3 */

static struct PyModuleDef cycompat =
{
    PyModuleDef_HEAD_INIT,
    "cycompat",                              /* Module name*/
    "Cython compatibility helper module",    /* Module documentation*/
    -1,                                      /* Size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    module_methods
};

PyMODINIT_FUNC PyInit_cycompat(void) {
    return PyModule_Create(&cycompat);
}

#else
/* Module initialization Python version 2 */

PyMODINIT_FUNC
initcycompat(void) {
    PyObject *m = Py_InitModule3("cycompat", module_methods, "Cython compatibility helper module");
    if (m == NULL)
        return;
}

#endif
