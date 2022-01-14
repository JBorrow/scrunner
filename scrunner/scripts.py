"""
Basic objects describing scripts.
"""

from distutils.util import strtobool
from pathlib import Path
from typing import Any, List, Union

import attr


def anytobool(x: Any) -> bool:
    return bool(strtobool(str(x).lower()))


@attr.s(auto_attribs=True)
class Output:
    filename: str
    title: str
    description: str
    multi_output: bool = attr.ib(converter=anytobool)

    def get_paths(self, file_type: str, number_of_figures: int) -> list[Path]:
        """
        Gets the possible (relative) file paths for this script.

        Parameters
        ----------

        file_type: str
            The file extension of the outputs.

        number_of_figures: int
            The total number of outputs that will be used in the
            generation of this figure. If ``multi_output`` is true,
            the outputs will be numbered.


        Returns
        -------

        file_paths: list[Path]
            The (base, with no top level) file paths to the outputs
            from this script.

        Example
        -------

        If the internal ``filename`` is set to "test", and ``multi_output``
        is ``true`` then:

        .. code::python

           Output.get_paths(file_type="png", number_of_outputs=3)
           >>> ["test_0.png", "test_1.png", "test_2.png"]

        If ``multi_output`` is ``false``, then:

        .. code::python

           Output.get_paths(file_type="png", number_of_outputs=3)
           >>> ["test.png"]
        """

        if not self.multi_output:
            return [Path(f"{self.filename}.{file_type}")]
        else:
            return [
                Path(f"{self.filename}_{n}.{file_type}")
                for n in range(number_of_figures)
            ]

    def get_metadata(
        self, file_type: str, number_of_figures: int
    ) -> dict[str, Union[str, Path]]:
        """
        Gets expanded, and flattened, metadata as a dictionary.

        Parameters
        ----------

        file_type: str
            The file extension of the outputs.

        number_of_figures: int
            The total number of outputs that will be used in the
            generation of this figure. If ``multi_output`` is true,
            the outputs will be numbered.


        Returns
        -------

        metadata: dict[str, Union[str, Path]]
            A metadata dictionary for the output files that this will produce.
        """

        metadata = dict(
            filenames=self.get_paths(
                file_type=file_type, number_of_figures=number_of_figures
            ),
            title=self.title,
            description=self.description,
            multi_output=self.multi_output,
        )

        return metadata


@attr.s(auto_attribs=True)
class Script:
    name: Path
    created_by: str
    contact_email: str
    capture_stdout: bool = attr.ib(converter=anytobool)
    outputs: list[Output]

    def get_metadata(
        self,
        file_type: str,
        number_of_figures: int,
    ) -> list[dict[str, Union[str, Path]]]:
        """
        Gets expanded, and flattened, metadata, for each of the individual
        outputs, as a dictionary.

        Parameters
        ----------

        file_type: str
            The file extension of the outputs.

        number_of_figures: int
            The total number of outputs that will be used in the
            generation of this figure. If ``multi_output`` is true,
            the outputs will be numbered.


        Returns
        -------

        metadata: list[dict[str, Union[str, Path]]]
            A metadata dictionary for the output files that this script will produce.
        """

        return [
            output.get_metadata(
                file_type=file_type, number_of_figures=number_of_figures
            )
            for output in self.outputs
        ]
