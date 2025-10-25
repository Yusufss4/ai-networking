#ifndef INFERENCE_ENGINE_H
#define INFERENCE_ENGINE_H

#include <torch/script.h>
#include <string>
#include "types.h"

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
     * @param model_path Path to the exported .ts (TorchScript) model file.
     * @throws std::runtime_error if the model fails to load.
     */
    explicit InferenceEngine(const std::string& model_path);

    /**
     * @brief Runs inference on a pre-processed input tensor.
     * @param input_tensor The input tensor, expected to be [1, 1, 28, 28].
     * @return A Prediction struct containing the predicted digit and confidence.
     */
    Prediction predict(const torch::Tensor& input_tensor);

private:
    torch::jit::script::Module m_model; ///< The loaded TorchScript module
};

#endif // INFERENCE_ENGINE_H
