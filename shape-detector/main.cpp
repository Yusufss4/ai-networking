#include <torch/script.h>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>

// --- Global variables for mouse drawing ---
cv::Mat canvas;
cv::Point last_point(-1, -1);
bool is_drawing = false;

// --- Mouse callback function to handle drawing ---
void mouse_callback(int event, int x, int y, int flags, void* userdata) {
    if (event == cv::EVENT_LBUTTONDOWN) {
        is_drawing = true;
        last_point = cv::Point(x, y);
    } else if (event == cv::EVENT_LBUTTONUP) {
        is_drawing = false;
    } else if (event == cv::EVENT_MOUSEMOVE && is_drawing) {
        cv::line(canvas, last_point, cv::Point(x, y), cv::Scalar(255, 255, 255), 20);
        last_point = cv::Point(x, y);
    }
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: ./shape_detector <path-to-digit_model.pt>\n";
        return -1;
    }

    // --- 1. Load the Model ---
    torch::jit::script::Module model;
    try {
        model = torch::jit::load(argv[1], torch::kCPU);
        model.eval();
        std::cout << "Digit recognition model loaded.\n";
    } catch (const c10::Error& e) {
        std::cerr << "Error loading the model\n";
        return -1;
    }

    // --- 2. Setup the Drawing Canvas ---
    canvas = cv::Mat(280, 280, CV_8UC3, cv::Scalar(0, 0, 0));
    cv::namedWindow("Draw a Digit");
    cv::setMouseCallback("Draw a Digit", mouse_callback, NULL);

    std::cout << "\nControls:\n"
              << " - Draw with the left mouse button.\n"
              << " - Press 'c' to classify the digit.\n"
              << " - Press 'd' to delete/clear the canvas.\n"
              << " - Press 'q' to quit.\n\n";

    // --- 3. Main Application Loop ---
    while (true) {
        cv::imshow("Draw a Digit", canvas);
        char key = (char)cv::waitKey(20);

        if (key == 'q') {
            break;
        } else if (key == 'd') {
            canvas.setTo(cv::Scalar(0, 0, 0)); // Clear canvas
        } else if (key == 'c') {
            // --- 4. Preprocess the Image for the Model ---
            cv::Mat processed_image;
            // Convert to grayscale
            cv::cvtColor(canvas, processed_image, cv::COLOR_BGR2GRAY);
            // Resize to 28x28, the size the model expects
            cv::resize(processed_image, processed_image, cv::Size(28, 28));

            // Convert cv::Mat to a torch::Tensor
            std::vector<int64_t> sizes = {1, 1, processed_image.rows, processed_image.cols};
            auto options = torch::TensorOptions().dtype(torch::kFloat32);
            torch::Tensor input_tensor = torch::from_blob(processed_image.data, sizes, options);
            
            // Normalize the tensor to match training conditions
            input_tensor = input_tensor.clone(); // Clone to make it mutable
            input_tensor /= 255.0; // Scale to [0, 1]
            input_tensor = (input_tensor - 0.1307) / 0.3081; // MNIST normalization

            // --- 5. Run Inference ---
            at::Tensor output = model.forward({input_tensor}).toTensor();
            auto prediction = output.argmax(1);
            int digit = prediction.item<int>();

            std::cout << "Model prediction: " << digit << std::endl;

            // Display the prediction on the canvas
            cv::putText(canvas, "Prediction: " + std::to_string(digit),
                        cv::Point(10, 20), cv::FONT_HERSHEY_SIMPLEX, 0.7,
                        cv::Scalar(0, 255, 0), 2);
        }
    }

    return 0;
}