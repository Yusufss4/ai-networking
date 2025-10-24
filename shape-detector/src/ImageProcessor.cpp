#include "ImageProcessor.h"

torch::Tensor ImageProcessor::process(const cv::Mat &raw_image) {
  // 1. Resize the image
  // The model was trained on 28x28 images.
  cv::Mat resized_image;
  cv::resize(raw_image, resized_image, cv::Size(28, 28), 0, 0,
             cv::INTER_LINEAR);

  // 2. Convert cv::Mat to torch::Tensor
  // torch::from_blob creates a tensor that "views" the cv::Mat's data.
  // No data is copied here.
  // The input 'resized_image' is 1-channel (grayscale), so shape is [1, 1, 28,
  // 28] (B, C, H, W) The data type is CV_8UC1, which corresponds to
  // torch::kByte.
  torch::Tensor tensor =
      torch::from_blob(resized_image.data, {1, 1, 28, 28}, torch::kByte);

  // 3. Convert type, scale, and clone
  // We must .clone() because the original tensor from from_blob()
  // does not own its memory, and 'resized_image' will go out of scope.
  // .to(torch::kFloat32) converts to float.
  // .div(255.0) scales pixel values from [0, 255] to [0.0, 1.0].
  tensor = tensor.to(torch::kFloat32).div(255.0);

  // 4. Normalize the tensor
  // (tensor - mean) / std
  // We use the pre-calculated mean and std dev of the MNIST dataset.
  tensor = tensor.sub(MNIST_MEAN).div(MNIST_STD);

  return tensor;
}