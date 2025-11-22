# Ray Parallel Training Lab - Diabetes Disease Progression Prediction

This project demonstrates the power of **distributed computing** using [Ray](https://www.ray.io/) to accelerate machine learning model training. We compare **sequential vs. parallel training** of Gradient Boosting models on the **Diabetes dataset** to predict disease progression.

### Key Features
-  **2-4x speedup** using Ray's parallel computing framework
- Real-world medical prediction problem (diabetes progression)
- Comprehensive performance metrics and visualization


## Dataset

**Diabetes Dataset** from scikit-learn
- **442 patients** with 10 baseline features
- **Features**: age, sex, BMI, blood pressure, 6 blood serum measurements
- **Target**: Quantitative measure of disease progression one year after baseline
- **Problem Type**: Regression


## Methodology

### Sequential Training (Baseline)
- Trains 20 Gradient Boosting models **one at a time**
- Each model uses different hyperparameters:
  - `n_estimators`: 50, 60, 70, ..., 240
  - `learning_rate`: 0.05, 0.055, 0.06, ..., 0.145
  - `max_depth`: 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, ...

### Parallel Training (Ray)
- Trains all 20 models **simultaneously** using Ray's distributed framework
- Ray automatically detects available CPU cores
- Same hyperparameter configurations as sequential training

## Results

### Performance Comparison
```
TIMING RESULTS:
  Sequential Time: 1.80s
  Parallel Time:   0.58s
  Speedup:         3.11x faster
  Time Saved:      1.22s (67.8%)
```

### Best Model Found
```
BEST MODEL:
  n_estimators: 80
  learning_rate: 0.065
  max_depth: 2
  RMSE: 52.42
  R²: 0.4814
  MAE: 42.74
```

## How It Works

### Ray Architecture
```
           ┌─ Model 1
           ├─ Model 2
Scheduler ─┤  Model 3   (all running simultaneously)
           ├─ Model 4
           └─ Model ...
```

### Key Concepts

1. **Object Store**: Ray stores training data in distributed memory
   ```python
   X_train_ref = ray.put(X_train)  # Creates reference, not copy
   ```

2. **Remote Functions**: `@ray.remote` decorator enables distribution
   ```python
   @ray.remote
   def train_and_score_model_remote(...):
       # Training logic
   ```

3. **Asynchronous Execution**: 
   ```python
   results_ref = [model.remote(...) for _ in range(20)]  # Non-blocking
   results = ray.get(results_ref)  # Wait for completion
   ```

## Installation

### Requirements
```bash
pip install ray scikit-learn pandas numpy matplotlib
```

### Python Version
- Python 3.7 or higher recommended

## Usage

### Running the Notebook

1. **Clone or download** the repository
2. **Open Jupyter Lab/Notebook**
   ```bash
   jupyter lab
   ```
3. **Open** `Ray.ipynb`
4. **Run all cells** sequentially

### Expected Output
- Training progress for both sequential and parallel runs
- Performance comparison table
- Visualization of RMSE and R² trends

## Visualizations

The notebook generates two plots showing:
- **RMSE vs. Number of Trees** (lower is better)
- **R² Score vs. Number of Trees** (higher is better)

Both metrics help identify the optimal model configuration.
