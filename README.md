# Motion Capture Validation Analysis

This pipeline compares markerless and marker-based motion capture systems to see how well they measure upper limb movements.

## What This Does

I built this tool to analyze kinematic data from two different motion capture systems:
- **MMC (Markerless Motion Capture)** - uses RGB cameras to track movement
- **MBMC (Marker-Based Motion Capture)** - the traditional gold standard with physical markers

The code processes data from 12 participants across 6 different joint movements and creates visualizations that show:
- How the two systems compare (mean angles with 95% confidence intervals)
- Where they differ (offset curves for each participant and overall)
- Whether the markerless system is accurate enough for clinical use

## What Gets Analyzed

The pipeline looks at these 6 movements:
1. Shoulder flexion-extension
2. Shoulder adduction-abduction
3. Elbow flexion-extension
4. Forearm supination-pronation
5. Wrist flexion-extension
6. Wrist velocity

## Requirements

You'll need these Python packages:
```
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
openpyxl>=3.0.0
```

Install them with:
```bash
pip install -r requirements.txt
```

## How to Use It

1. **Get your data ready**: You need Excel files with one sheet per movement type. Each sheet should have participants as columns (P02 through P13) and time-normalized data as rows.

2. **Update the file paths** at the top of `kinematic_comparison.py`:
```python
   MMC_FILE = "path/to/your/markerless_data.xlsx"
   MBMC_FILE = "path/to/your/markerbased_data.xlsx"
   OUTPUT_PATH = "where/you/want/the/figure.png"
```

3. **Run it**:
```bash
   python analysis/kinematic_comparison.py
```

## What You'll Get

The script creates a 6×2 panel figure where:
- **Left side**: Shows the mean movement curves for both systems with shaded confidence intervals (blue = markerless, orange = marker-based)
- **Right side**: Shows how much they differ at each point in the movement cycle (gray = individual participants, black = average difference)

## Note on Sample Data

I can't include sample data or output figures here because the data contains participant information. But the code is fully documented and ready to use with your own kinematic data

## Data Format

Your Excel files should be set up like this:
- One sheet per movement type (sheet names should match the movement variables)
- First row can have trial labels (the script skips this automatically)
- Columns labeled P02, P03, ... P13 for each participant
- Rows contain your time-normalized data (0-100% of the movement cycle)

## How It Works

The analysis:
1. Loads data from both Excel files
2. Calculates mean joint angles and 95% confidence intervals at each point in the movement cycle
3. Computes absolute differences between the two systems
4. Creates visualizations showing both the raw comparisons and the offset patterns

### What the Statistics Mean
- **Mean**: Average joint angle across all 12 participants at each time point
- **95% CI**: Range where we're 95% confident the true average falls
- **Offset**: How much the two systems differ at each point (measured in degrees or m/s for velocity)


## Why This Matters

Markerless motion capture is way more practical than marker-based systems—no suit-up time, cheaper equipment, easier for patients. But we need to make sure it's accurate enough for clinical decisions. This pipeline helps answer that question by showing exactly where and how much the systems differ.

## License

MIT License - feel free to use this for your own research or adapt it for different motion capture comparisons.
