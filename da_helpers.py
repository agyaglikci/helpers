import argparse
import gzip
import os
import sys
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
matplotlib.pyplot.switch_backend('Agg')

# color_list = [
#   "#1abc9c","#f1c40f",
#   "#2ecc71","#e67e22",
#   "#16a085","#f39c12",
#   "#27ae60","#d35400",
#   "#3498db","#e74c3c",
#   "#2980b9","#c0392b",
#   "#9b59b6","#ecf0f1",
#   "#8e44ad","#bdc3c7",
#   "#34495e","#95a5a6",
#   "#2c3e50","#7f8c8d"
# ]

color_list = list(reversed(list(sns.color_palette('colorblind'))))

def create_path_parser(path_sections):
    path_parse_indices = {}
    prev_section = ""
    for section_index, section in enumerate(path_sections):
        if section == prev_section:
            path_parse_indices[section][1] = section_index
        else:
            path_parse_indices[section] = [section_index] * 2
        prev_section = section

    return path_parse_indices


def normalize_and_stack(row, cols):
    total = float(sum([row[col] for col in cols]))
    base = 0
    for col in cols:
        row[col] = row[col] / total + base
        base = row[col]
    return row

def just_stack(row, cols):
    total = float(sum([row[col] for col in cols]))
    base = 0
    for col in cols:
        row[col] = row[col] + base
        base = row[col]
    return row

def normalize_within_row(row, cols):
    total = float(sum([row[col] for col in cols]))
    for col in reversed(cols):
        row[col] = row[col] / total
    return row


def sns_stack_plot(df, ax, x_col, y_cols, x_title, y_title, file_name, normalize=True):
    # Parameters
    barWidth = 0.85

    # print df
    if normalize:
        df = df.apply(lambda row: normalize_and_stack(row, y_cols), axis=1)
    else:
        df = df.apply(lambda row: just_stack(row, y_cols), axis=1)
    # print df

    # plot
    # xtick_labels = df[x_col]
    # xtick_values = range(len(xtick_labels))

    for i, ycol in enumerate(reversed(y_cols)):
        color = color_list[i%len(color_list)]
        sns.barplot(x=x_col, y=ycol, data=df,
            label=ycol, color=color, ax=ax)
        # ax.bar(xtick_values, df[ycol], color=color, edgecolor='white', width=barWidth)
    ax.legend(loc="lower right", frameon=True)
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    # plt.xticks(xtick_values, xtick_labels)
    plt.legend(loc='best')
    #ax.xlabel(x_title)
    #ax.ylabel(y_title)
    return ax


def filter_columns(df, cols):
    _df = df.apply(lambda row: normalize_within_row(row, cols), axis=1)

    # initialize a dictionary with the cumulative effect of each column
    col_coverages = {}
    sum_coverages = 0
    for col in cols:
        col_coverages[col] = sum(_df[_df[col] >= 0][col])
        sum_coverages += col_coverages[col]

    cum_coverage = num_components = 0
    target_coverage = sum_coverages * 0.9999
    filtered_cols = []
    for key, value in reversed(sorted(col_coverages.iteritems(), key=lambda (k,v): (v,k))):
        if (value == 0) or (cum_coverage >= target_coverage) or (num_components == len(color_list)):
            break

        else:
            cum_coverage += value
            filtered_cols.append(key)
            num_components += 1

    return filtered_cols
