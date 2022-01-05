"""
Runs the scripts in scripts/
"""

from scrunner import ScriptRunner

runner = ScriptRunner("./scripts")

runner.parse_scripts()

runner.run(
    data=["./data.csv"],
    output_directory="./output",
    file_type="png",
    number_of_figures=1,
    stylesheet="default",
)
