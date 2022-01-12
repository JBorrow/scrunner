"""
Script that plots x against z.

---
{
    "name": "file_name.py",
    "created_by": "Josh Borrow",
    "contact_email": "borrowj@mit.edu", 
    "outputs": [
        {
            "filename": "x_against_z",
            "title": "X against Z",
            "description": "Plots the first column of the file against the third column",
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

    ax.plot(data[:, 0], data[:, 2])

    ax.set_xlabel("$x$")
    ax.set_ylabel("$z$")

    fig.savefig(arguments.get_filename_for_output("x_against_z", n))
