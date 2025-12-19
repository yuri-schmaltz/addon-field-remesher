#pragma once
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

namespace im {
    pybind11::tuple remesh_numpy(pybind11::array_t<float> verts,
                                 pybind11::array_t<int> faces,
                                 pybind11::dict options);
}
