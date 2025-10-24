#include "Renderer.h"
#include <iomanip>
#include <sstream>

Renderer::Renderer(const std::string& window_name)
    : m_window_name(window_name),
      m_is_drawing(false),
      m_last_point(-1, -1)
{
    // Initialize the canvas as 280x280, 1-channel (grayscale)
    // Larger canvas for easier drawing, resized in ImageProcessor
    m_canvas = cv::Mat(280, 280, CV_8UC1, cv::Scalar(0));

    // Initialize the display buffer as 280x280, 3-channel (color)
    m_display_buffer = cv::Mat(280, 280, CV_8UC3, cv::Scalar(0, 0, 0));

    // Create the OpenCV window
    cv::namedWindow(m_window_name);

    // Set the mouse callback
    // Pass 'this' as userdata to access instance methods
    cv::setMouseCallback(m_window_name, Renderer::mouse_callback, this);
}

Renderer::~Renderer() {
    cv::destroyWindow(m_window_name);
}

void Renderer::update(const Prediction& pred, bool is_stopped) {
    {
        // Lock mutex for thread-safe access
        std::lock_guard<std::mutex> lock(m_canvas_mutex);
        // Convert 1-channel canvas to 3-channel display buffer
        cv::cvtColor(m_canvas, m_display_buffer, cv::COLOR_GRAY2BGR);
    } // Mutex unlocked

    // Prepare text and color for display
    std::string text = "Drawing...";
    cv::Scalar color(255, 255, 255); // White

    if (pred.digit != -1) {
        // Format confidence to 2 decimal places
        std::stringstream ss;
        ss << std::fixed << std::setprecision(2) << pred.confidence;

        if (is_stopped) {
            // Final prediction (locked)
            text = "Final: " + std::to_string(pred.digit) + " (" + ss.str() + ")";
            color = cv::Scalar(0, 255, 255); // Yellow
        } else {
            // Active prediction
            text = "Pred: " + std::to_string(pred.digit) + " (" + ss.str() + ")";
            color = cv::Scalar(0, 255, 0); // Green
        }
    }

    // Draw text on display buffer
    cv::putText(
        m_display_buffer,
        text,
        cv::Point(10, 25),
        cv::FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2
    );

    // Show the updated display
    cv::imshow(m_window_name, m_display_buffer);
}

char Renderer::get_key_press() {
    // Poll for key press for 20ms
    // This also allows the window to refresh
    return static_cast<char>(cv::waitKey(20));
}

void Renderer::clear_canvas() {
    std::lock_guard<std::mutex> lock(m_canvas_mutex);
    m_canvas.setTo(cv::Scalar(0)); // Set all pixels to black
}

cv::Mat Renderer::get_canvas() {
    std::lock_guard<std::mutex> lock(m_canvas_mutex);
    // Return a copy for thread safety
    return m_canvas.clone();
}

bool Renderer::is_drawing() const {
    std::lock_guard<std::mutex> lock(m_canvas_mutex);
    return m_is_drawing;
}

// --- Mouse Callback Implementation ---

void Renderer::mouse_callback(int event, int x, int y, int flags, void* userdata) {
    // Cast userdata back to Renderer instance pointer
    Renderer* renderer = static_cast<Renderer*>(userdata);
    if (renderer) {
        renderer->on_mouse(event, x, y);
    }
}

void Renderer::on_mouse(int event, int x, int y) {
    // Lock mutex to protect canvas and mouse state
    std::lock_guard<std::mutex> lock(m_canvas_mutex);

    if (event == cv::EVENT_LBUTTONDOWN) {
        // Start drawing
        m_is_drawing = true;
        m_last_point = cv::Point(x, y);
    } else if (event == cv::EVENT_LBUTTONUP) {
        // Stop drawing
        m_is_drawing = false;
    } else if (event == cv::EVENT_MOUSEMOVE && m_is_drawing) {
        // Draw a thick white line on the canvas
        cv::line(
            m_canvas,
            m_last_point,
            cv::Point(x, y),
            cv::Scalar(255), // White
            20               // Thick line for better recognition
        );
        m_last_point = cv::Point(x, y);
    }
}
