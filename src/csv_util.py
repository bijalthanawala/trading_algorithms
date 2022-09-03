from typing import List
import logging
import csv

from .result import Result


class ColumnTranslation:
    def __init__(self, column_name, column_name_xlat, column_type):
        self.column_name = column_name
        self.column_name_xlat = column_name_xlat
        self.column_type = column_type


def read_csv_file(
    csv_filename: str,
    column_translations: List[ColumnTranslation],
    row_object_type: type,
) -> Result:
    line_number = -1
    row_objects: List = []

    logging.info(f"Reading CSV file: {csv_filename}")
    try:
        with open(
            csv_filename, newline="", encoding="ascii", errors="ignore"
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            line_number = 2  # The very first line is the header

            for row in reader:
                if len(row) != len(column_translations):
                    return Result(
                        False,
                        message=f"File: {csv_filename} Line: {line_number} Error: Found {len(row)} fields, expected {len(column_translations)}",
                        result=None,
                    )

                # Tranform this CSV row dict into object of desired type
                # TODO: Replace this dict comprehension with code that is readable, and which can catch the missing header condition accurately
                row_object = row_object_type(
                    **{
                        translation.column_name_xlat: translation.column_type(
                            row.get(
                                translation.column_name,
                                f"Field '{translation.column_name}' missing!",
                            )
                        )
                        for translation in column_translations
                    }
                )
                row_objects.append(row_object)
                line_number += 1
    except Exception as ex:
        message = (
            str(ex)
            if line_number == -1
            else f"File: {csv_filename} Line: {line_number} Error: {str(ex)}"
        )
        return Result(isSuccess=False, message=message, result=None)

    logging.info(f"Read {len(row_objects)} rows")

    return Result(isSuccess=True, message="", result=row_objects)
