[![lint-free](https://github.com/software-students-spring2025/4-containers-anycontain/actions/workflows/lint.yml/badge.svg)](https://github.com/software-students-spring2025/4-containers-anycontain/actions/workflows/lint.yml)
[![Python CI](https://github.com/software-students-spring2025/4-containers-anycontain/actions/workflows/ci.yml/badge.svg)](https://github.com/software-students-spring2025/4-containers-anycontain/actions/workflows/ci.yml)
# Containerized App Exercise

# Animal Detection for Wildlife Protection

This project implements a machine learning client that detects the presence and type of animals in images for wild life protection. It collects images, analyzes them using a finetuned LLaVA-based model, and then stores the raw image data and detection metadata into a MongoDB database. 

## Environment Setup

This project is managed with [Pipenv](https://pipenv.pypa.io/en/latest/). It includes both runtime dependencies and development tools (like `pytest`, `black`, and `pylint`).

### Prerequisites

- **Python 3.11** installed on your system.
- [Pipenv](https://pipenv.pypa.io/en/latest/install/) installed globally.
- A MongoDB instance. (For local testing, you can run MongoDB in a Docker container or use your local installation. For production, consider using MongoDB Atlas.)

### Steps to Set Up the Environment

1. **Clone the Repository:**

   ```bash
   git clone <https://github.com/software-students-spring2025/4-containers-anycontain>
   cd <4-containers-anycontain>
   ```

2. **Install the Pipenv Environment:** 
   ```bash
   pipenv install --dev
   ```

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.
