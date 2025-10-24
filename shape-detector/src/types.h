#ifndef TYPES_H
#define TYPES_H

#include <string>

// A simple struct to hold the prediction results
struct Prediction {
    int digit = -1;       // The predicted digit (e.g., 7)
    float confidence = 0.0; // The confidence score (e.g., 0.95)
};

#endif // TYPES_H