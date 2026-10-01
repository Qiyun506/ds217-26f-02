"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """
    Return a list of the systolic readings from all encounters.
    """
    # TODO: collect the systolic value of every encounter into one list.
    return [systolic for _, _, systolic in encounters]


def mean_systolic(readings):
    """
    return the mean of systolic readingm if None when nothing to average
    """
    if not readings:
        return None
    return sum(readings) / len(readings)


def count_patients(encounters):
    """Return the number of distinct patients in the encounters list."""
    patients_total = {patient_id for patient_id, _, _ in encounters}
    return len(patients_total)


def patients_at_or_above(encounters, cutoff):
    """TODO: Return patient IDs with systolic readings at or above the cutoff."""
    patient_ids = {patient_id for patient_id,_,systolic in encounters if systolic >= cutoff}
    return patient_ids

