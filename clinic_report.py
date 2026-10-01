#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """
    Read the clinic CSV and keep only the usable encounters.

    One usable encounter is a tuple (patient_id, visit_date, systolic):
    the row split into exactly three fields, int() could read the
    systolic field, and the reading is from 60 to 250 mmHg inclusive

    Give back two values: the list of usable encounters, and how many data
    rows you skipped. `main()` unpacks them the way the lecture unpacks a
    tuple, with two names on the left of the `=`.
    """
    encounters = []
    skipped = 0
    with open(data_path) as df:
        lines = df.read().splitlines()
    # TODO: read the rows and skip the header line.
    for line in lines[1:]:
        if line.strip() == "":
            skipped += 1
            print("Skipped blank line")
            continue
        variables = line.split(",")
        # TODO: keep a row only when it has three fields, int() can read the
        #       systolic field, and the reading is plausible.
        if len(variables) != 3:
            skipped += 1
            print(f"Skipped line with wrong number of fields: {line}")
            continue
        patient_id, visit_date, systolic_str = variables

        # TODO: keep a row only when it has three fields, int() can read the
        #       systolic field, and the reading is plausible.
        # TODO: count every other data row as skipped, the blank line included,
        #       and print one line per skipped row so you can see what dropped out.
        try:
            systolic = int(systolic_str)
        except ValueError:
            skipped += 1
            print(f"Skipped line with non-integer systolic: {line}")
            continue
        if not (60 <= systolic <= 250):
            skipped += 1
            print(f"Skipped line with implausible systolic: {line}")
            continue
        encounters.append((patient_id, visit_date, systolic))
        # TODO: end with `return encounters, skipped`.
    return encounters, skipped
        # pass


def main():
    """TODO: describe the two artifacts this writes."""
    encounters, skipped = read_encounters(DATA_PATH)

    # TODO: build the six report lines and write them to output/vitals_report.txt.
    readings = systolic_readings(encounters)
    report_lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {count_patients(encounters)}",
        f"Mean systolic: {mean_systolic(readings)} mmHg",
        f"Highest systolic: {max(readings) if readings else 'N/A'} mmHg",
        f"Lowest systolic: {min(readings) if readings else 'N/A'} mmHg"
    ]
    with open("output/vitals_report.txt","w") as f:
        f.write("\n".join(report_lines))
    # TODO: read the file back and print it, so you can see what was saved.
    with open("output/vitals_report.txt") as f:
        print(f.read())
    # TODO: choose your follow-up cutoff, then write output/followup_list.txt
    #       with the Cutoff line, the Reason line, and one patient ID per line.

    CUTOFF = 155
    reason = "THE range of systolic reading is 60-250 mmHg, so I choose the midpoint as the cutoff."
    followup_patients = patients_at_or_above(encounters, CUTOFF)
    with open("output/followup_list.txt", "w") as f:
        f.write(f"Cutoff: {CUTOFF} mmHg\n")
        f.write(f"Reason: {reason}\n")
        for patient_id in followup_patients:
            f.write(f"{patient_id}\n")


if __name__ == "__main__":
    main()
