from django.urls import reverse
from django.test import TestCase
from django.test.utils import setup_test_environment

from zmiany_aranz.models import Procedure, Cost, KindOfCost


class ProcedureDetailViewTests(TestCase):
    def test_procedure_status_code_200(self):
        procedure = Procedure.objects.create()
        response = self.client.get(
            reverse(
                "zmiany_aranz:procedure_detail_view",
                kwargs={"pk": procedure.pk},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/")
        self.assertEqual(response.context["object"], procedure)

    def test_procedure_status_code_404(self):
        procedure = Procedure.objects.create()
        response = self.client.get(
            reverse(
                "zmiany_aranz:procedure_detail_view",
                kwargs={"pk": procedure.pk + 1},
            )
        )
        self.assertEqual(response.status_code, 404)


class ProcedureCostsListTests(TestCase):
    def test_procedure_without_costs(self):
        procedure = Procedure.objects.create()
        response = self.client.get(
            reverse("zmiany_aranz:procedure_costs_list", kwargs={"pk": procedure.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak kosztów")

    def test_procedure_with_one_cost(self):
        kind = KindOfCost.objects.create(name="Projekt zamienny")
        cost = Cost.objects.create(
            net=100,
            vat=8,
            gross=108,
            name="projekt zamienny c.o.",
            description="",
            kind=kind,
        )
        procedure = Procedure.objects.create()
        procedure.costs.set([cost])
        response = self.client.get(
            reverse("zmiany_aranz:procedure_costs_list", kwargs={"pk": procedure.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Projekt zamienny c.o.")
        self.assertContains(response, "Netto: 100,00 zł")
        self.assertContains(response, "VAT: 8,00 zł")
        self.assertContains(response, "Brutto: 108,00 zł")
        self.assertContains(response, "Rodzaj: Projekt zamienny")

    def test_procedure_with_many_costs(self):
        kind = KindOfCost.objects.create(name="Projekt zamienny")
        cost_1 = Cost.objects.create(
            net=100,
            vat=8,
            gross=108,
            name="projekt zamienny c.o.",
            description="",
            kind=kind,
        )
        cost_2 = Cost.objects.create(
            net=100,
            vat=8,
            gross=108,
            name="projekt zamienny wentylacji",
            description="",
            kind=kind,
        )
        procedure = Procedure.objects.create()
        procedure.costs.set([cost_1, cost_2])
        response = self.client.get(
            reverse("zmiany_aranz:procedure_costs_list", kwargs={"pk": procedure.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Projekt zamienny c.o.")
        self.assertContains(response, "Projekt zamienny wentylacji")

    def test_procedure_does_not_exist(self):
        response = self.client.get(
            reverse("zmiany_aranz:procedure_costs_list", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 404)


class ProcedureCostCreateTests(TestCase):
    def test_create_cost(self):
        procedure = Procedure.objects.create()
        kind = KindOfCost.objects.create(name="Projekt zamienny")
        response = self.client.post(
            reverse("zmiany_aranz:procedure_cost_create", kwargs={"pk": procedure.pk}),
            {
                "net": 100,
                "vat": 8,
                "gross": 108,
                "name": "projekt zamienny",
                "kind": kind.pk,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cost.objects.last().name, "projekt zamienny")

    def test_display_cost(self):
        procedure = Procedure.objects.create()
        kind = KindOfCost.objects.create(name="Projekt zamienny")
        cost = Cost.objects.create(
            net=100,
            vat=8,
            gross=108,
            name="projekt zamienny",
            kind=kind,
        )
        procedure.costs.set([cost])
        response = self.client.get(
            reverse("zmiany_aranz:procedure_costs_list", kwargs={"pk": procedure.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rodzaj: Projekt zamienny")


class CostDeleteTest(TestCase):
    def setUp(self) -> None:
        self.procedure = Procedure.objects.create()
        self.kind = KindOfCost.objects.create(name="Projekt zamienny")
        self.cost = Cost.objects.create(
            net=100,
            vat=8,
            gross=108,
            name="projekt zamienny",
            kind=self.kind,
        )
        self.procedure.costs.set([self.cost])

    def test_delete_confirmation_page(self):
        response = self.client.get(
            reverse("zmiany_aranz:cost_delete", kwargs={"pk": self.cost.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Czy na pewno usunąć koszt?")

    def test_delete_success_page(self):
        response = self.client.post(
            reverse("zmiany_aranz:cost_delete", kwargs={"pk": self.cost.pk}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak kosztów.")
