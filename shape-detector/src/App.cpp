#include "App.h"

// Now we include the full definitions of our components
#include "ImageProcessor.h"
#include "InferenceEngine.h"
#include "Renderer.h"

// JSON library
#include "nlohmann/json.hpp" // Assumes you have this in an 'nlohmann' subfolder
using json = nlohmann::json;

// Standard library includes
#include <fstream>
#include <iostream>

App::App(const std::string &config_path)
    : m_is_running(true) // Start in a running state
{
  try {
    // 1. Load configuration
    load_config(config_path);

    // 2. Initialize components
    // We use std::make_unique for modern, exception-safe object creation.
    m_processor = std::make_unique<ImageProcessor>();
    m_renderer = std::make_unique<Renderer>("Digit Recognizer");
    m_engine = std::make_unique<InferenceEngine>(m_model_path);

    std::cout << "Application initialized successfully." << std::endl;
    std::cout << "Controls: (c) clear, (q) quit" << std::endl;

  } catch (const std::exception &e) {
    std::cerr << "Application failed to initialize: " << e.what() << std::endl;
    throw; // Re-throw to stop the application
  }
}

// This explicit, empty destructor is required in the .cpp file
// to correctly destroy the unique_ptrs to forward-declared types.
App::~App() = default;

void App::load_config(const std::string &config_path) {
  std::ifstream config_file(config_path);
  if (!config_file.is_open()) {
    throw std::runtime_error("Could not open config file: " + config_path);
  }

  json config;
  config_file >> config;

  // Load values from JSON, with error checking
  if (config.contains("model_path")) {
    m_model_path = config["model_path"];
  } else {
    throw std::runtime_error("Config missing 'model_path'");
  }

  if (config.contains("confidence_threshold")) {
    m_confidence_threshold = config["confidence_threshold"];
  } else {
    throw std::runtime_error("Config missing 'confidence_threshold'");
  }

  std::cout << "Config loaded: " << m_model_path
            << " (Threshold: " << m_confidence_threshold << ")" << std::endl;
}

void App::run() {
  // This is the main application loop
  while (true) {
    // 1. Handle user input
    char key = m_renderer->get_key_press();
    if (key == 'q') {
      break; // Exit loop
    }
    if (key == 'c') {
      m_renderer->clear_canvas();
      m_is_running = true;    // Re-enable inference
      m_last_prediction = {}; // Reset the last prediction
    }

    // 2. Run inference (only if not stopped)
    if (m_is_running) {
      // Get the current drawing from the renderer
      cv::Mat canvas = m_renderer->get_canvas();

      // Process the image into a tensor
      torch::Tensor tensor = m_processor->process(canvas);

      // Get a prediction from the engine
      m_last_prediction = m_engine->predict(tensor);

      // Check if confidence threshold is met
      if (m_last_prediction.confidence >= m_confidence_threshold) {
        m_is_running = false; // Stop inference
      }
    }

    // 3. Update the display
    // We update the renderer every frame (even if stopped)
    // to keep the window responsive and show the final result.
    m_renderer->update(m_last_prediction, !m_is_running);
  }
}