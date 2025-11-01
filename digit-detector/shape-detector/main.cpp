#include "src/App.h" // The main application header
#include <iostream>  // For std::cerr
#include <stdexcept> // For std::exception

int main() {
  // Define the path to the configuration file
  const std::string config_path = "config.json";

  try {
    // 1. Create the application instance
    //    All initialization (loading config, models, UI)
    //    happens in the App's constructor.
    App application(config_path);

    // 2. Start the main application loop
    application.run();

  } catch (const std::exception &e) {
    // If anything went wrong during initialization or runtime,
    // catch the exception, print it, and exit.
    std::cerr << "CRITICAL ERROR: " << e.what() << std::endl;
    return 1; // Return a non-zero code to indicate failure
  }

  // If the loop exits cleanly (e.g., user pressed 'q')
  return 0; // Return 0 to indicate success
}