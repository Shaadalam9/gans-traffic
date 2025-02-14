import time  # noqa:F401
import os
import re
import tqdm
import numpy as np
import multiprocessing
import plotly.graph_objects as go
from options.test_options import TestOptions
from data.data_loader import CreateDataLoader
from models.models import create_model
from util.visualizer import Visualizer
from util import html
from custom_logger import CustomLogger
from logmod import logs
import common

# Initialize logging
logs(show_level="info", show_color=True)
logger = CustomLogger(__name__)  # use custom logger

# Load the base data folder from the config
data = common.get_configs("data")
plotly_template = common.get_configs("plotly_template")


def main():
    opt = TestOptions().parse()
    opt.nThreads = 1   # test code only supports nThreads = 1
    opt.batchSize = 1  # test code only supports batchSize = 1
    opt.serial_batches = True  # no shuffle
    opt.no_flip = True  # no flip

    data_loader = CreateDataLoader(opt)
    dataset = data_loader.load_data()
    model = create_model(opt)
    visualizer = Visualizer(opt)

    # Create website
    if opt.split != "":
        web_dir = os.path.join(opt.results_dir, opt.name, '%s_%s_%s' % (opt.phase, opt.split, opt.which_epoch))
    else:
        web_dir = os.path.join(opt.results_dir, opt.name, '%s_%s' % (opt.phase, opt.which_epoch))

    webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.which_epoch))

    for i, data in tqdm.tqdm(enumerate(dataset), total=len(dataset)):
        if i >= opt.how_many:
            break
        model.set_input(data)
        model.test()
        visuals = model.get_current_visuals()
        img_path = model.get_image_paths()
        visualizer.save_images(webpage, visuals, img_path)

    webpage.save()

    # After testing, generate the plot
    generate_plot()


def generate_plot():
    data_file = os.path.join(data, 'v2c_experiment', 'loss_log.txt')

    # Read the log file
    with open(data_file, "r") as file:
        log_data = file.readlines()

    # Variables to store parsed data
    iters = []
    variables_data = {
        "D_A": [], "G_A": [], "Cyc_A": [], "UnCyc_A": [], "Unsup_A": [], "Cont_A": [], "Idt_A": [],
        "D_B": [], "G_B": [], "Cyc_B": [], "UnCyc_B": [], "Unsup_B": [], "Cont_B": [], "Idt_B": []
    }

    variable_colors = {
        "D_A": (0, 0, 255), "G_A": (0, 128, 0), "Cyc_A": (255, 0, 0), "UnCyc_A": (128, 0, 128),
        "Unsup_A": (255, 165, 0), "Cont_A": (0, 255, 255), "Idt_A": (255, 0, 255),
        "D_B": (0, 128, 128), "G_B": (165, 42, 42), "Cyc_B": (255, 192, 203), "UnCyc_B": (128, 128, 128),
        "Unsup_B": (255, 215, 0), "Cont_B": (50, 205, 50), "Idt_B": (0, 0, 128)
    }

    # Parse the log data for epoch 1
    for line in log_data:
        if "(epoch: 1" in line:
            iter_match = re.search(r"iters: (\d+)", line)
            if iter_match:
                current_iter = int(iter_match.group(1))
                iters.append(current_iter)

            for var in variables_data.keys():
                match = re.search(fr"{var}: ([\d\.]+)", line)
                if match:
                    variables_data[var].append(float(match.group(1)))

    window_size = 100
    averages, variances, upper_bounds, lower_bounds = {}, {}, {}, {}

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

    fig = go.Figure()

    for var, values in variables_data.items():
        color = variable_colors[var]

        fig.add_trace(go.Scatter(
            x=iters + iters[::-1],
            y=upper_bounds[var] + lower_bounds[var][::-1],
            fill='toself',
            fillcolor=f'rgba({color[0]}, {color[1]}, {color[2]}, 0.1)',
            line=dict(color='rgba(0, 0, 0, 0)'),
            legendgroup=var,
            name=var,
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=iters,
            y=averages[var],
            mode='lines',
            name=var,
            line=dict(color=f'rgb({color[0]}, {color[1]}, {color[2]})'),
            legendgroup=var,
            showlegend=True
        ))

    fig.update_layout(
        xaxis={'title': {'text': "Iterations", 'font': {'size': 38}}, 'tickfont': {'size': 30}},
        yaxis={'title': {'text': "Values", 'font': {'size': 38}}, 'tickfont': {'size': 30}, 'range': [-5, 5]},
        legend={
            'font': {'size': 22}, 'orientation': 'h', 'x': 0.55, 'y': 0.1, 'xanchor': 'center', 'yanchor': 'top'
        },
        template=plotly_template,
    )
    fig.show()

    figures_dir = os.path.join(data, 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    fig.write_image(os.path.join(figures_dir, "plot.png"), width=1600, height=1200, scale=3)
    fig.write_image(os.path.join(figures_dir, "plot.eps"))
    fig.write_html(os.path.join(figures_dir, "plot.html"))


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
