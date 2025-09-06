# Project Rules

## Naming Conventions
- Use English for all file and folder names
- Use snake_case for directories and files
- No Cyrillic characters in paths

## Structure
- `practical_work_N/` - for practical work N
- `practical_work_N/task_N/` - for specific tasks

## Jupyter Notebook Formatting Rules
- No comments in code
- Remove all extra explanatory text
- Structure format:
  - Task number
  - Full task condition
  - Code only
  - Code output
- Tasks requiring user input must use `input()` function
- Tasks with "программа принимает", "на вход получает" require interactive input

## Setup and Dependencies
- Use `setup.sh` (macOS/Linux) or `setup.bat` (Windows) for quick project setup
- Scripts automatically create virtual environment and install all dependencies
- **IMPORTANT**: When using new Python libraries, update both setup scripts with the new dependencies

### Current Dependencies
- pandas - data manipulation and analysis
- scikit-learn - machine learning library
- jupyter - interactive notebooks
- matplotlib - plotting library
- seaborn - statistical data visualization
- numpy - numerical computing
- scipy - scientific computing

### Usage
**macOS/Linux:**
```bash
./setup.sh
```

**Windows:**
```cmd
setup.bat
```