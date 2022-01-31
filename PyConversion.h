#pragma once

#include <string>
#include <vector>
#include <Python.h>

std::vector<unsigned int> unsinged_int_vec_from_list(PyObject* incoming);
std::vector<int> int_vec_from_list(PyObject* incoming);
std::vector<std::string> string_vec_from_list(PyObject* incoming);

PyObject* to_list_vec_unsinged_int(const std::vector<unsigned int> the_vec);
PyObject* to_list_vec_int(const std::vector<int> the_vec);
PyObject* to_list_vec_double(const std::vector<double> the_vec);
PyObject* to_list_vec_string(const std::vector<std::string> the_vec);
