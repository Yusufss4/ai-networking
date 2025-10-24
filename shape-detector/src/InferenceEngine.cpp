#include "InferenceEngine.h"
#include <iostream>
#include <stdexcept> // For std::runtime_error
#include <vector>

InferenceEngine::InferenceEngine(const std::string &model_path) {
  try {
    // Load the model from disk
    // We explicitly map it to the CPU
    m_model = torch::jit::load(model_path, torch::kCPU);

    // Set the model to evaluation mode. This is critical for
    // disabling things like dropout, which are only used during training.
    m_model.eval();

    std::cout << "InferenceEngine: Model loaded successfully from "
              << model_path << std::endl;
  } catch (const c10::Error &e) {
    // If loading fails, log the error and throw an exception
    // to let the App class know initialization failed.
    std::cerr << "Error loading model: " << e.what() << std::endl;
    throw std::runtime_error("Failed to load LibTorch model: " + model_path);
  }
}

Prediction InferenceEngine::predict(const torch::Tensor &input_tensor) {
  // 1. Prepare the input for the model
  // The model.forward() method expects a std::vector of IValue.
  std::vector<torch::jit::IValue> inputs;
  inputs.push_back(input_tensor);

  // 2. Run the forward pass
  // The output 'logits' is a tensor of raw scores, shape [1, 10]
  at::Tensor logits = m_model.forward(inputs).toTensor();

  // 3. Convert raw scores (logits) to probabilities
  // We apply a softmax function along dimension 1
  at::Tensor probabilities = torch::softmax(logits, 1);

  // 4. Get the max probability and its index
  // torch::max returns a tuple of (values, indices)
  auto max_result = torch::max(probabilities, 1);
  at::Tensor max_confidence_tensor = std::get<0>(max_result);
  at::Tensor max_index_tensor = std::get<1>(max_result);

  // 5. Extract the scalar values from the tensors
  float confidence = max_confidence_tensor.item<float>();
  int digit = max_index_tensor.item<int>();

  // 6. Return the result in our struct
  return {digit, confidence};
}