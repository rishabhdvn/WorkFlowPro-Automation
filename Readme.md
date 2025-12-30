# WorkFlow Pro - QA Automation Assessment

## Overview
This repository contains the automation solution for the WorkFlow Pro B2B SaaS platform. It includes a robust test framework design, fixes for legacy flaky tests, and a hybrid API/UI integration strategy.

## Repository Structure
* **`tests/`**: Contains the automated test scripts.
* **`config/`**: Shared fixtures and configuration.
* **`data/`**: Externalized test data (JSON).
* **`TEST_PLAN.md`**: Detailed framework design and strategy (Part 2).
* **`.github/workflows`**: CI/CD Pipeline configuration.

## Setup & Execution
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install