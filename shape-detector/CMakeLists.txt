cmake_minimum_required(VERSION 3.10)
project(RealTimeDraw)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find LibTorch
find_package(Torch REQUIRED)
# Find OpenCV
find_package(OpenCV REQUIRED)

# Create the executable
add_executable(shape_detector main.cpp)

# Link against both libraries
target_link_libraries(shape_detector
    "${TORCH_LIBRARIES}"
    "${OpenCV_LIBS}"
)

set_property(TARGET shape_detector PROPERTY CXX_STANDARD_REQUIRED ON)