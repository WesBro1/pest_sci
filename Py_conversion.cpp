#include "PyConversion.h"

std::vector<unsigned int> unsinged_int_vec_from_list(PyObject* incoming)
{
	std::vector<unsigned int> data;
	if (PyTuple_Check(incoming)) {
		for (Py_ssize_t i = 0; i < PyTuple_Size(incoming); i++) {
			PyObject* value = PyTuple_GetItem(incoming, i);
			data.push_back(PyLong_AsUnsignedLong(value));
		}
	}
	else {
		if (PyList_Check(incoming)) {
			for (Py_ssize_t i = 0; i < PyList_Size(incoming); i++) {
				PyObject* value = PyList_GetItem(incoming, i);
				data.push_back(PyLong_AsUnsignedLong(value));
			}
		}
	}
	return data;
}

std::vector<int> int_vec_from_list(PyObject* incoming)
{
	std::vector<int> data;
	if (PyTuple_Check(incoming)) {
		for (Py_ssize_t i = 0; i < PyTuple_Size(incoming); i++) {
			PyObject* value = PyTuple_GetItem(incoming, i);
			data.push_back(PyLong_AsLong(value));
		}
	}
	else {
		if (PyList_Check(incoming)) {
			for (Py_ssize_t i = 0; i < PyList_Size(incoming); i++) {
				PyObject* value = PyList_GetItem(incoming, i);
				data.push_back(PyLong_AsLong(value));
			}
		}
	}
	return data;
}

std::vector<std::string> string_vec_from_list(PyObject* incoming)
{
	std::vector<std::string> data;
	if (PyTuple_Check(incoming)) {
		for (Py_ssize_t i = 0; i < PyTuple_Size(incoming); i++) {
			PyObject* value = PyTuple_GetItem(incoming, i);
			Py_ssize_t size = 0;
			char const* pc = PyUnicode_AsUTF8AndSize(value, &size);
			if (pc) {
				data.push_back(std::string(pc, size));
			}
		}
	}
	else {
		if (PyList_Check(incoming)) {
			for (Py_ssize_t i = 0; i < PyList_Size(incoming); i++) {
				PyObject* value = PyList_GetItem(incoming, i);
				Py_ssize_t size = 0;
				char const* pc = PyUnicode_AsUTF8AndSize(value, &size);
				if (pc) {
					data.push_back(std::string(pc, size));
				}
			}
		}
	}
	return data;
}

PyObject* to_list_vec_unsinged_int(const std::vector<unsigned int> the_vec)
{
	PyObject* listObj = PyList_New( the_vec.size() );
	for (unsigned int i = 0; i < the_vec.size(); i++) {
		PyObject* num = PyLong_FromUnsignedLong(the_vec[i]);
		if (!num) {
			Py_DECREF(listObj);
		}
		PyList_SET_ITEM(listObj, i, num);
	}
	return listObj;
}

PyObject* to_list_vec_int(const std::vector<int> the_vec)
{
	PyObject* listObj = PyList_New(the_vec.size());
	for (unsigned int i = 0; i < the_vec.size(); i++) {
		PyObject* num = PyLong_FromLong(the_vec[i]);
		if (!num) {
			Py_DECREF(listObj);
		}
		PyList_SET_ITEM(listObj, i, num);
	}
	return listObj;
}

PyObject* to_list_vec_double(const std::vector<double> the_vec)
{
	PyObject* listObj = PyList_New(the_vec.size());
	for (unsigned int i = 0; i < the_vec.size(); i++) {
		PyObject* num = PyFloat_FromDouble(the_vec[i]);
		if (!num) {
			Py_DECREF(listObj);
		}
		PyList_SET_ITEM(listObj, i, num);
	}
	return listObj;
}

PyObject* to_list_vec_string(const std::vector<std::string> the_vec)
{
	PyObject* listObj = PyList_New(the_vec.size());
	for (unsigned int i = 0; i < the_vec.size(); i++) {
		PyObject* num = PyUnicode_FromString(the_vec[i].c_str());
		if (!num) {
			Py_DECREF(listObj);
		}
		PyList_SET_ITEM(listObj, i, num);
	}
	return listObj;
}

