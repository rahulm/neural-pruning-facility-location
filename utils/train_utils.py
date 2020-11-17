"""Some utils for training, checkpointing, etc. of models."""

import csv
import os
from typing import List, Text

import matplotlib.pyplot as plt

FILE_NAME_CSV: Text = "vals.csv"
FILE_NAME_PLOT: Text = "plot.png"


class StatCounter:
    def __init__(self) -> None:
        self._counter: List[float] = []

    def add(self, val: float) -> None:
        self._counter.append(val)

    def save(
        self,
        folder_path: Text,
        file_prefix: Text = "",
        xlabel: Text = "iteration",
        ylabel: Text = "loss",
        title_prefix: Text = "",
        index_offset: int = 1,
        index_multiplier: int = 1,
    ) -> None:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Make index (x axis).
        indices: List[int] = [
            (index_multiplier * (i + index_offset))
            for i in range(len(self._counter))
        ]

        file_prefix = "{}-".format(file_prefix) if file_prefix else ""

        # Save CSV.
        with open(
            os.path.join(
                folder_path, "{}{}".format(file_prefix, FILE_NAME_CSV)
            ),
            "w",
            newline="",
        ) as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([xlabel, ylabel])
            for ind, val in zip(indices, self._counter):
                writer.writerow([ind, val])

        # Save plot.
        title: Text = (
            "{}{}".format(
                "" if (not title_prefix) else "{} - ".format(title_prefix),
                "{} per {}".format(ylabel.capitalize(), xlabel.capitalize()),
            )
        )
        plt.figure()
        plt.plot(indices, self._counter)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.savefig(
            os.path.join(
                folder_path, "{}{}".format(file_prefix, FILE_NAME_PLOT)
            )
        )

