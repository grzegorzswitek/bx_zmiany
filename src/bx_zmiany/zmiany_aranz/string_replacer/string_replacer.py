from typing import *


class ReplacerInterface:
    """Return a copy with all occurrences of defined strings
    replaced by data based on the given object."""

    def __init__(self, object) -> None:
        self.replacements_dict = {}

    def __call__(self, sentence: str) -> str:
        if not isinstance(sentence, str):
            raise TypeError(
                f"'sentence' must be a str, not {sentence.__class__.__name__}."
            )
        for old, new in self.replacements_dict.items():
            sentence = sentence.replace(f"[{old}]", new)
        return sentence

    def _add_if_not_none(self, key, value):
        """Update self.replacements_dict with {key: value} if value is not None."""
        if value is None:
            return
        if not all([isinstance(arg, str) for arg in [key, value]]):
            raise TypeError("Both, 'key' and 'value' must be a str.")
        self.replacements_dict[key] = value

    def _add_related_dict(self, object, prefix="", suffix=""):
        """Update self.replacements_dict with dict for related object."""
        if object is None:
            return
        if not all([isinstance(arg, str) for arg in [prefix, suffix]]):
            raise TypeError("Both, 'prefix' and 'suffix' must be a str.")
        related_replacer = Replacer(object)
        self.replacements_dict.update(
            {
                f"{prefix}_{key}_{suffix}".strip("_ "): value
                for key, value in related_replacer.replacements_dict.items()
            }
        )


class CostEstimateReplacer(ReplacerInterface):
    """Return a copy with all occurrences of defined strings
    replaced by data based on the given CostEstimate object."""

    def __init__(self, cost_estimate) -> None:
        super().__init__(cost_estimate)
        self.cost_estimate = cost_estimate
        self._add_if_not_none("NET", self._value("net"))
        self._add_if_not_none("GROSS", self._value("gross"))

    def _value(self, field):
        try:
            result = getattr(self.cost_estimate, field)
        except AttributeError:
            raise
        if result:
            return f"{result:2f}"


class ProcedureReplacer(ReplacerInterface):
    """Return a copy with all occurrences of defined strings
    replaced by data based on the given Procedure object."""

    def __init__(self, procedure) -> None:
        super().__init__(procedure)
        self.procedure = procedure
        self._add_if_not_none("PREMISES_SYMBOL", self._premises_symbol())
        self._add_related_dict(
            self._last_cost_estimate(_for="customer"), prefix="COST_ESTIMATE_CUSTOMER"
        )
        self._add_related_dict(
            self._last_cost_estimate(_for="general_contractor"),
            prefix="COST_ESTIMATE_GC",
        )

    def _premises_symbol(self):
        premises = self.procedure.premises.all()
        if not premises:
            return None
        return ", ".join([p.symbol for p in premises])

    # Methods for related objects
    def _last_cost_estimate(self, _for: str = None):
        if _for is None:
            cost_estimate = self.procedure.cost_estimates.last()
        elif _for.lower() == "customer":
            cost_estimate = self.procedure.cost_estimates.filter(
                costestimateofprocedure__for_customer=True
            ).last()
        elif _for.lower() == "general_contractor":
            cost_estimate = self.procedure.cost_estimates.filter(
                costestimateofprocedure__for_general_contractor=True
            ).last()
        else:
            raise ValueError(
                "_for param must be in ['customer', 'general_contractor'] or None."
            )
        return cost_estimate


class Replacer:
    """Replacer factory for specific model."""

    def __new__(cls, object):
        return_class = {
            "Procedure": ProcedureReplacer,
            "CostEstimate": CostEstimateReplacer,
        }.get(object.__class__.__name__, None)
        if return_class is None:
            return None
        return return_class(object)
