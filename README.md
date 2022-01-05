ScRunner
========

ScRunner is a script runner for python.

It specialises in running a repeated set of analysis scripts on similar data,
and allows you to collect scripts together with metadata for easy
comparisons.

The scripts must all use the same argument parser API, and
must contain frontmatter in the docstring to describe the figures
that will be made.