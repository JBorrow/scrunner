"""
Script runner main object.
"""

import json
import sys
from pathlib import Path
from subprocess import CalledProcessError, run
from time import perf_counter
from typing import Optional, Union

import attr

from scrunner.scripts import Output, Script


@attr.s(auto_attribs=False)
class ScriptRunner:
    """
    Parses and runs scripts in a given directory.

    First, it searches the ``path`` that is given for
    python scripts that contain valid frontmatter.

    Then, it generates ``Script`` objects for each of
    these scripts.

    The scripts can be ran by using the ``run`` method
    with appropriate arguments, that will in turn be passed
    down to the scripts.
    """

    path = attr.ib(type=Path, converter=Path)
    scripts: list[Script]
    script_paths: list[Path]
    captured_stdout: str

    def __attrs_post_init__(self):
        """
        Search for and store the information about the scripts.
        """

        self.scripts, self.script_paths = self.parse_scripts()
        self.captured_stdout = ""

    def parse_scripts(self) -> list[Script]:
        """
        Parses scripts in directory.
        """

        scripts = []
        script_paths = []

        for script_filename in self.path.glob("*.py"):
            with open(script_filename, "r") as handle:
                # Check if first line is a comment, if not we
                # should skip.

                first_line = handle.readline()

                if '"""' not in first_line:
                    continue

                started_frontmatter = False
                frontmatter = []

                for line in handle:
                    if "---" in line:
                        if started_frontmatter:
                            # We've read all the frontmatter
                            break
                        else:
                            started_frontmatter = True
                    elif started_frontmatter:
                        frontmatter.append(line)
                    elif '"""' in line:
                        # Somebody forgot to end the frontmatter
                        break
                    else:
                        continue

            try:
                parsed_frontmatter = json.loads("".join(frontmatter))
            except json.decoder.JSONDecodeError:
                raise RuntimeError(
                    f"Unable to parse JSON frontmatter in {script_filename}."
                )

            parsed_script = Script(
                name=parsed_frontmatter["name"],
                created_by=parsed_frontmatter.get("created_by", "Unknown"),
                contact_email=parsed_frontmatter.get("contact_email", "Unknown"),
                capture_stdout=parsed_frontmatter.get("capture_stdout", False),
                outputs=[
                    Output(
                        filename=output["filename"],
                        title=output["title"],
                        description=output["description"],
                        multi_output=output["multi_output"],
                    )
                    for output in parsed_frontmatter.get("outputs", [])
                ],
            )

            scripts.append(parsed_script)
            script_paths.append(script_filename)

        return scripts, script_paths

    def get_metadata(
        self, file_type: str, number_of_figures: int
    ) -> list[dict[str, Union[str, Path]]]:
        """
        Gets expanded, and flattened, metadata as a list of
        dictionaries for each script.

        Parameters
        ----------

        file_type: str
            The file extension of the outputs.

        number_of_figures: int
            The total number of outputs that will be used in the
            generation of these figures. If ``multi_output`` is true,
            the outputs will be numbered.


        Returns
        -------

        metadata: list[dict[str, Union[str, Path]]]
            A metadata dictionary for the output files that this will produce.
        """
        metadata = []

        for script in self.scripts:
            metadata = metadata + script.get_metadata(
                file_type=file_type,
                number_of_figures=number_of_figures,
            )

        return metadata

    def run(
        self,
        data: list[Path],
        output_directory: Path,
        file_type: str,
        number_of_figures: int,
        stylesheet: str,
        interpreter: Optional[str] = None,
    ):
        """
        Run the scripts!

        Parameters
        ----------

        data: list[Path]
            Paths to the data files.

        otuput_directory: Path
            The path in which you would like to save the
            data. It must exist.

        file_type: str
            The file type (extension) to save all figures to.

        number_of_figures: int
            The number of figures that each script should
            produce.

        stylesheet: str
            The matplotlib stylesheet to use.
        """

        arguments = [
            "-d",
            *[str(d) for d in data],
            "-o",
            str(output_directory),
            "-f",
            str(file_type),
            "-n",
            str(number_of_figures),
            "-s",
            str(stylesheet),
        ]

        interpreter = sys.executable if interpreter is None else interpreter

        failures = []
        warnings = []
        n_failures = 0
        n_warnings = 0

        for script, script_path in zip(self.scripts, self.script_paths):
            start = perf_counter()

            to_run = [
                str(interpreter),
                str(script_path),
                *arguments,
            ]

            complete = run(
                to_run,
                capture_output=True,
                encoding="utf-8",
                check=False,
            )
            end = perf_counter()

            script_time = end - start

            output_text = (
                f"Output:\n{complete.stdout}\n" if len(complete.stdout) > 0 else ""
            )
            error_text = (
                f"Errors:\n{complete.stderr}\n" if len(complete.stderr) > 0 else ""
            )

            try:
                complete.check_returncode()
                if "Warn" in complete.stdout or "Warn" in complete.stderr:
                    warnings.append(
                        f"{script_path}\n{output_text}{error_text}\n"
                        f"Run just this script with {' '.join(to_run)}."
                    )
                    n_warnings += 1

                if script.capture_stdout:
                    self.captured_stdout += complete.stdout
            except CalledProcessError:
                n_failures += 1
                failures.append(
                    f"{script_path}\n{output_text}{error_text}\n"
                    f"Run just this script with {' '.join(to_run)}."
                )

        if n_warnings > 0:
            print("Warnings:")
            print("\n".join(warnings))

        if n_failures > 0:
            print("Failures:")
            print("\n".join(failures))

        print(f"Successfully completed {len(self.scripts) - n_failures} scripts")
        print(f"There were {n_failures} failures")
        print(f"There were {n_warnings} scripts that raised warnings")

        if n_warnings + n_failures > 0:
            print("Error and warning information are available in stdout above.")
