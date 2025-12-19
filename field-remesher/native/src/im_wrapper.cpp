\
#include "im_wrapper.h"
#include <stdexcept>

namespace py = pybind11;

namespace im {

py::tuple remesh_numpy(py::array_t<float> verts,
                       py::array_t<int> faces,
                       py::dict options) {
    // TODO: Implementar:
    // 1) Validar shapes (N,3) e (M,3) (ou equivalente)
    // 2) Chamar core do engine (instant_meshes_core)
    // 3) Retornar (out_verts, out_faces, meta)
    throw std::runtime_error("instant_meshes_py.remesh() não implementado neste scaffold.");
}

}
