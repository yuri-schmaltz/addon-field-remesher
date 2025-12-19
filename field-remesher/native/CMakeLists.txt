cmake_minimum_required(VERSION 3.18)
project(instant_meshes_py LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG v2.11.1
)
FetchContent_MakeAvailable(pybind11)

# TODO:
# - Adicionar upstream como submodule em third_party/instant-meshes
# - Criar/ligar uma lib "instant_meshes_core" sem dependências de UI

pybind11_add_module(instant_meshes_py
  src/bindings.cpp
  src/im_wrapper.cpp
)

target_include_directories(instant_meshes_py PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/src
  ${CMAKE_CURRENT_SOURCE_DIR}/third_party/instant-meshes
)

# target_link_libraries(instant_meshes_py PRIVATE instant_meshes_core)
