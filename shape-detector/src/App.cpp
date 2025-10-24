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
    : m_inference_active(true) // Start in a running state
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
  while (true) {
    // 1. Handle user input
    char key = m_renderer->get_key_press();
    if (key == 'q') {
      break;
    }
    if (key == 'c') {
      m_renderer->clear_canvas();
      m_inference_active = true; // Re-enable inference
      m_last_prediction = {};
    }

    // --- NEW LOGIC ---
    // Get the user's drawing state
    bool is_user_drawing = m_renderer->is_drawing();

    // If the user starts drawing again, unlock the inference
    if (is_user_drawing) {
      m_inference_active = true;
    }

    // 2. Run inference (only if active)
    if (m_inference_active) {
      cv::Mat canvas = m_renderer->get_canvas();
      torch::Tensor tensor = m_processor->process(canvas);
      m_last_prediction = m_engine->predict(tensor);

      // NEW STOP CONDITION:
      // Stop ONLY IF confidence is high AND the user is NOT drawing.
      if (m_last_prediction.confidence >= m_confidence_threshold &&
          !is_user_drawing) {
        m_inference_active = false; // Stop/lock inference
      }
    }

    // 3. Update the display
    // Pass the "stopped" state to the renderer for styling
    m_renderer->update(m_last_prediction, !m_inference_active);
  }
}