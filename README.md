# Abstracting Terms of Service

## Project Overview

This project aims to automate the analysis and abstraction of Terms of Service (ToS) documents to identify potentially problematic clauses and practices. By leveraging natural language processing and machine learning techniques, the system extracts and classifies segments of ToS documents that may be concerning for users.

## Problem Statement

Terms of Service documents are often lengthy, complex, and difficult for average users to understand. This project addresses this issue by:

1. Collecting ToS documents from various online services
2. Processing and analyzing the text to identify concerning clauses
3. Classifying these clauses into categories of user rights concerns
4. Providing a simplified abstraction of the key issues users should be aware of

## Project Structure

The repository is organized into the following directories:

### 1. Data Collection (`1_data_collection/`)

Scripts for gathering Terms of Service documents from online services:

- `pull_docs.py`: Retrieves ToS documents from services
- `browser_login.py`: Handles browser automation for accessing services
- `pull_highlights.py`: Extracts highlighted sections from documents
- `data_func.py`: Utility functions for data collection

### 2. Data Preprocessing (`2_data_preprocessing/`)

- `Data_Preprocessing.ipynb`: Notebook for cleaning and preparing the collected data for analysis

### 3. Baselines (`3_baselines/`)

Baseline models for comparison:

- `Stage1_Chunk_Baseline.ipynb`: Baseline model using chunk-based approach
- `Stage1_Sentence_Baseline.ipynb`: Baseline model using sentence-based approach
- `Stage2_Baseline.ipynb`: Second-stage baseline model

### 4. Experiments (`4_experiments/`)

Different experimental approaches:

- `Chunk/`: Experiments using chunk-based text processing
- `Sentence/`: Experiments using sentence-based text processing

### 5. Full Orchestration (`5_full_orchestration/`)

End-to-end pipeline implementation:

- `Full_Orchestration.ipynb`: Complete pipeline from data to results
- `Stage1_Model.ipynb`: First-stage model implementation
- `Stage2_Model.ipynb`: Second-stage model implementation
- `Full Orchestration - True Positives.xlsx`: Analysis of model performance

### 6. Reports (`6_reports/`)

- `Abstracting Terms of Service.pdf`: Comprehensive report on the project methodology and findings

## Getting Started

### Prerequisites

- Python 3.8+
- Required Python packages (install via `pip install -r requirements.txt`):
  - pandas
  - numpy
  - scikit-learn
  - jupyter
  - transformers
  - torch
  - openpyxl
  - browserbase (for web automation)

### Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/tosdr.git
   cd tosdr
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Usage

1. **Data Collection**:

   ```
   cd 1_data_collection
   python pull_docs.py
   ```

2. **Data Preprocessing**:

   - Open and run the Jupyter notebook in `2_data_preprocessing/`

3. **Running Models**:
   - Execute the notebooks in `5_full_orchestration/` for the complete pipeline

## Methodology

The project employs a two-stage approach:

1. **Stage 1**: Identifies potentially problematic segments in ToS documents
2. **Stage 2**: Classifies these segments into specific categories of concern

Both stages utilize natural language processing techniques and machine learning models to analyze and categorize text.

## Results

The system successfully identifies concerning clauses in Terms of Service documents and categorizes them based on their potential impact on user rights. For detailed results and analysis, refer to the report in the `6_reports/` directory.

## Acknowledgments

- [Terms of Service; Didn't Read](https://tosdr.org/) for inspiration and data sources
