---
name: learning-code_generation
description: Generate Python code and Jupyter notebooks for course assignments. Use when (1) user asks to generate code for lab/assignment, (2) mentions "生成代码" or "generate code", (3) needs to create .py or .ipynb files for coursework.
---

# Learning Code Generation

## Objectives

Generate well-structured, documented Python code for course assignments that meets academic requirements.

## Instructions

### 1. Understand Requirements

Before generating code:

- Read assignment document thoroughly
- Identify all required steps
- Note submission requirements (file format, naming, structure)
- Check for specific code style requirements

### 2. Code Structure

**For Python scripts (.py):**

```python
"""
Course Code Lab X: Title
Author: [Student Name]
Section: [Section Number]
Date: [Date]

Brief description of what the program does.

Innovations:
- Innovation 1
- Innovation 2
"""

# Step 1: Import libraries
import required_libraries

# Download data instructions (if needed)
# Comment out download commands with instructions

# Define functions with docstrings
def function_name(param1, param2):
    """
    Function description

    Args:
        param1 (type): Description
        param2 (type): Description

    Returns:
        type: Description
    """
    # Implementation
    pass

# Main program following assignment steps
# Step 2: ...
# Step 3: ...
```

**For Jupyter Notebooks (.ipynb):**

Structure:

1. **First Markdown Cell** - Title and metadata:

   ```markdown
   # Course Code Lab X: Title

   **Author:** [Student Name]  
   **Section:** [Section Number]  
   **Date:** [Date]

   ## Description

   Brief description of what the program does.

   ## Innovations

   - Innovation 1
   - Innovation 2
   ```

2. **Step Markdown Cells** - Each step gets its own markdown cell:

   ```markdown
   ## Step 1: Import Libraries

   Brief explanation of what this step does.
   ```

3. **Code Cells** - Implementation for each step:
   - One code cell per logical step
   - Include function definitions with docstrings
   - Add inline comments for clarity
   - Keep cells focused and not too long (< 50 lines)

4. **Output Cells** - Run all cells to show results:
   - Print statements show intermediate results
   - Plots display inline
   - DataFrames render as tables

5. **Final Markdown Cell** - Submission reminder:
   ```markdown
   ## Submission Reminder

   - Take screenshots of all plots/outputs
   - Save to Assignment.docx
   - etc.
   ```

**Jupyter-specific guidelines:**

- Use `# %%` magic comments if converting from .py
- Keep markdown cells concise (2-4 sentences)
- Run all cells before saving to show outputs
- Use `plt.show()` for plots (displays inline)
- Clear outputs if file size is too large

### 3. Code Requirements

**Must include:**

- ✅ File-level docstring with author, section, date
- ✅ Function docstrings with parameters and return values
- ✅ Meaningful variable names (descriptive, not x, y, z)
- ✅ Constants for magic numbers
- ✅ Comments explaining complex logic
- ✅ Proper spacing (2 lines between functions)
- ✅ Follow assignment step order exactly

**Language:**

- Code and variable names: English
- Comments: English
- Docstrings: English
- Print outputs: English
- All code content must be in English only

### 4. Common Patterns

**Pattern 1: Data Analysis Assignment**

```python
# Step 1: Import libraries
# Step 2: Load data
# Step 3: Preprocess data
# Step 4: Analysis
# Step 5: Visualization
# Step 6: Results and discussion
```

**Pattern 2: Algorithm Implementation**

```python
# Step 1: Import libraries
# Step 2: Define helper functions
# Step 3: Implement main algorithm
# Step 4: Test with examples
# Step 5: Performance analysis
```

**Pattern 3: Machine Learning Assignment**

```python
# Step 1: Import libraries
# Step 2: Load and explore data
# Step 3: Feature engineering
# Step 4: Train model
# Step 5: Evaluate model
# Step 6: Visualize results
```

### 5. File Organization

Follow assignment requirements:

```
assignment_folder/
├── assignment_name.py or .ipynb
├── Assignment.docx (with screenshots)
└── data/ (if needed)
```

### 6. Submission Checklist

Generate reminder at end of code:

```python
print("\nReminder:")
print("1. Take screenshots of all plots/outputs")
print("2. Save screenshots to Assignment.docx")
print("3. Complete discussion section")
print("4. Check file naming")
print("5. Create folder and compress")
print("6. Upload to specified platform")
```

### 7. Special Considerations

**Data downloads:**

- Comment out download commands
- Add instructions for first-time setup
- Check if data exists before downloading

**Plotting:**

- Use English labels for axes and titles
- Include grid for readability
- Use appropriate figure sizes
- Show plots with plt.show()

**Error handling:**

- Add try-except for file operations
- Validate input data
- Provide helpful error messages

## Validation

### Auto-Check Code Quality

After generating code, automatically check:

**1. Documentation Check:**

- [ ] File-level docstring exists with author, section, date
- [ ] All functions have docstrings
- [ ] Docstrings include parameter descriptions (Args:)
- [ ] Docstrings include return value descriptions (Returns:)

**2. Code Style Check:**

- [ ] Variable names are meaningful (not x, y, data1)
- [ ] Constants used for magic numbers
- [ ] Proper spacing (2 blank lines between functions)
- [ ] Comments in English
- [ ] Code and variable names in English

**3. Assignment Requirements Check:**

- [ ] Follows assignment step order exactly
- [ ] All required steps are implemented
- [ ] Submission reminder included at end
- [ ] File naming matches requirements
- [ ] Folder structure matches requirements

**4. Language Usage Check:**

- [ ] Comments: English
- [ ] Docstrings: English
- [ ] Print outputs: English
- [ ] Code/variables: English
- [ ] All code content in English only

### Check Report Format

After validation, provide report:

```
✅ Code Check Report

Documentation: ✅ Pass
- File-level docstring: ✅
- Function docstrings: ✅ (3/3)
- Parameter descriptions: ✅
- Return value descriptions: ✅

Code Style: ✅ Pass
- Variable naming: ✅ Meaningful names
- Constants usage: ✅
- Code spacing: ✅
- Comment language: ✅ English

Assignment Requirements: ✅ Pass
- Step order: ✅ Step 1-6
- Submission reminder: ✅
- File naming: ✅

Language Usage: ✅ Pass
- Comments: ✅ English
- Docstrings: ✅ English
- Print outputs: ✅ English
- Code: ✅ English

Summary: Code meets all requirements, ready to submit ✅
```

If issues found, report with fixes:

```
⚠️ Code Check Report

Documentation: ⚠️ Needs Improvement
- File-level docstring: ✅
- Function docstrings: ⚠️ (2/3) - calculate_frequency missing docstring
- Parameter descriptions: ❌ plot_results missing parameter descriptions

Suggested fixes:
1. Add docstring to calculate_frequency function
2. Add parameter descriptions to plot_results docstring

Please fix and re-check.
```

## Example Usage

**User request:** "生成Lab1的Python代码"

**Your workflow:**

1. Read the lab document to understand requirements
2. Identify all steps (Step 1, 2, 3...)
3. Generate code following exact step order
4. Add functions for repeated operations
5. Include complete docstrings
6. Add submission reminder
7. **Auto-check code quality** (run validation checklist)
8. **Provide check report** (show what passed/failed)
9. Fix any issues if found
10. Save to appropriate location

## Anti-Patterns (Avoid)

- ❌ Generating code without reading assignment requirements
- ❌ Using English comments for Chinese-speaking students
- ❌ Missing docstrings or incomplete parameter descriptions
- ❌ Not following assignment step order
- ❌ Using meaningless variable names (x, y, data1, data2)
- ❌ Forgetting submission requirements reminder
- ❌ Hardcoding values that should be constants
