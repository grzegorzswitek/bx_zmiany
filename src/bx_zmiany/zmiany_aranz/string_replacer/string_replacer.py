class Replacer:
    """Replacer factory for specific model."""

    def __new__(cls, object):

        return_class = {
            "Procedure": ProcedureReplacer,
        }.get(object.__class__.__name__, None)
        if return_class is None:
            return None
        return return_class(object)


class ReplacerInterface:
    """Return a copy with all occurrences of defined strings
    replaced by data based on the given object."""

    replacements_dict = {}

    def __init__(self, object) -> None:
        pass

    def __call__(self, sentence: str) -> str:
        for old, new in self.replacements_dict.items():
            sentence = sentence.replace(old, new)
        return sentence


class ProcedureReplacer(ReplacerInterface):
    """Return a copy with all occurrences of defined strings
    replaced by data based on the given object."""

    replacements_dict = {
        "[PREMISES_SYMBOL]": "[PREMISES_SYMBOL]",
        "[COST_ESTIMATE_CUSTOMER_NET]": "[COST_ESTIMATE_CUSTOMER_NET]",
        "[COST_ESTIMATE_CUSTOMER_GROSS]": "[COST_ESTIMATE_CUSTOMER_GROSS]",
        "[COST_ESTIMATE_GC_NET]": "[COST_ESTIMATE_GC_NET]",
        "[COST_ESTIMATE_GC_GROSS]": "[COST_ESTIMATE_GC_GROSS]",
    }

    def __init__(self, procedure) -> None:
        super().__init__(procedure)
        self.procedure = procedure
        self.replacements_dict["[PREMISES_SYMBOL]"] = (
            self._premises_symbol() or "[PREMISES_SYMBOL]"
        )
        self.replacements_dict["[COST_ESTIMATE_CUSTOMER_NET]"] = (
            self._cost_estimate("net", "customer") or "[COST_ESTIMATE_CUSTOMER_NET]"
        )
        self.replacements_dict["[COST_ESTIMATE_CUSTOMER_GROSS]"] = (
            self._cost_estimate("gross", "customer") or "[COST_ESTIMATE_CUSTOMER_GROSS]"
        )
        self.replacements_dict["[COST_ESTIMATE_GC_NET]"] = (
            self._cost_estimate("net", "general_contractor") or "[COST_ESTIMATE_GC_NET]"
        )
        self.replacements_dict["[COST_ESTIMATE_GC_GROSS]"] = (
            self._cost_estimate("gross", "general_contractor")
            or "[COST_ESTIMATE_GC_GROSS]"
        )

    def _premises_symbol(self):
        premises = self.procedure.premises.all()
        if not premises:
            return None
        return ", ".join([p.symbol for p in premises])

    def _cost_estimate(self, net_or_gross, _for: str = None):
        cost_estimates = self.procedure.cost_estimates.all()
        if not cost_estimates:
            return None
        if _for is None:
            cost_estimate = cost_estimates.last()
        elif _for.lower() == "customer":
            cost_estimate = cost_estimates.filter(
                costestimateofprocedure__for_customer=True
            ).last()
        elif _for.lower() == "general_contractor":
            cost_estimate = cost_estimates.filter(
                costestimateofprocedure__for_general_contractor=True
            ).last()
        else:
            raise ValueError(
                "_for param must be in ['customer', 'general_contractor'] or None."
            )
        if not cost_estimate:
            return None
        if net_or_gross == "net":
            result = cost_estimate.net
        elif net_or_gross == "gross":
            result = cost_estimate.gross
        else:
            raise ValueError("net_or_gross param must be in ['net', 'gross'].")
        return f"{result:2f}"
