"""
Script that plots x against y.

---
{
    "name": "file_name.py",
    "created_by": "Josh Borrow",
    "contact_email": "borrowj@mit.edu", 
    "outputs": [
        {
            "filename": "x_against_y",
            "title": "X against Y",
            "description": "Plots the first column of the file against the second column",
            "multi_output": "True"
        }
    ]
}
---
"""

from scrunner import ScriptArgumentParser

import matplotlib.pyplot as plt
import numpy as np

arguments = ScriptArgumentParser()
plt.style.use(arguments.stylesheet)

loaded_data = [np.loadtxt(x, delimiter=",") for x in arguments.data]

for n, data in enumerate(loaded_data):
    fig, ax = plt.subplots()

    ax.plot(data[:, 0], data[:, 1])

    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")

    fig.savefig(arguments.output_directory / f"x_against_y_{n}.{arguments.file_type}")
