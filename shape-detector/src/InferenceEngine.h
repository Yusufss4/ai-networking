#ifndef INFERENCE_ENGINE_H
#define INFERENCE_ENGINE_H

#include <torch/script.h> // The main LibTorch header
#include <string>
#include "types.h" // For the Prediction struct

/**
 * @class InferenceEngine
 * @brief Manages loading the AI model and running predictions.
 *
 * This class loads a TorchScript model at construction and provides
 * a single method 'predict' to run inference on an input tensor.
 */
class InferenceEngine {
public:
    /**
     * @brief Constructs the engine and loads the model.
     * Throws a std::runtime_error if the model fails to load.
     * @param model_path Path to the exported .pt (TorchScript) model file.
     */
    explicit InferenceEngine(const std::string& model_path);

    /**
     * @brief Runs inference on a pre-processed input tensor.
     * @param input_tensor The input tensor, expected to be [1, 1, 28, 28].
     * @return A 'Prediction' struct containing the predicted digit and confidence.
     */
    Prediction predict(const torch::Tensor& input_tensor);

private:
    // The loaded TorchScript module.
    torch::jit::script::Module m_model;
};

#endif // INFERENCE_ENGINE_H