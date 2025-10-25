#include "ImageProcessor.h"

torch::Tensor ImageProcessor::process(const cv::Mat& raw_image) {
    // 1. Resize the image to 28x28
    // The model was trained on 28x28 images
    cv::Mat resized_image;
    cv::resize(raw_image, resized_image, cv::Size(28, 28), 0, 0, cv::INTER_LINEAR);

    // 2. Convert cv::Mat to torch::Tensor
    // torch::from_blob creates a tensor that "views" the cv::Mat's data
    // Input is 1-channel grayscale, shape [1, 1, 28, 28] (B, C, H, W)
    // Data type is CV_8UC1 (uint8), which corresponds to torch::kByte
    torch::Tensor tensor = torch::from_blob(
        resized_image.data,
        {1, 1, 28, 28},
        torch::kByte
    );

    // 3. Convert type, scale, and clone
    // Must clone() because from_blob() doesn't own memory
    // and resized_image will go out of scope
    // Convert to float and scale from [0, 255] to [0.0, 1.0]
    tensor = tensor.to(torch::kFloat32).div(255.0);

    // 4. Normalize using MNIST dataset statistics
    // (tensor - mean) / std
    tensor = tensor.sub(MNIST_MEAN).div(MNIST_STD);

    return tensor;
}
