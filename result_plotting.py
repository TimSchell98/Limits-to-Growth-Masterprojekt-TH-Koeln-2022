import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
from matplotlib.image import imread
from numpy import isnan



'''
Copied plotting function from the original PyWorld3 Package to make Changes in the Function

'''

def plot_world_variables_color_linestyle(time, var_data, var_names, var_lims, alpha, color, linestyle,
                         img_background=None,
                         title=None,
                         figsize=None,
                         dist_spines=0.09,
                         grid=False,
                         legend = True):
    """
    Plots world state from an instance of World3 or any single sector.

    """
    prop_cycle = plt.rcParams['axes.prop_cycle']
    # colors = prop_cycle.by_key()['color']

    var_number = len(var_data)

    fig, host = plt.subplots(figsize=figsize)
    axs = [host, ]
    for i in range(var_number-1):
        axs.append(host.twinx())

    fig.subplots_adjust(left=dist_spines*2)


    if img_background is not None:
        im = imread(img_background)
        axs[0].imshow(im, aspect="auto",
                      extent=[time[0], time[-1],
                              var_lims[0][0], var_lims[0][1]], cmap="gray")

    ps = []
    for ax, label, ydata, linestyle, alpha, color in zip(axs, var_names, var_data, linestyle, alpha, color):
        ps.append(ax.plot(time, ydata, label=label, color = color, linestyle=linestyle, alpha=alpha)[0])
    axs[0].grid(grid)
    axs[0].set_xlim(time[0], time[-1])

    for ax, lim in zip(axs, var_lims):
        ax.set_ylim(lim[0], lim[1])

    for ax_ in axs:
        formatter_ = EngFormatter(places=0, sep="\N{THIN SPACE}")
        ax_.tick_params(axis='y', rotation=90)
        ax_.yaxis.set_major_locator(plt.MaxNLocator(5))
        ax_.yaxis.set_major_formatter(formatter_)
        #ax_.legend()

    tkw = dict(size=4, width=1.5)
    axs[0].set_xlabel("time [years]")
    axs[0].tick_params(axis='x', **tkw)
    if legend:
        fig.legend(loc='upper right', bbox_to_anchor=(0.3, 0.75))

    if title is not None:
        #fig.suptitle(title, x=0.95, ha="right", fontsize=10)
        fig.suptitle(title, fontsize=14)

    #plt.tight_layout()

def plot_world_variables(time, var_data, var_names, var_lims, alpha,
                         img_background=None,
                         title=None,
                         figsize=None,
                         dist_spines=0.09,
                         grid=False):
    """
    Plots world state from an instance of World3 or any single sector.

    """
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    var_number = len(var_data)

    fig, host = plt.subplots(figsize=figsize)
    axs = [host, ]
    for i in range(var_number-1):
        axs.append(host.twinx())

    fig.subplots_adjust(left=dist_spines*2)
    for i, ax in enumerate(axs[1:]):
        ax.spines["left"].set_position(("axes", -(i + 1)*dist_spines))
        ax.spines["left"].set_visible(True)
        ax.yaxis.set_label_position('left')
        ax.yaxis.set_ticks_position('left')

    if img_background is not None:
        im = imread(img_background)
        axs[0].imshow(im, aspect="auto",
                      extent=[time[0], time[-1],
                              var_lims[0][0], var_lims[0][1]], cmap="gray")

    ps = []
    for ax, label, ydata, color, alpha in zip(axs, var_names, var_data, colors, alpha):
        ps.append(ax.plot(time, ydata, label=label, color=color, alpha=alpha)[0])
    axs[0].grid(grid)
    axs[0].set_xlim(time[0], time[-1])

    for ax, lim in zip(axs, var_lims):
        ax.set_ylim(lim[0], lim[1])

    for ax_ in axs:
        formatter_ = EngFormatter(places=0, sep="\N{THIN SPACE}")
        ax_.tick_params(axis='y', rotation=90)
        ax_.yaxis.set_major_locator(plt.MaxNLocator(5))
        ax_.yaxis.set_major_formatter(formatter_)

    tkw = dict(size=4, width=1.5)
    axs[0].set_xlabel("time [years]")
    axs[0].tick_params(axis='x', **tkw)
    for i, (ax, p) in enumerate(zip(axs, ps)):
        ax.set_ylabel(p.get_label(), rotation="vertical", fontsize='medium', horizontalalignment='right')
        ax.yaxis.label.set_color(p.get_color())
        ax.tick_params(axis='y', colors=p.get_color(), **tkw)
        ax.yaxis.set_label_coords(-i*dist_spines-0.05, 1)


    if title is not None:
        #fig.suptitle(title, x=0.95, ha="right", fontsize=10)
        fig.suptitle(title, fontsize=14)

    plt.tight_layout()

def plot_world_variables_color(time, var_data, var_names, var_lims, alpha, colors,
                         img_background=None,
                         title=None,
                         figsize=None,
                         dist_spines=0.09,
                         grid=False):
    """
    Plots world state from an instance of World3 or any single sector.

    """
    prop_cycle = plt.rcParams['axes.prop_cycle']
    #colors = prop_cycle.by_key()['color']

    var_number = len(var_data)

    fig, host = plt.subplots(figsize=figsize)
    axs = [host, ]
    for i in range(var_number-1):
        axs.append(host.twinx())

    fig.subplots_adjust(left=dist_spines*2)
    for i, ax in enumerate(axs[1:]):
        ax.spines["left"].set_position(("axes", -(i + 1)*dist_spines))
        ax.spines["left"].set_visible(True)
        ax.yaxis.set_label_position('left')
        ax.yaxis.set_ticks_position('left')

    if img_background is not None:
        im = imread(img_background)
        axs[0].imshow(im, aspect="auto",
                      extent=[time[0], time[-1],
                              var_lims[0][0], var_lims[0][1]], cmap="gray")

    ps = []
    for ax, label, ydata, color, alpha in zip(axs, var_names, var_data, colors, alpha):
        ps.append(ax.plot(time, ydata, label=label, color=color, alpha=alpha)[0])
    axs[0].grid(grid)
    axs[0].set_xlim(time[0], time[-1])

    for ax, lim in zip(axs, var_lims):
        ax.set_ylim(lim[0], lim[1])

    for ax_ in axs:
        formatter_ = EngFormatter(places=0, sep="\N{THIN SPACE}")
        ax_.tick_params(axis='y', rotation=90)
        ax_.yaxis.set_major_locator(plt.MaxNLocator(5))
        ax_.yaxis.set_major_formatter(formatter_)

    tkw = dict(size=4, width=1.5)
    axs[0].set_xlabel("time [years]")
    axs[0].tick_params(axis='x', **tkw)
    for i, (ax, p) in enumerate(zip(axs, ps)):
        ax.set_ylabel(p.get_label(), rotation="vertical", fontsize='medium', horizontalalignment='right')
        ax.yaxis.label.set_color(p.get_color())
        ax.tick_params(axis='y', colors=p.get_color(), **tkw)
        ax.yaxis.set_label_coords(-i*dist_spines-0.05, 1)


    if title is not None:
        #fig.suptitle(title, x=0.95, ha="right", fontsize=10)
        fig.suptitle(title, fontsize=14)

    plt.tight_layout()


def plot_world_variables_vc(time, var_data, var_names, var_lims, alpha,
                         img_background=None,
                         title=None,
                         figsize=None,
                         dist_spines=0.09,
                         grid=False):
    """
    Plots world state from an instance of World3 or any single sector.

    """
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    var_number = len(var_data)

    fig, host = plt.subplots(figsize=figsize)
    axs = [host, ]



    if img_background is not None:
        im = imread(img_background)
        axs[0].imshow(im, aspect="auto",
                      extent=[time[0], time[-1],
                              var_lims[0][0], var_lims[0][1]], cmap="gray")

    ps = []

    for label, ydata, color, alpha in zip(var_names, var_data, colors, alpha):
        ps.append(host.plot(time, ydata, label=label, color=color, alpha=alpha)[0])

    axs[0].grid(grid)
    axs[0].set_xlim(time[0], time[-1])

    for ax, lim in zip(axs, var_lims):
        ax.set_ylim(lim[0], lim[1])

    tkw = dict(size=4, width=1.5)
    axs[0].set_xlabel("time [years]")
    axs[0].tick_params(axis='x', **tkw)
    fig.legend(loc='center', bbox_to_anchor=(0.8, 0.82))

    if title is not None:
        fig.suptitle(title, fontsize=14)

    return fig, host
