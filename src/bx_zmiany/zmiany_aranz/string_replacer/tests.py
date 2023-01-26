from pprint import pprint

from django.test import TestCase

from .string_replacer import Replacer
from zmiany_aranz.models import Procedure, CostEstimate


class ProcedureReplacerTests(TestCase):
    fixtures = ["procedure.json"]

    def setUp(self):
        self.procedure = Procedure.objects.get(pk=1)
        self.cost_estimate = CostEstimate.objects.get(pk=1)

    def test_procedure_replacer(self):
        expected_dict = {
            "PREMISES_SYMBOL": "URZ-N-M39B",
            "COST_ESTIMATE_CUSTOMER_NET": "1000.00 zł",
            "COST_ESTIMATE_CUSTOMER_GROSS": "1080.00 zł",
            "COST_ESTIMATE_GC_NET": "900.00 zł",
            "COST_ESTIMATE_GC_GROSS": "972.00 zł",
        }
        before = """symbol: [PREMISES_SYMBOL],
        ce customer net: [COST_ESTIMATE_CUSTOMER_NET] zł,
        ce customer gross: [COST_ESTIMATE_CUSTOMER_GROSS] zł,
        ce general contractrator net: [COST_ESTIMATE_GC_NET] zł,
        ce general contractrator gross: [COST_ESTIMATE_GC_GROSS] zł
        """
        after = """symbol: URZ-N-M39B,
        ce customer net: 1000.00 zł,
        ce customer gross: 1080.00 zł,
        ce general contractrator net: 900.00 zł,
        ce general contractrator gross: 972.00 zł
        """
        procedure_replacer = Replacer(self.procedure)
        self.assertEqual(procedure_replacer(before), after)
