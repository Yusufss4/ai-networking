#ifndef APP_H
#define APP_H

#include <memory>
#include <string>
#include "types.h" // Include our simple Prediction struct

// Forward declarations of our components
// This avoids including their full headers here,
// which speeds up compilation.
class InferenceEngine;
class ImageProcessor;
class Renderer;

/**
 * @class App
 * @brief The main application class.
 *
 * This class owns and coordinates all major components:
 * - Renderer (for UI and drawing)
 * - ImageProcessor (for data conversion)
 * - InferenceEngine (for running the model)
 * It also manages the main application loop and state.
 */
class App {
public:
    /**
     * @brief Constructs the application.
     * @param config_path Path to the JSON configuration file.
     */
    App(const std::string& config_path);
    
    /**
     * @brief Destructor.
     * Required for a clean shutdown with unique_ptrs to
     * forward-declared types.
     */
    ~App();

    /**
     * @brief Starts and runs the main application loop.
     */
    void run();

private:
    /**
     * @brief Loads settings from the JSON config file.
     * @param config_path Path to the JSON configuration file.
     */
    void load_config(const std::string& config_path);

    // --- Components ---
    // We use std::unique_ptr for modern C++ resource management.
    // The App "owns" these components.
    std::unique_ptr<InferenceEngine> m_engine;
    std::unique_ptr<ImageProcessor> m_processor;
    std::unique_ptr<Renderer> m_renderer;

    // --- Configuration & State ---
    std::string m_model_path;
    float m_confidence_threshold;
    bool m_is_running;          // Controls if inference is active
    Prediction m_last_prediction; // Stores the last prediction
};

#endif // APP_H