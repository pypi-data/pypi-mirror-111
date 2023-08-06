#include <stdio.h>

#define PIXEL_MIN 0
#define PIXEL_MAX 255

// Helper functions to control minimum and maximum pixel values
int Minimum(int input1, int input2) {
    return input1 < input2 ? input1 : input2;
}

int Maximum(int input1, int input2) {
    return input1 > input2 ? input1 : input2;
}

// Blending functions for multiple images
void AdditionBlend(int size, __uint8_t* image1, __uint8_t* image2, __uint8_t* result) {
    for (int i = 0; i < size; i++) {
        result[i] = Minimum(image1[i] + image2[i], PIXEL_MAX);
    }
}

void SubtractionBlend(int size, __uint8_t* image1, __uint8_t* image2, __uint8_t* result) {
    for (int i = 0; i < size; i++) {
        result[i] = Maximum(image1[i] - image2[i], PIXEL_MIN);
    }
}