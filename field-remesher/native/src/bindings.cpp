#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "im_wrapper.h"

namespace py = pybind11;

PYBIND11_MODULE(instant_meshes_py, m) {
    m.doc() = "Instant-like remeshing engine bindings (scaffold)";

    m.def("remesh", &im::remesh_numpy,
          py::arg("verts"), py::arg("faces"), py::arg("options"),
          "Run remeshing and return (out_verts, out_faces, meta).");
}
