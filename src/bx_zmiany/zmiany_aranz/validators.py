import csv
from typing import *

from django.core.exceptions import ValidationError

from .models import Building, KindOfPremises, Premises


class PremisesImportDataValidator:
    def __init__(self, column_names) -> None:
        self.column_names = column_names

    def __call__(self, file, *args: Any, **kwargs: Any) -> None:
        errors = []
        try:
            reader = csv.reader(
                file.read().decode("utf-8").split("\n")[1:],
                delimiter=";",
            )
        except UnicodeError:
            raise ValidationError("Expected encoding is utf-8.")
        data_by_columns = {
            fieldname: values
            for fieldname, values in zip(
                self.column_names, (list(zip(*[line for line in reader if line])))
            )
        }
        # Check the number of columns
        if not len(data_by_columns) == len(self.column_names):
            raise ValidationError(
                f"The file has the wrong number of columns. "
                f"You should pass {self.column_names}."
            )
        # Check if the buildings and kinds_of_premises are in database.
        building_symbols = [b.symbol for b in Building.objects.all()]
        kind_of_premises_symbols = [k.symbol for k in KindOfPremises.objects.all()]
        for value in data_by_columns["building_symbol"]:
            if value not in building_symbols:
                errors.append(f"building_symbol must be in {building_symbols}.")
                break
        for value in data_by_columns["kind_symbol"]:
            if value not in kind_of_premises_symbols:
                errors.append(f"kind_symbol must be in {kind_of_premises_symbols}.")
                break
        # Run the model validators.
        for field in ("id_crm", "symbol", "staircase", "storey"):
            run_validators = Premises._meta.get_field(field).run_validators
            for value in data_by_columns[field]:
                try:
                    run_validators(value)
                except ValidationError as e:
                    errors.append(f"{field}: {';'.join(e.messages)}")
                    break
        # Check if values are unique.
        for field in ("id_crm", "symbol"):
            values = data_by_columns.get(field)
            if not len(set(values)) == len(values):
                errors.append(f"{field!r} must be unique.")
        # Check if premises symbols not in database.
        symbols = [symbol for (symbol,) in Premises.objects.values_list("symbol")]
        if any([symbol in symbols for symbol in data_by_columns["symbol"]]):
            errors.append("The premises with this symbol are already in the database.")

        if errors:
            raise ValidationError(errors)
