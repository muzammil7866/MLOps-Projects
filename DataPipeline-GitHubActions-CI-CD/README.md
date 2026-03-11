# Data Pipeline - GitHub Actions CI/CD

Production-ready data processing and analysis pipeline with automated CI/CD using GitHub Actions and Makefile-based workflow orchestration.

## Overview

This project demonstrates MLOps best practices by implementing a complete data pipeline with:
- Reproducible data processing workflows via Makefile
- Automated code quality checks (Black formatting, linting)
- CI/CD automation with GitHub Actions
- Automated report generation
- CML (Continuous Machine Learning) integration

## Dataset: World Happiness Report 2023

- **Source**: World Happiness Report (WHR)
- **Original File**: `WHR2023.csv` (raw/data/)
- **Processing**: Data cleaning, validation, aggregation
- **Output**: `WHR2023_cleaned.csv` (processed_data/)

## Pipeline Stages

### 1. Data Processing (`data_processing.py`)
- CSV loading and validation
- Missing value handling
- Outlier detection
- Data type conversion
- Feature engineering

### 2. Data Analysis (`data_analysis.py`)
- Descriptive statistics
- Correlation analysis
- Visualization generation
- Report creation
- Summary statistics → `summary.txt`

## Makefile Targets

```makefile
make install          # Install dependencies from requirements.txt
make format           # Format code with Black
make process-data     # Run data_processing.py
make analyze          # Run data_analysis.py
make summary          # Generate summary.txt report
make all              # Run full pipeline
```

## GitHub Actions Workflows

Automated CI/CD with:
- Code formatting checks (Black)
- Data pipeline execution
- Report generation
- CML comment annotations
- PR automation

## Features

- **Reproducibility**: Makefile ensures consistent execution order
- **Code Quality**: Black auto-formatting, error checking
- **Automation**: GitHub Actions triggers on push/PR
- **Documentation**: Inline code comments and README
- **Metrics Tracking**: CML integration for metrics in PR comments
- **Artifact Management**: Processed data and reports as outputs

## Requirements

```
pandas>=1.0.0
numpy>=1.18.0
matplotlib>=3.0.0
seaborn>=0.9.0
black>=22.0.0
scikit-learn>=0.20.0
```

## File Structure

```
DataPipeline-GitHubActions-CI-CD/
├── Makefile                          # Workflow orchestration
├── requirements.txt                  # Python dependencies
├── data_processing.py               # Data cleaning/processing
├── data_analysis.py                 # Statistical analysis
├── raw_data/
│   └── WHR2023.csv                 # Original dataset
├── processed_data/
│   ├── WHR2023_cleaned.csv         # Cleaned output
│   └── summary.txt                 # Analysis summary
├── figures/                         # Generated plots
└── .github/workflows/               # GitHub Actions configs
```

## Usage

### Local Execution

```bash
# Install dependencies
make install

# Run complete pipeline
make all

# Or individual stages
make process-data
make analyze
make summary
```

### Automated Execution

Push to GitHub to trigger CI/CD workflows:
1. Code formatting check
2. Data processing
3. Analysis generation
4. Report publication in PR comments

## Metrics Tracked

- Data quality metrics
- Processing statistics
- Analysis results
- Model performance (if applicable)

## MLOps Best Practices Demonstrated

✓ Makefile for reproducible workflows  
✓ Version-controlled data processing  
✓ Code formatting automation (Black)  
✓ Dependency management (requirements.txt)  
✓ CI/CD automation  
✓ Artifacts and metrics logging  
✓ Continuous monitoring  
✓ Documentation and comments  

## Configuration

### Makefile Variables

Customize variables in Makefile:
- `PYTHON`: Python interpreter
- `PIP`: Package installer
- `DATA_DIR`: Raw data directory
- `OUTPUT_DIR`: Processed data directory

### GitHub Actions

Configure in `.github/workflows/`:
- Trigger events
- Environment variables
- Secret management
- Artifact retention

## Extending the Pipeline

Add new stages:

1. Create processing script (e.g., `feature_engineering.py`)
2. Add Makefile target
3. Update GitHub Actions workflow
4. Document in README

## Troubleshooting

**Issue**: Make command not found  
**Solution**: Install GNU Make (Windows: use WSL or Git Bash)

**Issue**: Missing Python dependencies  
**Solution**: Run `make install` to install requirements

**Issue**: GitHub Actions failures  
**Solution**: Check workflow logs in Actions tab

## Future Enhancements

- Docker containerization
- Database integration
- API endpoints for data access
- Advanced monitoring/alerting
- Data quality checks (Great Expectations)
- Feature store integration
