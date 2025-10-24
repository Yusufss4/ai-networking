#ifndef IMAGE_PROCESSOR_H
#define IMAGE_PROCESSOR_H

#include <opencv2/opencv.hpp>
#include <torch/script.h>

/**
 * @class ImageProcessor
 * @brief Handles preprocessing of images for the model.
 *
 * This is a stateless utility class that converts a raw
 * cv::Mat from the canvas into a normalized, correctly-sized
 * tensor for the InferenceEngine.
 */
class ImageProcessor {
public:
  /**
   * @brief Default constructor.
   */
  ImageProcessor() = default;

  /**
   * @brief Processes a raw image into a model-ready tensor.
   * @param raw_image The 1-channel, 280x280 image from the Renderer.
   * @return A [1, 1, 28, 28] float tensor, scaled and normalized.
   */
  torch::Tensor process(const cv::Mat &raw_image);

private:
  // MNIST dataset-specific normalization constants
  static constexpr double MNIST_MEAN = 0.1307;
  static constexpr double MNIST_STD = 0.3081;
};

#endif // IMAGE_PROCESSOR_H