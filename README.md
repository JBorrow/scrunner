ScRunner
========

ScRunner is a script runner for python.

It specialises in running a repeated set of analysis scripts on similar data,
and allows you to collect scripts together with metadata for easy
comparisons.

The scripts must all use the same argument parser API, and
must contain frontmatter in the docstring to describe the figures
that will be made.

These figures can then be combined together into a webpage for easy
viewing. ScRunner is a simplified, generalised, version of the
[`swift-pipeline`](https://github.com/swiftsim/pipeline), along
with [PagePlot](https://github.com/jborrow/pageplot).

Requirements
------------

This package only has two requirements:

+ `attrs`
+ `jinja2`

Script API
----------

Scripts must include frontmatter in their docstring, as follows (with
examples):

```python
"""
Basic script description

---
{
"name": "test_script.py",
"created_by": "Josh Borrow",
"contact_email": "borrowj@mit.edu",
"capture_stdout": "True",
"outputs": [
    {
        "filename": "stellar_density_image",
        "title": "Stellar Halo Image",
        "description": "Projected stellar density through entire selected volume (as a 2D histogram). Haloes with $M_* > 10^6$ M$_\\odot$ are shown as points.",
        "multi_output": "False"
    },
    {
        "filename": "stellar_density_image_individual",
        "title": "Stellar Halo Image",
        "description": "Projected stellar density for individual objects",
        "multi_output": "True"
    }
],
"ancillary_outputs": [
    {
        "filename": "parameters.txt",
        "title": "Runtime Parameters"
    },
    {
        "filename": "config.txt",
        "title": "Compile-time Parameters"
    }
]
}
---
```

The frontmatter should be valid JSON (i.e. it must not have
trailing commas).

This script should then produce two sets of figures (listed in "outputs"),
and two additional outputs ("parameters.txt" and "config.txt"). The first,
a single figure, called `stellar_density_image.png` (or other given
file extension, decided at runtime), and a series of figures called
`stellar_density_image_individual_0.png` up to a number determined
at run time. If "capture_stdout" is `True`, then the standard output
of this script will be captured and displayed at the top of the webpage.
It is suggested that the script prints valid HTML.

Within the script, the `ScriptArgumentParser` must be used, as
follows:

```python
from scrunner import ScriptArgumentParser
arguments = ScriptArgumentParser()
```

The `arguments` instance will then take a number
of command-line arguments, as follows:

```
usage: star_images.py [-h] -d [DATA ...] -o OUTPUT_DIRECTORY -f FILE_TYPE -n
                      NUMBER_OF_FIGURES [-s STYLESHEET]

optional arguments:
  -h, --help            show this help message and exit
  -d [DATA ...], --data [DATA ...]
                        Data input files. Example: test_0.hdf5 test_1.hdf5
  -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        Output directory for the produced figures.
  -f FILE_TYPE, --file-type FILE_TYPE
                        File type (extension) for the output files
  -n NUMBER_OF_FIGURES, --number-of-figures NUMBER_OF_FIGURES
                        Number of figures to create with this script.
  -s STYLESHEET, --stylesheet STYLESHEET
                        Matplotlib stylesheet to use
```

These should be accessed and used within the script in
the folowing ways:

### Data

The data argument will be a list of data paths, received from the
main script runner (see later). These will be given in the same
order to all scripts.

```python
arguments.data
>>> [PosixPath("./DataFileOne.hdf5"), PosixPath("./DataFileTwo.hdf5")]
```

### Number of Figures

The number of figures is simply an integer describing the number
of figures that plots tagged with `"multi_output": "true"` should
output. The webpage will expect this many figures.

```
arguments.number_of_figures
>>> 5
```

### Matplotlib Stylesheet

To ensure a consistent stylesheet across your output figures,
it is highly recommended that you use the stylesheet argument
in your script:

```python
import matplotlib.pyplot as plt
plt.style.use(arguments.stylesheet)
```

### Saving Figures

There are two arguments that the script argument parser
takes, `output_directory`, and `file_type`. It's recommended
that, instead of using these yourself, you use the provided
`get_filename_for_output` method:

```python
arguments.get_filename_for_output(
    base_name="stellar_density_image"
)
>>> PosixPath("output_path/stellar_density_image.png")

arguments.get_filename_for_output(
    base_name="stellar_density_image_individual",
    output_number=3,
)
>>> PosixPath("output_path/stellar_density_image_individual_3.png")
```

Not providing the `output_number` argument provides the
file path for a non-multi-output figure.

Ancillary outputs should make use of the `arguments.output_directory`
to save to the correct location.


Running Scripts
---------------

Running a collection of scripts is as simple as placing
them all in the same directory, and using the command-line
tool `scrun`:

```
scrun \
  -d data_file_one.csv data_file_two.csv \
  -p /home/josh/scripts_to_run \
  -o ./my_outputs/output_7 \
  -f png \
  -n 3 \
  -s /home/josh/stylesheet.mplstyle
```

Where all of these will be passed as expected through to the
scripts, except for `-r` which is the directory containing all
scripts to run.

In your output folder, which will be created if it does not exist,
you will find an `index.html` file, which provides a summary of
your outputs.

On completion, `scrun` will print:
```
Successfully completed 2 scripts
There were 0 failures
There were 0 scripts that raised warnings
```
and individual stdout and stderr from your scripts,
if they raise a warning or fail.