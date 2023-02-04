import os
import logging
import tempfile
from shutil import rmtree

from django.urls import reverse
from django.test import TestCase
from django.test.utils import setup_test_environment

from model_bakery import baker

from zmiany_aranz.models import (
    Procedure,
    Cost,
    KindOfCost,
    Invoice,
    Customer,
    CustomerOfProcedure,
    CostEstimate,
    InvestmentStage,
    Building,
    Premises,
    EmailAction,
    Person,
    InvestmentStagePerson,
    EmailActionPerson,
)

from zmiany_aranz.forms import SendEmailForm

from zmiany_aranz.apps import ZmianyAranzConfig

logger = logging.getLogger(__name__)
logging.disable(logging.CRITICAL)

APP_NAME = ZmianyAranzConfig.name


class ProcedureDetailViewTests(TestCase):
    def test_procedure_status_code_200(self):
        procedure = Procedure.objects.create()
        response = self.client.get(
            reverse(
                f"{APP_NAME}:procedure_detail_view",
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
                f"{APP_NAME}:procedure_detail_view",
                kwargs={"pk": procedure.pk + 1},
            )
        )
        self.assertEqual(response.status_code, 404)


class ProcedureCostsListTests(TestCase):
    def test_procedure_without_costs(self):
        procedure = Procedure.objects.create()
        response = self.client.get(
            reverse(f"{APP_NAME}:procedure_costs_list", kwargs={"pk": procedure.pk})
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
            reverse(f"{APP_NAME}:procedure_costs_list", kwargs={"pk": procedure.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Projekt zamienny c.o.")
        self.assertContains(response, "100,00 zł")
        self.assertContains(response, "8,00 zł")
        self.assertContains(response, "108,00 zł")
        self.assertContains(response, "Projekt zamienny")

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
            reverse(f"{APP_NAME}:procedure_costs_list", kwargs={"pk": procedure.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Projekt zamienny c.o.")
        self.assertContains(response, "Projekt zamienny wentylacji")

    def test_procedure_does_not_exist(self):
        response = self.client.get(
            reverse(f"{APP_NAME}:procedure_costs_list", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 404)


class ProcedureCostCreateTests(TestCase):
    def test_create_cost(self):
        procedure = Procedure.objects.create()
        kind = KindOfCost.objects.create(name="Projekt zamienny")
        response = self.client.post(
            reverse(f"{APP_NAME}:procedure_cost_create", kwargs={"pk": procedure.pk}),
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
            reverse(f"{APP_NAME}:procedure_costs_list", kwargs={"pk": procedure.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Projekt zamienny")


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
            reverse(f"{APP_NAME}:cost_delete", kwargs={"pk": self.cost.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Czy na pewno usunąć koszt?")

    def test_delete_success_page(self):
        response = self.client.post(
            reverse(f"{APP_NAME}:cost_delete", kwargs={"pk": self.cost.pk}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak kosztów.")
        self.assertQuerysetEqual(Cost.objects.all(), [])


class CostUpdateTest(TestCase):
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

    def test_update_GET(self):
        response = self.client.get(
            reverse(f"{APP_NAME}:cost_update", kwargs={"pk": self.cost.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "100")

    def test_update_POST(self):
        response = self.client.post(
            reverse(f"{APP_NAME}:cost_update", kwargs={"pk": self.cost.pk}),
            {
                "net": 200,
                "vat": 16,
                "gross": 216,
                "name": "projekt zamienny",
                "kind": self.kind.pk,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "200")
        self.assertEqual(Cost.objects.last().net, 200)


class ProcedureInvoicesListTests(TestCase):
    def setUp(self) -> None:
        self.invoice_1 = Invoice.objects.create(
            number="FVS/1/1/2022",
            invoice_date="2022-01-01",
            due_date="2022-01-15",
            net=100,
            vat=8,
            gross=108,
            description="",
        )
        self.invoice_2 = Invoice.objects.create(
            number="FVS/2/1/2022",
            invoice_date="2022-01-02",
            due_date="2022-01-16",
            net=100,
            vat=8,
            gross=108,
            description="",
        )
        self.procedure_with_invoices = Procedure.objects.create()
        self.procedure_without_invoices = Procedure.objects.create()
        self.procedure_with_invoices.invoices.set([self.invoice_1, self.invoice_2])

    def test_procedure_without_invoices(self):
        response = self.client.get(
            reverse(
                f"{APP_NAME}:procedure_invoices_list",
                kwargs={"pk": self.procedure_without_invoices.pk},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak faktur.")

    def test_procedure_with_invoices(self):
        response = self.client.get(
            reverse(
                f"{APP_NAME}:procedure_invoices_list",
                kwargs={"pk": self.procedure_with_invoices.pk},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FVS/2/1/2022")

    def test_procedure_does_not_exist(self):
        response = self.client.get(
            reverse(f"{APP_NAME}:procedure_invoices_list", kwargs={"pk": 0})
        )
        self.assertEqual(response.status_code, 404)


class ProcedureInvoiceCreateTests(TestCase):
    def setUp(self) -> None:
        self.procedure = Procedure.objects.create()
        self.invoice = Invoice.objects.create(
            number="FVS/1/1/2022",
            invoice_date="2022-01-01",
            due_date="2022-01-15",
            net=100,
            vat=8,
            gross=108,
            description="",
        )
        self.procedure.invoices.set([self.invoice])

    def test_create_invoice(self):
        response = self.client.post(
            reverse(
                f"{APP_NAME}:procedure_invoice_create",
                kwargs={"pk": self.procedure.pk},
            ),
            {
                "number": "FVS/3/2/2022",
                "invoice_date": "2022-02-01",
                "due_date": "2022-02-15",
                "net": 1000,
                "vat": 80,
                "gross": 1080,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Invoice.objects.last().number, "FVS/3/2/2022")


class InvoiceDeleteTest(TestCase):
    def setUp(self) -> None:
        self.procedure = Procedure.objects.create()
        self.invoice = Invoice.objects.create(
            number="FVS/1/1/2022",
            invoice_date="2022-01-01",
            due_date="2022-01-15",
            net=100,
            vat=8,
            gross=108,
            description="",
        )
        self.procedure.invoices.set([self.invoice])

    def test_delete_confirmation_page(self):
        response = self.client.get(
            reverse(f"{APP_NAME}:invoice_delete", kwargs={"pk": self.invoice.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Czy na pewno usunąć fakturę?")

    def test_delete_success_page(self):
        response = self.client.post(
            reverse(f"{APP_NAME}:invoice_delete", kwargs={"pk": self.invoice.pk}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak faktur.")
        self.assertQuerysetEqual(Invoice.objects.all(), [])


class InvoiceUpdateTest(TestCase):
    def setUp(self) -> None:
        self.procedure = Procedure.objects.create()
        self.invoice = Invoice.objects.create(
            number="FVS/1/1/2022",
            invoice_date="2022-01-01",
            due_date="2022-01-15",
            net=100,
            vat=8,
            gross=108,
            description="",
        )
        self.procedure.invoices.set([self.invoice])

    def test_update_GET(self):
        response = self.client.get(
            reverse(f"{APP_NAME}:invoice_update", kwargs={"pk": self.invoice.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "100")

    def test_update_POST(self):
        response = self.client.post(
            reverse(f"{APP_NAME}:invoice_update", kwargs={"pk": self.invoice.pk}),
            {
                "number": "FVS/1/1/2022",
                "invoice_date": "2022-01-01",
                "due_date": "2022-01-15",
                "net": 200,
                "vat": 16,
                "gross": 216,
                "description": "",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "200")
        self.assertEqual(Invoice.objects.last().net, 200)


class ProcedureCustomersListTests(TestCase):
    def setUp(self):
        self.procedure_1 = Procedure.objects.create()
        self.procedure_2 = Procedure.objects.create()
        customers = (
            Customer.objects.create(
                first_name="Anna",
                last_name="Kowalska",
            ),
            Customer.objects.create(
                first_name="Jan",
                last_name="Kowalski",
            ),
        )
        self.procedure_1.customers.set(customers)

    def test_procedure_with_customers(self):
        response = self.client.get(
            reverse(
                f"{APP_NAME}:procedure_customers_list",
                kwargs={"pk": self.procedure_1.pk},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Anna")
        self.assertContains(response, "Jan")

    def test_procedure_without_customers(self):
        response = self.client.get(
            reverse(
                f"{APP_NAME}:procedure_customers_list",
                kwargs={"pk": self.procedure_2.pk},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak klientów")

    def test_procedure_does_not_exist(self):
        response = self.client.get(
            reverse(
                f"{APP_NAME}:procedure_customers_list",
                kwargs={"pk": 0},
            )
        )
        self.assertEqual(response.status_code, 404)


class CustomerOfProcedureCreateTests(TestCase):
    def setUp(self):
        self.procedure = Procedure.objects.create()
        self.customer = Customer.objects.create(
            first_name="Anna",
            last_name="Kowalska",
        )

    def test_customer_of_procedure_create(self):
        response = self.client.post(
            reverse(
                f"{APP_NAME}:customer_of_procedure_create",
                kwargs={"pk": self.procedure.pk},
            ),
            {
                "procedure": self.procedure.pk,
                "customer": self.customer.pk,
                "shares": 0.5,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        customer_of_procedure = CustomerOfProcedure.objects.filter(
            procedure=self.procedure
        ).first()
        self.assertEqual(customer_of_procedure.customer, self.customer)
        self.assertEqual(CustomerOfProcedure.objects.last().shares, 0.5)


class CustomerOfProcedureUpdateTests(TestCase):
    def setUp(self):
        self.procedure = Procedure.objects.create()
        self.customer = Customer.objects.create(
            first_name="Anna",
            last_name="Kowalska",
        )
        self.customer_of_procedure = CustomerOfProcedure.objects.create(
            procedure=self.procedure, customer=self.customer
        )

    def test_customer_of_procedure_update(self):
        response = self.client.post(
            reverse(
                f"{APP_NAME}:customer_of_procedure_update",
                kwargs={"pk": self.customer_of_procedure.pk},
            ),
            {
                "procedure": self.procedure.pk,
                "customer": self.customer.pk,
                "shares": 0.1,
            },
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                f"{APP_NAME}:procedure_customers_list",
                kwargs={"pk": self.procedure.pk},
            ),
        )
        self.assertEqual(CustomerOfProcedure.objects.last().shares, 0.1)


class CustomerOfProcedureDeleteTests(TestCase):
    def setUp(self):
        self.procedure = Procedure.objects.create()
        self.customer = Customer.objects.create(
            first_name="Anna",
            last_name="Kowalska",
        )
        self.customer_of_procedure = CustomerOfProcedure.objects.create(
            procedure=self.procedure, customer=self.customer
        )

    def test_delete_confirmation_page(self):
        response = self.client.get(
            reverse(
                f"{APP_NAME}:customer_of_procedure_delete",
                kwargs={"pk": self.customer_of_procedure.pk},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Czy na pewno usunąć klienta?")

    def test_delete_success_page(self):
        response = self.client.post(
            reverse(
                f"{APP_NAME}:customer_of_procedure_delete",
                kwargs={"pk": self.customer_of_procedure.pk},
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak klientów.")
        self.assertRedirects(
            response,
            reverse(
                f"{APP_NAME}:procedure_customers_list",
                kwargs={"pk": self.procedure.pk},
            ),
        )
        self.assertQuerysetEqual(CustomerOfProcedure.objects.all(), [])


class CustomerCreateTests(TestCase):
    def test_customer_create(self):
        response = self.client.post(
            reverse(f"{APP_NAME}:customer_create"),
            {"first_name": "Jan", "last_name": "Testowy"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jan")
        self.assertEqual(Customer.objects.last().first_name, "Jan")


class CustomerDetailTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(first_name="Anna", last_name="Kowalska")

    def test_customer_detail(self):
        response = self.client.get(
            reverse(f"{APP_NAME}:customer_detail", kwargs={"pk": self.customer.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Anna")


class CustomerUpdateTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(first_name="Anna", last_name="Kowalska")

    def test_customer_update(self):
        response = self.client.post(
            reverse(f"{APP_NAME}:customer_update", kwargs={"pk": self.customer.pk}),
            {"first_name": "Anna", "last_name": "Kwiatkowska"},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(f"{APP_NAME}:customer_detail", kwargs={"pk": self.customer.pk}),
            status_code=302,
            target_status_code=200,
        )
        self.assertEqual(Customer.objects.last().last_name, "Kwiatkowska")


class CustomerDeleteTests(TestCase):
    def setUp(self) -> None:
        self.customer = Customer.objects.create(first_name="Anna", last_name="Kowalska")
        self.procedure = Procedure.objects.create()
        self.procedure.customers.set([self.customer])

    def test_customer_delete_GET(self):
        response = self.client.get(
            reverse(f"{APP_NAME}:customer_delete", kwargs={"pk": self.customer.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Czy na pewno usunąć")
        self.assertContains(response, self.procedure.number)

    def test_customer_delete_POST(self):
        response = self.client.post(
            reverse(f"{APP_NAME}:customer_delete", kwargs={"pk": self.customer.pk})
        )
        self.assertRedirects(response, reverse(f"{APP_NAME}:index"), 302, 200)
        self.assertQuerysetEqual(Customer.objects.all(), [])


class ProcedureCostEstimatesListTests(TestCase):
    def test_procedure_without_cost_estimates(self):
        procedure = Procedure.objects.create()
        response = self.client.get(
            reverse(
                f"{APP_NAME}:procedure_cost_estimates_list", kwargs={"pk": procedure.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak kosztorysów")

    def test_procedure_with_many_cost_estimates(self):
        cost_estimate_1 = baker.make(CostEstimate, file_name="Kosztorys.rds")
        cost_estimate_2 = baker.make(CostEstimate, file_name="Kosztorys 23.rds")
        procedure = Procedure.objects.create()
        procedure.cost_estimates.set([cost_estimate_1, cost_estimate_2])
        response = self.client.get(
            reverse(
                f"{APP_NAME}:procedure_cost_estimates_list", kwargs={"pk": procedure.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kosztorys.rds")
        self.assertContains(response, "Kosztorys 23.rds")

    def test_procedure_does_not_exist(self):
        response = self.client.get(
            reverse(f"{APP_NAME}:procedure_cost_estimates_list", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 404)


class ProcedureCostEstimateCreateTests(TestCase):
    def test_create_cost_estimate(self):
        procedure = Procedure.objects.create()
        response = self.client.post(
            reverse(
                f"{APP_NAME}:procedure_cost_estimate_create",
                kwargs={"pk": procedure.pk},
            ),
            {
                "file_name": "Kosztorys123.pdf",
                "net": 100,
                "vat": 8,
                "gross": 108,
                "construction_net": 50,
                "sanitary_net": 30,
                "electric_net": 20,
                "other_net": 0,
                "creation_date": "2022-02-02",
                "added_date": "2022-02-21",
                "number": "10",
                "description": "Kosztorys wstępny",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CostEstimate.objects.last().description, "Kosztorys wstępny")

    def test_display_cost_estimate(self):
        procedure = Procedure.objects.create()
        cost_estimate = baker.make(CostEstimate, file_name="Kosztorys.rds")
        procedure.cost_estimates.set([cost_estimate])
        response = self.client.get(
            reverse(
                f"{APP_NAME}:procedure_cost_estimates_list", kwargs={"pk": procedure.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kosztorys.rds")


class CostEstimateDeleteTest(TestCase):
    def setUp(self) -> None:
        self.procedure = Procedure.objects.create()
        self.cost_estimate = baker.make(CostEstimate)
        self.procedure.cost_estimates.set([self.cost_estimate])

    def test_delete_confirmation_page(self):
        response = self.client.get(
            reverse(
                f"{APP_NAME}:cost_estimate_delete", kwargs={"pk": self.cost_estimate.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Czy na pewno usunąć koszt?")

    def test_delete_success_page(self):
        response = self.client.post(
            reverse(
                f"{APP_NAME}:cost_estimate_delete", kwargs={"pk": self.cost_estimate.pk}
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak kosztorysów.")
        self.assertQuerysetEqual(CostEstimate.objects.all(), [])


class CostEstimateUpdateTest(TestCase):
    def setUp(self) -> None:
        self.procedure = Procedure.objects.create()
        self.cost_estimate = baker.make(CostEstimate, description="Wstępny")
        self.procedure.cost_estimates.set([self.cost_estimate])

    def test_update_GET(self):
        response = self.client.get(
            reverse(
                f"{APP_NAME}:cost_estimate_update", kwargs={"pk": self.cost_estimate.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wstępny")

    def test_update_POST(self):
        response = self.client.post(
            reverse(
                f"{APP_NAME}:cost_estimate_update", kwargs={"pk": self.cost_estimate.pk}
            ),
            {
                "file_name": "Kosztorys123.pdf",
                "net": 100,
                "vat": 8,
                "gross": 108,
                "construction_net": 50,
                "sanitary_net": 30,
                "electric_net": 20,
                "other_net": 0,
                "creation_date": "2022-02-02",
                "added_date": "2022-02-21",
                "number": "10",
                "description": "Kosztorys wstępny",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kosztorys wstępny")
        self.assertEqual(CostEstimate.objects.last().description, "Kosztorys wstępny")


class SendEmailTests(TestCase):
    fixtures = ["email_action.json"]

    def setUp(self):
        self.url = f"{APP_NAME}:send_email"
        self.action_slug = "gw-woz"
        self.directory = tempfile.mkdtemp()
        os.mkdir(os.path.join(self.directory, "PDF po zmianach"))
        self.abs_file_paths = [
            os.path.join(self.directory, path)
            for path in [
                "URZ-N-M39B - Wniosek o zmiany aranżacyjne w mieszkaniu.pdf",
                "URZ-N-M39B - Kosztorys.ath",
                "URZ-N-M39B - Kosztorys.pdf",
                "PDF po zmianach\\plik_1.pdf",
                "PDF po zmianach\\plik_2.pdf",
            ]
        ]
        for path in self.abs_file_paths:
            with open(path, "w") as f:
                f.write("Plik testowy")
        self.procedure = Procedure.objects.get(pk=1)
        self.procedure.directory = self.directory
        self.procedure.save()
        email_action = EmailAction.objects.get(pk=1)
        self.attachments_ids = [
            id
            for id, _ in email_action._get_attachments_path_for_procedure(
                self.procedure
            )
        ]

    def test_GET_invalid_procedure_pk(self):
        response = self.client.get(
            reverse(self.url, kwargs={"pk": 0, "slug": self.action_slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_GET_invalid_action_slug(self):
        response = self.client.get(
            reverse(self.url, kwargs={"pk": self.procedure.pk, "slug": "invalid-slug"})
        )
        self.assertEqual(response.status_code, 404)

    def test_GET_correct(self):
        response = self.client.get(
            reverse(
                self.url, kwargs={"pk": self.procedure.pk, "slug": self.action_slug}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")
        self.assertIsInstance(response.context["form"], SendEmailForm)
        self.assertContains(response, "Anna Sadowska")
        self.assertContains(
            response, "URZ-N-M39B - Wniosek o zmiany aranżacyjne w mieszkaniu.pdf"
        )

    def test_POST_invalid_procedure_pk(self):
        response = self.client.post(
            reverse(self.url, kwargs={"pk": 0, "slug": self.action_slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_POST_invalid_action_slug(self):
        response = self.client.post(
            reverse(self.url, kwargs={"pk": self.procedure.pk, "slug": "invalid-slug"})
        )
        self.assertEqual(response.status_code, 404)

    def test_POST_invalid_form(self):
        response = self.client.post(
            reverse(
                self.url, kwargs={"pk": self.procedure.pk, "slug": self.action_slug}
            ),
            data={},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], SendEmailForm)

    def test_POST_correct(self):
        response = self.client.post(
            reverse(
                self.url,
                kwargs={"pk": self.procedure.pk, "slug": self.action_slug},
            ),
            data={
                "to": "user1@example.com\r\nuser2@example.com  ",
                "cc": "user3@example.com\r\nuser4@example.com  ",
                "bcc": "user5@example.com\r\n  ",
                "subject": "URZ-N-M24B - Wniosek o zmiany",
                "body": "Dzień dobry,\r\nW załączeniu przesyłam wniosek o zmiany.",
                "attachments": self.attachments_ids,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wiadomość została utworzona")

    def tearDown(self) -> None:
        rmtree(self.directory)
        return super().tearDown()


class PremisesImportTests(TestCase):
    # TODO: test incorrect file
    fixtures = ["premises_import.json"]

    def test_import_success(self):
        path = os.path.join(
            os.path.dirname(__file__), r"import_premises\import_premises.csv"
        )
        with open(path) as f:
            response = self.client.post(
                reverse(f"{APP_NAME}:premises_import"), data={"file": f}, follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(Premises.objects.values_list("symbol")),
            [("ENK-Z1-LM01",), ("ENK-Z1-LM02",), ("ENK-Z1-LM03",), ("ENK-Z1-LM04",)],
        )
