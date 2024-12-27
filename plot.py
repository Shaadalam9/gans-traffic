import re
import plotly.graph_objects as go
import numpy as np

# Read the log file
data_file = "loss_log.txt"
with open(data_file, "r") as file:
    log_data = file.readlines()

# Variables to store parsed data
iters = []
variables_data = {  # Dictionary to store data for the specified variables
    "D_A": [],
    "G_A": [],
    "Cyc_A": [],
    "UnCyc_A": [],
    "Unsup_A": [],
    "Cont_A": [],
    "Idt_A": [],
    "D_B": [],
    "G_B": [],
    "Cyc_B": [],
    "UnCyc_B": [],
    "Unsup_B": [],
    "Cont_B": [],
    "Idt_B": []
}

# Define colors for each variable
variable_colors = {
    "D_A": (0, 0, 255),  # Blue
    "G_A": (0, 128, 0),  # Green
    "Cyc_A": (255, 0, 0),  # Red
    "UnCyc_A": (128, 0, 128),  # Purple
    "Unsup_A": (255, 165, 0),  # Orange
    "Cont_A": (0, 255, 255),  # Cyan
    "Idt_A": (255, 0, 255),  # Magenta
    "D_B": (0, 128, 128),  # Teal
    "G_B": (165, 42, 42),  # Brown
    "Cyc_B": (255, 192, 203),  # Pink
    "UnCyc_B": (128, 128, 128),  # Gray
    "Unsup_B": (255, 215, 0),  # Gold
    "Cont_B": (50, 205, 50),  # Lime
    "Idt_B": (0, 0, 128)  # Navy
}

# Parse the log data for epoch 1
for line in log_data:
    if "(epoch: 1" in line:  # Only consider lines for epoch 1
        # Extract iteration
        iter_match = re.search(r"iters: (\d+)", line)
        if iter_match:
            current_iter = int(iter_match.group(1))
            iters.append(current_iter)

        # Extract specified variables
        for var in variables_data.keys():
            match = re.search(fr"{var}: ([\d\.]+)", line)
            if match:
                variables_data[var].append(float(match.group(1)))

# Calculate the average and variance for each variable
window_size = 100
averages = {}
variances = {}
upper_bounds = {}
lower_bounds = {}

for var, values in variables_data.items():
    averages[var] = [
        np.mean(values[max(0, i - window_size + 1):i + 1]) for i in range(len(values))
    ]
    variances[var] = [
        np.var(values[max(0, i - window_size + 1):i + 1]) for i in range(len(values))
    ]
    upper_bounds[var] = [
        avg + np.sqrt(var) for avg, var in zip(averages[var], variances[var])
    ]
    lower_bounds[var] = [
        avg - np.sqrt(var) for avg, var in zip(averages[var], variances[var])
    ]

# Create the Plotly plot
fig = go.Figure()

# Add traces for each specified variable
for var, values in variables_data.items():
    # Get the color for this variable
    color = variable_colors[var]  # Ensure color is a tuple (R, G, B)

    # Add variance shading (background)
    fig.add_trace(go.Scatter(
        x=iters + iters[::-1],  # x values (forward + reverse for shading)
        y=upper_bounds[var] + lower_bounds[var][::-1],  # Upper + reversed lower bounds
        fill='toself',
        fillcolor=f'rgba({color[0]}, {color[1]}, {color[2]}, 0.1)',  # Light shading with transparency
        line=dict(color='rgba(0, 0, 0, 0)'),  # No border line
        legendgroup=var,  # Group with the solid line
        name=var,  # Legend label
        showlegend=False  # Hide from legend (use solid line's legend entry)
    ))

    # Add dynamic average line (solid line)
    fig.add_trace(go.Scatter(
        x=iters,
        y=averages[var],
        mode='lines',
        name=var,  # Legend label for variable
        line=dict(color=f'rgb({color[0]}, {color[1]}, {color[2]})'),  # Solid color for the line
        legendgroup=var,  # Group with the background
        showlegend=True  # Show in legend
    ))

# Add labels and title
fig.update_layout(
    title={
        'text': "Specified Variables vs. Iterations (Epoch 1, Variance Shaded)",
        'font': {'size': 24}
    },
    xaxis={
        'title': {'text': "Iterations", 'font': {'size': 18}},
        'tickfont': {'size': 14}
    },
    yaxis={
        'title': {'text': "Values", 'font': {'size': 18}},
        'tickfont': {'size': 14}
    },
    legend={
        'font': {'size': 16},
        'x': 0.887,  # X-coordinate for the legend
        'y': 0.986   # Y-coordinate for the legend
    },
    template="plotly_white"
)

# Show the plot
fig.show()
