"""
Argument parsing wrapper for the scripts, to make sure that
they conform to the correct API.
"""

import argparse as ap
from pathlib import Path
from typing import Optional

import attr


@attr.s(auto_attribs=False)
class ScriptArgumentParser:
    """
    Script argument parser for ``scrunner`` additional scripts.
    They must conform to the following command-line api:
    + ``-d``: List of input data files
    + ``-o``: Output directory for the figure.
    + ``-f``: File type that the figures should be output with.
    + ``-n``: Number of figures to create.
    + ``-s``: Matplotlib stylesheet to use.
    """

    parser: ap.ArgumentParser

    data: list[Path]
    output_directory: Path
    file_type: str
    number_of_figures: int
    stylesheet: str

    def __attrs_post_init__(self):
        """
        Initialises the argument parser object and parses the args, as they say.
        """

        self.setup_parser()
        self.parse_arguments()

        return

    def setup_parser(self):
        """
        Set up the argument parser.
        """

        self.parser = ap.ArgumentParser()

        self.parser.add_argument(
            "-d",
            "--data",
            help="Data input files. Example: test_0.hdf5 test_1.hdf5",
            type=Path,
            required=True,
            nargs="*",
        )

        self.parser.add_argument(
            "-o",
            "--output-directory",
            help="Output directory for the produced figures.",
            type=Path,
            required=True,
        )

        self.parser.add_argument(
            "-f",
            "--file-type",
            help="File type (extension) for the output files",
            type=str,
            required=True,
        )

        self.parser.add_argument(
            "-n",
            "--number-of-figures",
            help="Number of figures to create with this script.",
            type=int,
            required=True,
        )

        self.parser.add_argument(
            "-s",
            "--stylesheet",
            help="Matplotlib stylesheet to use",
            type=str,
            required=False,
            default="default",
        )

        return

    def parse_arguments(self):
        """
        Parses the arguments from the ``parser``.
        """

        args = self.parser.parse_args()

        self.data = args.data
        self.output_directory = args.output_directory
        self.file_type = args.file_type
        self.number_of_figures = args.number_of_figures
        self.stylesheet = args.stylesheet

    def get_filename_for_output(
        self, base_name: str, output_number: Optional[int] = None
    ) -> Path:
        """
        Gets the filename, including output path, for a given
        output number.

        Parameters
        ----------

        base_name: str
            The base name of the file, for instance ``plot_example``.
            This will be converted to ``output_path/plot_example_0.file_type``

        output_number: Optional[int]
            The output number that this file corresponds to. If this is
            not a multi-output figure, do not supply this argument.

        Returns
        -------

        Path
            The ``pathlib`` object at which the figure should be
            saved at.
        """

        if output_number is not None:
            return (
                self.output_directory / f"{base_name}_{output_number}.{self.file_type}"
            )
        else:
            return self.output_directory / f"{base_name}.{self.file_type}"
