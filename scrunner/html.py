"""
Functions that aid in the production of the HTML webpages.
"""

from pathlib import Path
from time import strftime
from typing import Optional, Union

import unyt
from jinja2 import Environment, PackageLoader, select_autoescape

from scrunner import __version__


def format_number(number):
    """
    Formats a number from float (with or without units) to a latex-like number.
    """

    try:
        units = f"\\; {number.units.latex_repr}"
    except:
        units = ""

    try:
        mantissa, exponent = ("%.3g" % number).split("e+")
        exponent = f" \\times 10^{{{int(exponent)}}}"
    except:
        mantissa = "%.3g" % number
        exponent = ""

    return f"\\({mantissa}{exponent}{units}\\)"


def get_if_present_float(dictionary, value: str, input_unit=None, output_unit=None):
    """
    A replacement for .get() that also formats the number if present.
    Assumes data should be a float.
    """

    try:
        value = float(dictionary[value])

        if input_unit is not None:
            value = unyt.unyt_quantity(value, input_unit)

            if output_unit is not None:
                value.convert_to_units(output_unit)

        return format_number(value)
    except KeyError:
        return ""


def get_if_present_int(dictionary, value: str, input_unit=None, output_unit=None):
    """
    A replacement for .get() that also formats the number if present.
    Assumes data should be an integer.
    """

    try:
        value = int(dictionary[value])

        if input_unit is not None:
            value = unyt.unyt_quantity(value, input_unit)

            if output_unit is not None:
                value.convert_to_units(output_unit)

        return format_number(value)
    except KeyError:
        return ""


def camel_to_title(string):
    return string.title().replace("_", " ")


class WebpageCreator(object):
    """
    Creates webpages based on the information that is provided in
    the plots metadata through the autoplotter and the additional
    plotting interface provided through the pipeline.
    """

    environment: Environment
    loader: PackageLoader

    variables: dict
    html: str

    def __init__(self):
        """
        Sets up the ``jinja`` templating system.
        """

        self.loader = PackageLoader("scrunner", "templates")
        self.environment = Environment(
            loader=self.loader, autoescape=select_autoescape(["js"])
        )

        # Initialise empty variables dictionary, with the versions of
        # this package and the velociraptor package used.
        self.variables = dict(
            scrunner_version=__version__,
            creation_date=strftime(r"%Y-%m-%d"),
            sections={},
            runs=[],
        )

        return

    def render_webpage(self, template: str = "plot_viewer.html") -> str:
        """
        Renders a webpage based on the internal variables stored in
        the ``variables`` dictionary.
        Parameters
        ----------
        template: str
            The name of the template that you wish to use. Defaults to
            "plot_viewer.html".
        Returns
        -------
        html: str
            The resulting HTML. This is also stored in ``.html``.
        """

        self.html = self.environment.get_template(template, parent="base.html").render(
            **self.variables
        )

        return self.html

    def add_metadata(self, page_name: str, additional_text: Optional[str] = None):
        """
        Add additional metadata to the page.
        Parameters
        ----------
        page_name: str
            Name to put in the page title.
        """

        if additional_text is not None:
            self.variables.update(
                dict(additional_text=additional_text),
            )

        self.variables.update(dict(page_name=page_name))

    def add_plots(
        self,
        data: list[dict[str, Union[str, Path]]],
        output_directory: Optional[Path] = None,
    ):
        """
        Adds the auto plotter metadata to the section / plot metadata.

        Parameters
        ----------

        data: list[dict[str, Union[str, Path]]]
            Result of ``runner.get_metadata()``.

        output_directory: Path, optional
            Output directory that contains the figures. If this
            is provided, only created figures will be displayed
            on the webpage. If not, then the page will contain
            blank spaces where failed plots should live (can be
            useful for debugging).
        """

        self.data = data

        output = {}

        for plot in data:
            if output_directory is not None:
                valid_filenames = [
                    x for x in plot["filenames"] if (output_directory / x).exists()
                ]
            else:
                valid_filenames = plot["filenames"]

            if len(valid_filenames) > 0:
                hash_and_filenames = {
                    x: f"plot{abs(hash(str(x)))}" for x in valid_filenames
                }

                temp_output = plot.copy()
                temp_output["filenames"] = hash_and_filenames

                temp_output["id"] = f"sec{abs(hash(plot['title']))}"

                output[plot["title"]] = temp_output

        self.variables["sections"] = output

        return

    def save_html(self, filename: str):
        """
        Saves the html in ``self.html`` to the filename provided.
        Parameters
        ----------
        filename: str
            Full filename (including file path) to save the HTML as.
        """

        with open(filename, "w") as handle:
            handle.write(self.html)
