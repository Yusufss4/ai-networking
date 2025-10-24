cmake_minimum_required(VERSION 3.10)
project(DigitRecognizer)

# --- Set C++ Standard ---
# We use C++17 for modern features like std::unique_ptr
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# --- Find Dependencies ---

# 1. Find LibTorch (PyTorch C++ API)
#    You MUST provide the path to LibTorch when you run cmake
#    e.g., cmake -DCMAKE_PREFIX_PATH=/path/to/libtorch ..
find_package(Torch REQUIRED)

# 2. Find OpenCV
#    We need these specific components:
#    - core: For cv::Mat, cv::Point, etc.
#    - highgui: For cv::namedWindow, cv::imshow, cv::waitKey
#    - imgproc: For cv::resize, cv::cvtColor, cv::line, cv::putText
find_package(OpenCV REQUIRED COMPONENTS core highgui imgproc)

# --- Define the Executable ---

# Create an executable named 'digit_recognizer'
add_executable(digit_recognizer
    main.cpp
    src/App.cpp
    src/ImageProcessor.cpp
    src/InferenceEngine.cpp
    src/Renderer.cpp
)

# --- Configure Includes and Links ---

# 1. Add our 'src' directory to the include path
#    This lets us find our headers (#include "App.h")
#    and the json header (#include "nlohmann/json.hpp")
target_include_directories(digit_recognizer
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# 2. Link our executable against the libraries
target_link_libraries(digit_recognizer
    PUBLIC
    ${TORCH_LIBRARIES}
    ${OpenCV_LIBS}
)

# --- LibTorch Specific Setting ---
# This is often required for C++11 ABI compatibility with LibTorch
set_property(TARGET digit_recognizer PROPERTY CXX_STANDARD_REQUIRED ON)

# --- Install (Optional but good practice) ---
# This will create a 'make install' command
install(TARGETS digit_recognizer
    RUNTIME DESTINATION bin
)

# --- Output ---
message(STATUS "Configured DigitRecognizer")
message(STATUS "  - LibTorch found: ${TORCH_LIBRARIES}")
message(STATUS "  - OpenCV found: ${OpenCV_LIBS}")