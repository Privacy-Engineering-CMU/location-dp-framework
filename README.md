# Unified Locational Differential Privacy Framework

A versatile differential privacy framework for privacy-preserving aggregation of diverse geographical data types.

## Overview

The Unified Locational Differential Privacy Framework is a comprehensive tool designed to enable private aggregation of various data types over geographical regions while providing strong privacy guarantees. This framework is inspired by Apple's work on learning "iconic scenes" using differential privacy and extends its capabilities to handle a wide range of data types commonly encountered in geographical analysis, such as one-hot encoded vectors, boolean arrays, integer counts, and floating-point values.

## Features

- Support for diverse data types: one-hot encoded, boolean, float, and integer arrays
- Implementation of local differential privacy mechanisms: randomized response, exponential mechanism, and Gaussian mechanism
- Privacy budget tracking and composition using the Opacus library
- Modular design for easy integration of additional data types and mechanisms
- Evaluation on simulated datasets representing real-world location data aggregation scenarios

## Installation

```bash
# Clone the repository
git clone https://github.com/Privacy-Engineering-CMU/location-dp-framework.git

# Install the required dependencies
pip install -r requirements.txt
```

## Usage

```python
# Run our streamlit app
streamlit run app.py
```

## Directory Structure

```
./MVP/
├── dataset/
│   ├── __init__.py
│   ├── base_simulator.py
│   ├── boolean_simulator.py
│   ├── integers_simulator.py
│   ├── one_hot_simulator.py
│   ├── rankings_simulator.py
├── localDP/
│   ├── __init__.py
│   ├── exponential_mechanism.py
│   ├── gaussian_mechanism.py
│   └── randomized_response.py
├── README.md
├── requirements.txt
├── app.py
├── simulation_runner.py
└── ...
```

## Research and Methods

### Background

Aggregating statistics over geographical regions is crucial for various applications, such as analyzing income, election results, and disease spread. However, the sensitive nature of this data necessitates robust privacy protections. Inspired by [Apple's work on learning "iconic scenes"](https://machinelearning.apple.com/research/scenes-differential-privacy) using differential privacy, we developed a unified locational differential privacy framework that extends its capabilities to handle diverse data types and aggregation scenarios.

### Differential Privacy Mechanisms

Our framework employs three local differential privacy mechanisms:

1. Randomized Response: Suitable for binary or categorical attributes, providing plausible deniability to respondents.
2. Exponential Mechanism: Privately selects an output from a set of possible choices based on a utility function, useful for large or unordered output spaces.
3. Gaussian Mechanism: Adds carefully calibrated Gaussian noise to the true output of a function, commonly used for numerical queries or functions with continuous output ranges.

### Privacy Budget Tracking and Composition

To ensure that the overall differential privacy guarantees are maintained throughout the aggregation process, we utilize the Opacus library for privacy budget tracking and composition. Opacus provides advanced privacy accounting techniques and implements composition theorems, allowing for accurate tracking of privacy loss across multiple mechanisms and aggregation steps.

### Evaluation on Simulated Datasets

Due to the lack of suitable real-world datasets, we evaluate our framework on four simulated datasets representing different data aggregation scenarios:

1. One-hot encoded data (Apple's implementation)
2. Boolean-based data (contagion tracking)
3. Integer-based data (rankings)
4. Float-based data (income)

These datasets are carefully designed to capture the key characteristics and challenges associated with various types of geographical data, such as spatial correlations and dependencies.

## Future Work

- Integration of secure aggregation protocols for enhanced privacy protection
- Extension of the framework to support additional data types and mechanisms
- Evaluation on real-world datasets to validate the framework's effectiveness in practical settings
- Packaging the framework into an open-source library for wider adoption and contribution

## Tools and Libraries Used:

We would like to acknowledge the following libraries and resources that have been instrumental in the development of this framework:

- Diffprivlib: A comprehensive Python library for differential privacy algorithms and tools
- Opacus: A powerful Python library for differentially private computations in PyTorch
- [Apple's work on learning "iconic scenes"](https://machinelearning.apple.com/research/scenes-differential-privacy) using differential privacy

## License

This project is licensed under the [MIT License](LICENSE).
