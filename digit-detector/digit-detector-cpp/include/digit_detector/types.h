#ifndef TYPES_H
#define TYPES_H

#include <string>

/**
 * @file types.h
 * @brief Common type definitions for the digit detector.
 */

/**
 * @struct Prediction
 * @brief Holds the result of a digit recognition inference.
 */
struct Prediction {
    int digit = -1;         ///< The predicted digit (0-9), or -1 if no prediction
    float confidence = 0.0; ///< The confidence score (0.0-1.0)
};

#endif // TYPES_H
