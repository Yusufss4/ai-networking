#ifndef RENDERER_H
#define RENDERER_H

#include <opencv2/opencv.hpp>
#include <string>
#include <mutex>
#include "types.h" // For the Prediction struct

/**
 * @class Renderer
 * @brief Manages the GUI window, mouse input, and drawing.
 *
 * This class uses OpenCV to create a window, captures mouse
 * events for drawing, and displays the current canvas state
 * along with the model's predictions.
 */
class Renderer {
public:
    /**
     * @brief Constructs the Renderer.
     * @param window_name The name to display on the GUI window.
     */
    Renderer(const std::string& window_name);

    /**
     * @brief Destructor. Cleans up the OpenCV window.
     */
    ~Renderer();

    /**
     * @brief Updates the window with the latest prediction text.
     * This function also calls cv::imshow().
     * @param pred The prediction from the model.
     * @param is_stopped True if inference is paused, changes text color.
     */
    void update(const Prediction& pred, bool is_stopped);

    /**
     * @brief Polls for user key presses.
     * @return The character of the key pressed, or -1 if none.
     */
    char get_key_press();

    /**
     * @brief Clears the drawing canvas.
     */
    void clear_canvas();

    /**
     * @brief Gets a thread-safe copy of the current drawing.
     * @return A cv::Mat copy of the 1-channel drawing canvas.
     */
    cv::Mat get_canvas();

    bool is_drawing() const;

  private:
    /**
     * @brief Static C-style callback for OpenCV mouse events.
     * This function acts as a bridge to our class instance.
     */
    static void mouse_callback(int event, int x, int y, int flags, void* userdata);

    /**
     * @brief The instance method that handles mouse drawing logic.
     */
    void on_mouse(int event, int x, int y);

    // --- Member Variables ---
    cv::Mat m_canvas;         // 1-channel (grayscale) for the model
    cv::Mat m_display_buffer; // 3-channel (color) for the user
    std::string m_window_name;

    // --- State for drawing ---
    bool m_is_drawing;
    cv::Point m_last_point;

    // --- Thread Safety ---
    mutable std::mutex m_canvas_mutex; // Protects m_canvas and mouse state
};

#endif // RENDERER_H