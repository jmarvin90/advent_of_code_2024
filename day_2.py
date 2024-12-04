import pathlib
import numpy as np

# Populate input reports
reports = []

with pathlib.Path("puzzle_2_input.txt").open("r") as infile:
    for line in infile:
        report = line.strip("\n").split(" ")
        reports.append([int(level) for level in report])


# ---- Day 2, PT 1---- #

# How we check a valid report
def report_is_valid(report: list) -> bool:
    diffs = np.diff(report)
    diffs_positive = [diff > 0 for diff in diffs]

    # If numbers move in the same direction...
    # ...and are no more than 3/less than 1 away from each other
    if (
        min(diffs_positive) == max(diffs_positive) and
        all(3 >= abs(num) >= 1 for num in diffs)
    ):
        return True
    return False

# ANSWER
safe_reports = sum(1 if report_is_valid(report) else 0 for report in reports)
print(safe_reports)


# ---- Day 2, PT 2---- #

# How we check valid reports - tolerating one bad level
def report_is_valid_tolerate_one_bad(report: list) -> bool:
    # Return immediately if the report is conventionally acceptable
    if (report_is_valid(report)):
        return True

    # Point all the reports in the same direction
    w_report = report[:] if report[0] < report[-1] else list(reversed(report))

    # Get the differences between levels to see which ones might be bad
    level_is_valid = [1 <= diff <= 3 for diff in np.diff(w_report)]

    # If there are more than two bad differences, we've had it
    if level_is_valid.count(False) > 2:
        return False

    # Otherwise try again - removing indexes either side of the first bad diff
    bad_level_index = level_is_valid.index(False)

    return (
        report_is_valid(
            w_report[:bad_level_index] + w_report[bad_level_index+1:]
        ) or
        report_is_valid(
            w_report[:bad_level_index+1] + w_report[bad_level_index+2:]
        )
    )

# ANSWER
safe_reports_tolerate_one_bad = sum(
    1 if report_is_valid_tolerate_one_bad(report)
    else 0
    for report in reports
)
print(safe_reports_tolerate_one_bad)