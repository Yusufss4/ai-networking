cmake_minimum_required(VERSION 3.10)
project(DigitDetector VERSION 1.0.0 LANGUAGES CXX)

# --- C++ Standard ---
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# --- Build Type ---
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# --- Compiler Flags ---
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    add_compile_options(-Wall -Wextra -Wpedantic)
    if(CMAKE_BUILD_TYPE STREQUAL "Release")
        add_compile_options(-O3)
    endif()
endif()

# --- Find Dependencies ---

# 1. Find LibTorch (PyTorch C++ API)
#    Specify path with: cmake -DCMAKE_PREFIX_PATH=/path/to/libtorch ..
find_package(Torch REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${TORCH_CXX_FLAGS}")

# 2. Find OpenCV
find_package(OpenCV REQUIRED COMPONENTS core highgui imgproc)

# --- Source Files ---
set(SOURCES
    src/main.cpp
    src/App.cpp
    src/InferenceEngine.cpp
    src/ImageProcessor.cpp
    src/Renderer.cpp
)

set(HEADERS
    include/digit_detector/App.h
    include/digit_detector/InferenceEngine.h
    include/digit_detector/ImageProcessor.h
    include/digit_detector/Renderer.h
    include/digit_detector/types.h
)

# --- Executable Target ---
add_executable(digit_recognizer ${SOURCES} ${HEADERS})

# --- Include Directories ---
target_include_directories(digit_recognizer
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${CMAKE_CURRENT_SOURCE_DIR}/include/digit_detector
        ${CMAKE_CURRENT_SOURCE_DIR}/include/third_party
)

# --- Link Libraries ---
target_link_libraries(digit_recognizer
    PRIVATE
        ${TORCH_LIBRARIES}
        ${OpenCV_LIBS}
)

# --- LibTorch Specific Settings ---
set_property(TARGET digit_recognizer PROPERTY CXX_STANDARD 17)

# Copy torch DLLs to output directory (Windows only)
if(MSVC)
    file(GLOB TORCH_DLLS "${TORCH_INSTALL_PREFIX}/lib/*.dll")
    add_custom_command(TARGET digit_recognizer
        POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${TORCH_DLLS}
        $<TARGET_FILE_DIR:digit_recognizer>)
endif()

# --- Install Target ---
install(TARGETS digit_recognizer
    RUNTIME DESTINATION bin
)

# --- Build Information ---
message(STATUS "========================================")
message(STATUS "Digit Detector Configuration")
message(STATUS "========================================")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Compiler: ${CMAKE_CXX_COMPILER_ID}")
message(STATUS "LibTorch: ${TORCH_LIBRARIES}")
message(STATUS "OpenCV: ${OpenCV_VERSION}")
message(STATUS "OpenCV Libs: ${OpenCV_LIBS}")
message(STATUS "========================================")
