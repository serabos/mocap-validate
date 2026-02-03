import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap

# File paths
mmc_file = ".../mmc_kinematics.xlsx"   # markerless kinematic data
mbmc_file = ".../mbmc_kinematics.xlsx"   # marker-based kinematic data

# Joint angles & wrist velocity
variables = [
    "shoulder flex-ext",
    "shoulder add-abd",
    "elbow flex-ext",
    "forearm sup-pronation", 
    "wrist flex-ext",
    "wrist velocity norm"
]

# Participants P02-13
participants = [f"P{p:02d}" for p in range(2, 14)]  # fixed list

# Load data
def load_numeric(file, sheet):
    df = pd.read_excel(file, sheet_name=sheet)
    df = df.iloc[1:]  # remove first row containing trial names
    df = df.apply(pd.to_numeric, errors="coerce")

    # Select only columns P02–P13
    df = df[participants]

    return df


# Compute mean and 95% confidence interval for all particiapnts
def mean_ci(df):
    arr = df.values.astype(float)

    mean = np.nanmean(arr, axis=1)
    sd = np.nanstd(arr, axis=1)

    n = np.sum(~np.isnan(arr), axis=1)
    se = sd / np.sqrt(n)

    ci_low = mean - 1.96 * se
    ci_high = mean + 1.96 * se

    return mean, ci_low, ci_high


# Plot findings
n = len(variables)
rows = 6
cols = 1

fig, axes = plt.subplots(rows, cols, figsize=(5, 11))
axes = axes.flatten()

labels = ["A", "B", "C", "D", "E", "F", "G"]

for i, var in enumerate(variables):
    ax = axes[i]

    # Load marker-based + markerless data
    df_mmc = load_numeric(mmc_file, var)
    df_mb = load_numeric(mbmc_file, var)

    # Movement cycle 0–100%
    cycle = np.linspace(0, 100, df_mmc.shape[0])

    # Stats
    mean_mmc, low_mmc, high_mmc = mean_ci(df_mmc)
    mean_mb, low_mb, high_mb = mean_ci(df_mb)

    # Plot for MBMC (orange)
    ax.plot(cycle, mean_mb, linewidth=2, color="orange", label="MBMC")
    ax.fill_between(cycle, low_mb, high_mb, color="orange", alpha=0.25)

    # Plot for MMC (blue)
    ax.plot(cycle, mean_mmc, linewidth=2, color="blue", label="MMMC")
    ax.fill_between(cycle, low_mmc, high_mmc, color="blue", alpha=0.25)

    if i < 5:
        ylabel = '\n'.join(wrap(var, width=9))+ str('(°)')
    else:
        ylabel = '\n'.join(wrap(var, width=9))+ str('(m/s)')

    # Formatting
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 50, 100])

    # ax.set_title(var, fontsize=13, fontweight="bold")
    # ax.set_xlabel("Movement cycle (%)")
    # ax.set_ylabel(variables[i], fontdict=dict(weight='bold') )
    ax.set_ylabel(ylabel, fontdict=dict(weight='bold'))
    ax.grid(True, alpha=0.3)

    # Panel label A/B/C/…
    ax.text(-0.19, 0.85, labels[i], fontsize=15, fontweight="bold", transform=ax.transAxes)

axes[-1].set_xlabel("Movement Cycle (%)")
axes[-1].legend(loc="upper right", fontsize=8)

# Remove unused subplot cells (if any)
for j in range(len(variables), len(axes)):
    fig.delaxes(axes[j])

fig.suptitle("Mean Joint Kinematics Across Participants", fontsize=13, fontweight="bold", ha="center")
plt.subplots_adjust(top=0.93)

plt.tight_layout()

# Save figure
output_path = "C:/Users/k2583179/PycharmProjects/mars-analysis/Draft Results/final_joint_panel.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")

print("Saved:", output_path)
