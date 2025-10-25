#include "InferenceEngine.h"
#include <iostream>
#include <stdexcept>
#include <vector>

InferenceEngine::InferenceEngine(const std::string& model_path) {
    try {
        // Load the TorchScript model from disk
        // Explicitly map to CPU
        m_model = torch::jit::load(model_path, torch::kCPU);

        // Set the model to evaluation mode
        // This disables dropout and batch normalization training behavior
        m_model.eval();

        std::cout << "InferenceEngine: Model loaded successfully from "
                  << model_path << std::endl;
    } catch (const c10::Error& e) {
        // If loading fails, log the error and throw
        std::cerr << "Error loading model: " << e.what() << std::endl;
        throw std::runtime_error("Failed to load LibTorch model: " + model_path);
    }
}

Prediction InferenceEngine::predict(const torch::Tensor& input_tensor) {
    // 1. Prepare input for the model
    // The forward() method expects a vector of IValue
    std::vector<torch::jit::IValue> inputs;
    inputs.push_back(input_tensor);

    // 2. Run forward pass
    // Output is a tensor of logits (raw scores), shape [1, 10]
    at::Tensor logits = m_model.forward(inputs).toTensor();

    // 3. Convert logits to probabilities using softmax
    at::Tensor probabilities = torch::softmax(logits, 1);

    // 4. Get the maximum probability and its index
    // torch::max returns a tuple of (values, indices)
    auto max_result = torch::max(probabilities, 1);
    at::Tensor max_confidence_tensor = std::get<0>(max_result);
    at::Tensor max_index_tensor = std::get<1>(max_result);

    // 5. Extract scalar values from tensors
    float confidence = max_confidence_tensor.item<float>();
    int digit = max_index_tensor.item<int>();

    // 6. Return the result
    return {digit, confidence};
}
