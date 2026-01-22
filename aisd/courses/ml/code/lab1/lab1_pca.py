"""
CST8506 Lab 1: Dimensionality Reduction using PCA
Author: [Your Name]
Section: [Your Section]
Date: [Date]

This program performs Principal Component Analysis (PCA) on the Diabetes dataset
to reduce dimensionality and compares model performance before and after reduction.

Innovations:
- Comprehensive visualization with both 2D and 3D plots
- Detailed variance analysis with dual scree plots
- Complete performance comparison metrics
"""

# Step 1: Import required libraries
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from pathlib import Path

# Set random seed for reproducibility
RANDOM_STATE = 42
TEST_SIZE = 0.2
N_ESTIMATORS = 100
VARIANCE_THRESHOLD = 0.95

# Create images directory
IMAGES_DIR = Path('images')
IMAGES_DIR.mkdir(exist_ok=True)

np.random.seed(RANDOM_STATE)

print("=" * 80)
print("CST8506 Lab 1: PCA Dimensionality Reduction")
print("=" * 80)
print()


def load_dataset(filepath):
    """
    Load the diabetes dataset from CSV file.
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded dataset
    """
    df = pd.read_csv(filepath)
    return df


def print_dataset_info(df):
    """
    Print basic information about the dataset.
    
    Args:
        df (pd.DataFrame): Dataset to analyze
    """
    print("Attribute names:", df.columns.tolist())
    print(f"Number of instances: {len(df)}")
    print(f"Number of attributes: {len(df.columns)}")
    print("\nFirst 5 instances:")
    print(df.head())
    print()


def split_features_target(df, target_column='class'):
    """
    Split dataset into features and target variable.
    
    Args:
        df (pd.DataFrame): Dataset to split
        target_column (str): Name of target column
        
    Returns:
        tuple: (X, y) features and target
    """
    X = df.drop(target_column, axis=1)
    y = df[target_column]
    return X, y


def standardize_data(X_train, X_test):
    """
    Standardize features using StandardScaler.
    
    Args:
        X_train (np.ndarray): Training features
        X_test (np.ndarray): Test features
        
    Returns:
        tuple: (X_train_scaled, X_test_scaled, scaler)
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler


def train_random_forest(X_train, y_train, n_estimators=N_ESTIMATORS):
    """
    Train a Random Forest classifier.
    
    Args:
        X_train (np.ndarray): Training features
        y_train (np.ndarray): Training labels
        n_estimators (int): Number of trees in the forest
        
    Returns:
        RandomForestClassifier: Trained model
    """
    rf = RandomForestClassifier(n_estimators=n_estimators, random_state=RANDOM_STATE)
    rf.fit(X_train, y_train)
    return rf


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance.
    
    Args:
        model: Trained classifier
        X_test (np.ndarray): Test features
        y_test (np.ndarray): Test labels
        
    Returns:
        tuple: (confusion_matrix, accuracy)
    """
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    return cm, acc


def apply_pca_full(X_train, X_test):
    """
    Apply PCA to extract all principal components.
    
    Args:
        X_train (np.ndarray): Training features
        X_test (np.ndarray): Test features
        
    Returns:
        tuple: (X_train_pca, X_test_pca, pca_model)
    """
    pca = PCA()
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)
    return X_train_pca, X_test_pca, pca


def find_optimal_components(explained_variance_ratio, threshold=VARIANCE_THRESHOLD):
    """
    Find optimal number of components based on variance threshold.
    
    Args:
        explained_variance_ratio (np.ndarray): Variance explained by each component
        threshold (float): Minimum cumulative variance to retain
        
    Returns:
        int: Optimal number of components
    """
    cumulative_variance = np.cumsum(explained_variance_ratio)
    n_components = np.argmax(cumulative_variance >= threshold) + 1
    return n_components


def plot_scree_plots(explained_variance, cumulative_variance, save_path='images/lab1_scree_plots.png'):
    """
    Generate scree plots for variance analysis.
    
    Args:
        explained_variance (np.ndarray): Variance explained by each component
        cumulative_variance (np.ndarray): Cumulative variance
        save_path (str): Path to save the plot
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Explained Variance Ratio
    ax1.plot(range(1, len(explained_variance) + 1), explained_variance, 
             'bo-', linewidth=2, markersize=8)
    ax1.set_xlabel('Principal Component Number', fontsize=12)
    ax1.set_ylabel('Explained Variance Ratio', fontsize=12)
    ax1.set_title('Scree Plot - Explained Variance Ratio', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(range(1, len(explained_variance) + 1))
    
    # Plot 2: Cumulative Explained Variance
    ax2.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, 
             'ro-', linewidth=2, markersize=8)
    ax2.axhline(y=0.85, color='g', linestyle='--', linewidth=2, label='85% variance')
    ax2.axhline(y=0.90, color='orange', linestyle='--', linewidth=2, label='90% variance')
    ax2.axhline(y=0.95, color='purple', linestyle='--', linewidth=2, label='95% variance')
    ax2.set_xlabel('Principal Component Number', fontsize=12)
    ax2.set_ylabel('Cumulative Explained Variance Ratio', fontsize=12)
    ax2.set_title('Scree Plot - Cumulative Variance', fontsize=14, fontweight='bold')
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(range(1, len(cumulative_variance) + 1))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_2d_pca(X_pca, y, save_path='images/lab1_pca_2d.png'):
    """
    Plot first 2 principal components in 2D.
    
    Args:
        X_pca (np.ndarray): PCA-transformed features
        y (np.ndarray): Labels
        save_path (str): Path to save the plot
    """
    plt.figure(figsize=(10, 8))
    
    classes = np.unique(y)
    colors = plt.cm.Set1(np.linspace(0, 1, len(classes)))
    
    for class_label, color in zip(classes, colors):
        mask = y == class_label
        plt.scatter(X_pca[mask, 0], X_pca[mask, 1], c=[color],
                   label=f'Class {class_label}', alpha=0.6,
                   edgecolors='black', linewidth=0.5, s=50)
    
    plt.xlabel('First Principal Component (PC1)', fontsize=12)
    plt.ylabel('Second Principal Component (PC2)', fontsize=12)
    plt.title('2D Visualization: First 2 Principal Components', 
              fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_3d_pca(X_pca, y, save_path='images/lab1_pca_3d.png'):
    """
    Plot first 3 principal components in 3D.
    
    Args:
        X_pca (np.ndarray): PCA-transformed features
        y (np.ndarray): Labels
        save_path (str): Path to save the plot
    """
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    classes = np.unique(y)
    colors = plt.cm.Set1(np.linspace(0, 1, len(classes)))
    
    for class_label, color in zip(classes, colors):
        mask = y == class_label
        ax.scatter(X_pca[mask, 0], X_pca[mask, 1], X_pca[mask, 2],
                  c=[color], label=f'Class {class_label}', alpha=0.6,
                  edgecolors='black', linewidth=0.5, s=50)
    
    ax.set_xlabel('First Principal Component (PC1)', fontsize=11)
    ax.set_ylabel('Second Principal Component (PC2)', fontsize=11)
    ax.set_zlabel('Third Principal Component (PC3)', fontsize=11)
    ax.set_title('3D Visualization: First 3 Principal Components', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================================
# Main Program
# ============================================================================

# Step 1: Load the CSV file using Pandas
print("Step 1: Loading diabetes.csv file...")
print("-" * 80)
df = load_dataset('diabetes.csv')
print("Dataset loaded successfully")
print()

# Step 2: Print dataset information
print("Step 2: Dataset Information")
print("-" * 80)
print_dataset_info(df)

# Step 3: Split the dataset into train and test sets
print("Step 3: Splitting dataset into train and test sets")
print("-" * 80)
X, y = split_features_target(df)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)
print(f"Training set size: {X_train.shape[0]} instances")
print(f"Test set size: {X_test.shape[0]} instances")
print(f"Number of features: {X_train.shape[1]}")
print()

# Step 4: Standardize the data
print("Step 4: Standardizing the data")
print("-" * 80)
X_train_scaled, X_test_scaled, scaler = standardize_data(X_train, X_test)
print("Data standardized successfully")
print(f"Mean of scaled training data: {X_train_scaled.mean():.6f}")
print(f"Standard deviation of scaled training data: {X_train_scaled.std():.6f}")
print()

# Step 5: Fit Random Forest model (Baseline)
print("Step 5: Training baseline Random Forest model (before PCA)")
print("-" * 80)
rf_baseline = train_random_forest(X_train_scaled, y_train)
cm_baseline, acc_baseline = evaluate_model(rf_baseline, X_test_scaled, y_test)
print("Baseline model trained successfully")
print("Baseline Confusion Matrix:")
print(cm_baseline)
print(f"Baseline Accuracy: {acc_baseline:.4f}")
print()

# Step 6: Apply PCA to find all principal components
print("Step 6: Applying PCA to find all principal components")
print("-" * 80)
X_train_pca_full, X_test_pca_full, pca_full = apply_pca_full(X_train_scaled, X_test_scaled)
print("PCA applied successfully")
print(f"Total number of components: {pca_full.n_components_}")
print()
print("Explanation of n_components parameter:")
print("  - None: Keep all components (min(n_samples, n_features))")
print("  - Integer (e.g., 5): Keep specified number of components")
print("  - Float (e.g., 0.95): Keep components explaining specified variance ratio")
print("  - 'mle': Use Minka's MLE to automatically select components")
print()

# Step 7: Print explained variance ratios
print("Step 7: Explained Variance Ratios")
print("-" * 80)
explained_var = pca_full.explained_variance_ratio_
cumulative_var = np.cumsum(explained_var)

print("Explained Variance Ratio for each component:")
for i, var in enumerate(explained_var, 1):
    print(f"  PC{i}: {var:.4f} ({var*100:.2f}%)")

print("\nCumulative Explained Variance Ratios:")
for i, cum_var in enumerate(cumulative_var, 1):
    print(f"  PC1-PC{i}: {cum_var:.4f} ({cum_var*100:.2f}%)")
print()

# Step 8: Generate Scree Plots
print("Step 8: Generating Scree Plots")
print("-" * 80)
plot_scree_plots(explained_var, cumulative_var)
print("Scree plots saved as 'images/lab1_scree_plots.png'")

d = find_optimal_components(explained_var, VARIANCE_THRESHOLD)
print(f"\nOptimal number of components (d) for {VARIANCE_THRESHOLD*100:.0f}% variance: {d}")
print(f"Variance explained by {d} components: {cumulative_var[d-1]:.4f} ({cumulative_var[d-1]*100:.2f}%)")
print()

# Step 9: Re-run PCA with d components
print(f"Step 9: Re-running PCA with d={d} components")
print("-" * 80)
pca_final = PCA(n_components=d)
X_train_pca = pca_final.fit_transform(X_train_scaled)
X_test_pca = pca_final.transform(X_test_scaled)
print("PCA with optimal components applied successfully")
print(f"Original dimensions: {X_train_scaled.shape[1]}")
print(f"Reduced dimensions: {X_train_pca.shape[1]}")
print(f"Dimensionality reduction: {X_train_scaled.shape[1]} -> {d}")
print()

# Step 10: Apply Random Forest to reduced dataset
print("Step 10: Training Random Forest on PCA-reduced dataset")
print("-" * 80)
rf_pca = train_random_forest(X_train_pca, y_train)
cm_pca, acc_pca = evaluate_model(rf_pca, X_test_pca, y_test)
print("Model trained on PCA-reduced data successfully")
print("PCA Confusion Matrix:")
print(cm_pca)
print(f"PCA Accuracy: {acc_pca:.4f}")
print()

# Step 11: Print confusion matrices comparison
print("Step 11: Confusion Matrix Comparison")
print("-" * 80)
print("Before PCA (Baseline):")
print(cm_baseline)
print()
print("After PCA:")
print(cm_pca)
print()

# Step 12: Print accuracy comparison
print("Step 12: Accuracy Comparison")
print("-" * 80)
print(f"Accuracy before PCA: {acc_baseline:.4f} ({acc_baseline*100:.2f}%)")
print(f"Accuracy after PCA:  {acc_pca:.4f} ({acc_pca*100:.2f}%)")
print(f"Accuracy change:     {acc_pca - acc_baseline:+.4f} ({(acc_pca - acc_baseline)*100:+.2f}%)")
print(f"Dimensionality reduction: {X_train_scaled.shape[1]} -> {d} features")
print()

# Step 13: Plot first 2 principal components (2D)
print("Step 13: Plotting first 2 principal components (2D visualization)")
print("-" * 80)
plot_2d_pca(X_train_pca, y_train)
print("2D plot saved as 'images/lab1_pca_2d.png'")
print()

# Step 14: Plot first 3 principal components (3D)
print("Step 14: Plotting first 3 principal components (3D visualization)")
print("-" * 80)
plot_3d_pca(X_train_pca, y_train)
print("3D plot saved as 'images/lab1_pca_3d.png'")
print()

# Summary
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Original features: {X_train_scaled.shape[1]}")
print(f"Reduced features: {d}")
print(f"Variance retained: {cumulative_var[d-1]*100:.2f}%")
print(f"Baseline accuracy: {acc_baseline:.4f}")
print(f"PCA accuracy: {acc_pca:.4f}")
print(f"Accuracy change: {(acc_pca - acc_baseline)*100:+.2f}%")
print()
print("Lab 1 completed successfully!")
print("=" * 80)
print()

# Submission Reminder
print("SUBMISSION REMINDER:")
print("-" * 80)
print("1. Take screenshots of all plots and outputs")
print("2. Paste screenshots into Lab1_<firstname>.doc")
print("3. Include explanations for each step")
print("4. Submit answer document and this Python code to Brightspace")
print("5. DO NOT ZIP your files - submit separately")
print("=" * 80)
