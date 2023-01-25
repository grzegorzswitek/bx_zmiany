from datetime import date
import tempfile
from shutil import rmtree
import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.template.defaultfilters import slugify

from model_bakery import baker

from zmiany_aranz.models import (
    Procedure,
    Investment,
    InvestmentStage,
    Building,
    Premises,
    KindOfPremises,
    Person,
    Customer,
    CustomerHandler,
    CostEstimate,
    CostEstimateOfProcedure,
    Invoice,
    Cost,
    KindOfCost,
    CustomerOfProcedure,
    InvestmentStagePerson,
    EmailAction,
    EmailActionPerson,
)


class UsermanagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", password="foo"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )


class ProcedureTests(TestCase):
    def setUp(self) -> None:
        Procedure.objects.create()
        Procedure.objects.create()

    def test_procedure_number_one(self):
        current_year = date.today().year
        expected_number = f"001/{str(current_year)[-2:]}"
        procedure = Procedure.objects.get(pk=1)
        self.assertEqual(procedure.number, expected_number)

    def test_procedure_number_two(self):
        current_year = date.today().year
        expected_number = f"002/{str(current_year)[-2:]}"
        procedure = Procedure.objects.get(pk=2)
        self.assertEqual(procedure.number, expected_number)


class InvestmentTests(TestCase):
    def test_investment_str(self):
        investment = Investment(name="Urzecze", symbol="URZ")
        excected_str = "Urzecze (URZ)"
        self.assertEqual(str(investment), excected_str)


class InvestmentStageTests(TestCase):
    def test_investment_stage_str(self):
        obj = InvestmentStage(name="Urzecze II", symbol="URZ-K")
        excected_str = "Urzecze II (URZ-K)"
        self.assertEqual(str(obj), excected_str)


class BuildingTests(TestCase):
    def test_building_str(self):
        obj = Building(name="Urzecze II, budynek A", symbol="URZ-K-A")
        excected_str = "Urzecze II, budynek A (URZ-K-A)"
        self.assertEqual(str(obj), excected_str)


class PremisesTests(TestCase):
    def test_premises_str(self):
        obj = Premises(symbol="T2-M39B")
        expected_str = "T2-M39B"
        self.assertEqual(str(obj), expected_str)


class KindOfPremisesTests(TestCase):
    def test_kind_of_premises_str(self):
        obj = KindOfPremises(name="lokal mieszkalny", symbol="M")
        expected_str = "lokal mieszkalny (M)"
        self.assertEqual(str(obj), expected_str)


class PersonTests(TestCase):
    def test_person_str(self):
        objects = (
            Person(
                first_name="Jan",
                last_name="Kowalski",
                role="Kierownik budowy",
                company="LECH",
            ),
            Person(first_name="Jan", last_name="Kowalski", role="Kierownik budowy"),
            Person(first_name="Jan", last_name="Kowalski", company="LECH"),
            Person(first_name="Jan", last_name="Kowalski"),
            Person(first_name="Jan"),
            Person(last_name="Kowalski"),
            Person(first_name="Jan", role="Kierownik budowy", company="LECH"),
            Person(first_name="Jan", role="Kierownik budowy"),
            Person(first_name="Jan", company="LECH"),
            Person(last_name="Kowalski", role="Kierownik budowy", company="LECH"),
            Person(last_name="Kowalski", role="Kierownik budowy"),
            Person(last_name="Kowalski", company="LECH"),
        )
        expected_strings = (
            "Jan Kowalski (LECH - Kierownik budowy)",
            "Jan Kowalski (Kierownik budowy)",
            "Jan Kowalski (LECH)",
            "Jan Kowalski",
            "Jan",
            "Kowalski",
            "Jan (LECH - Kierownik budowy)",
            "Jan (Kierownik budowy)",
            "Jan (LECH)",
            "Kowalski (LECH - Kierownik budowy)",
            "Kowalski (Kierownik budowy)",
            "Kowalski (LECH)",
        )
        for obj, expected_str in zip(objects, expected_strings):
            self.assertEqual(str(obj), expected_str)

    def test_email_recipient_property(self):
        person = Person.objects.create(
            first_name="Jan", last_name="Kowalski", e_mail="user@example.com"
        )
        self.assertEqual(person.email_recipient, "Jan Kowalski <user@example.com>")
        person = Person.objects.create()
        self.assertEqual(person.email_recipient, "")


class CustomerTest(TestCase):
    def test_customer_str(self):
        objects = (
            Customer(first_name="Jan", last_name="Kowalski"),
            Customer(first_name="Jan"),
            Customer(last_name="Kowalski"),
        )
        expected_strings = (
            "Jan Kowalski",
            "Jan",
            "Kowalski",
        )
        for obj, expected_str in zip(objects, expected_strings):
            self.assertEqual(str(obj), expected_str)


class CustomerHandlerTest(TestCase):
    def test_customer_handler_str(self):
        objects = ()
        expected_strings = ()
        for obj, expected_str in zip(objects, expected_strings):
            self.assertEqual(str(obj), expected_str)
        obj1 = CustomerHandler(first_name="Jan", last_name="Kowalski")
        obj2 = CustomerHandler(first_name="Jan")
        obj3 = CustomerHandler(last_name="Kowalski")
        expected_str1 = "Jan Kowalski"
        expected_str2 = "Jan"
        expected_str3 = "Kowalski"
        self.assertEqual(str(obj1), expected_str1)
        self.assertEqual(str(obj2), expected_str2)
        self.assertEqual(str(obj3), expected_str3)


class CostEstimateTest(TestCase):
    def test_cost_estimete_str(self):
        objects = (
            CostEstimate(
                file_name="T2-M39B - Kosztorys.pdf",
                net=1000.4,
                vat=80,
                gross=1080,
                construction_net=0,
                sanitary_net=0,
                electric_net=0,
                other_net=0,
                creation_date="2022-02-02",
                number="1",
                description="kosztorys wstępny",
            ),
            CostEstimate(
                file_name=None,
                net=1000.4,
                vat=80,
                gross=1080,
                construction_net=0,
                sanitary_net=0,
                electric_net=0,
                other_net=0,
                creation_date="2022-02-02",
                number="1",
                description="kosztorys wstępny",
            ),
            CostEstimate(
                file_name=None,
                net=1000.4,
                vat=80,
                gross=1080,
                construction_net=0,
                sanitary_net=0,
                electric_net=0,
                other_net=0,
                creation_date="2022-02-02",
                number="1",
                description=None,
            ),
        )
        expected_strings = (
            "T2-M39B - Kosztorys.pdf; 1000.40; kosztorys wstępny",
            "1000.40; kosztorys wstępny",
            "1000.40",
        )
        for obj, expected_str in zip(objects, expected_strings):
            self.assertEqual(str(obj), expected_str)


class CostEstimateOfProcedureTest(TestCase):
    def test_cost_estimate_of_procedure_str(self):
        procedure = Procedure()
        cost_estimate = CostEstimate(
            file_name="T2-M39B - Kosztorys.pdf",
            net=1000.4,
            vat=80,
            gross=1080,
            construction_net=0,
            sanitary_net=0,
            electric_net=0,
            other_net=0,
            creation_date="2022-02-02",
            number="1",
            description="kosztorys wstępny",
        )
        obj = CostEstimateOfProcedure(procedure=procedure, cost_estimate=cost_estimate)
        expected_str = f"{str(procedure)} ({str(cost_estimate)})"
        self.assertEqual(str(obj), expected_str)


class InvoiceTest(TestCase):
    def test_invoice_str(self):
        objects = (
            Invoice(
                number="1/2022",
                invoice_date="2022-02-02",
                due_date="2022-02-16",
                net=100,
                vat=8,
                gross=108,
            ),
            Invoice(
                number="1/2022",
                invoice_date="2022-02-02",
                due_date="2022-02-16",
                net=100,
                vat=8,
                gross=108,
                paid=True,
            ),
            Invoice(
                number=None,
                invoice_date="2022-02-02",
                due_date="2022-02-16",
                net=100,
                vat=8,
                gross=108,
                paid=True,
            ),
        )
        expected_strings = (
            "1/2022; 100.00; unpaid",
            "1/2022; 100.00; paid",
            "100.00; paid",
        )
        for obj, expected_str in zip(objects, expected_strings):
            self.assertEqual(str(obj), expected_str)


class CostTest(TestCase):
    def test_cost_str(self):
        obj = Cost(net=100, vat=8, gross=108, name="Projekt zamienny c.o.")
        expected_str = "Projekt zamienny c.o.; 108.00 zł brutto"
        self.assertEqual(str(obj), expected_str)


class KindOfCostTest(TestCase):
    def test_kind_of_cost(self):
        obj = KindOfCost(name="Projekt zamienny")
        expected_str = "Projekt zamienny"
        self.assertEqual(str(obj), expected_str)


class CustomerOfProcedureTest(TestCase):
    def test_customer_of_procedure_str(self):
        procedure = Procedure.objects.create()
        number = procedure.number
        customer = Customer(first_name="Anna", last_name="Kowalska")
        obj = CustomerOfProcedure(procedure=procedure, customer=customer)
        expected_str = f"Anna Kowalska ({number})"
        self.assertEqual(str(obj), expected_str)


class InvestmentStagePersonTests(TestCase):
    def test_str_method(self):
        investment_stage = baker.make("InvestmentStage")
        person = Person.objects.create(first_name="John", last_name="Smith")
        obj = InvestmentStagePerson.objects.create(
            person=person, investment_stage=investment_stage
        )
        self.assertEqual(str(obj), f"John Smith ({investment_stage.symbol})")


class EmailActionTests(TestCase):
    fixtures = ["email_action.json"]

    def setUp(self) -> None:
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
        self.ids = [str(hash(path))[-6:] for path in self.abs_file_paths]
        self.procedure = Procedure.objects.get(pk=1)
        self.procedure.directory = self.directory
        self.procedure.save()
        self.email_action = EmailAction.objects.get(pk=1)
        return super().setUp()

    def test_slug(self):
        obj = baker.make("EmailAction", slug="Invalid slug")
        correct_slug = slugify(obj.name)
        self.assertEqual(obj.slug, correct_slug)

    def test_get_recipients_empty(self):
        obj: EmailAction = baker.make("EmailAction")
        self.assertEqual(obj.get_recipients(), {"to": [], "cc": [], "bcc": []})

    def test_get_recipients_filled(self):
        obj = EmailAction.objects.get(pk=1)
        self.assertEqual(
            obj.get_recipients(),
            {
                "to": [
                    "Adam Kwiatkowski <gw1@company.com>",
                ],
                "cc": [
                    "Jerzy Kowalski <gw2@company.com>",
                    "Anna Sadowska <gw3@company.com>",
                ],
                "bcc": [],
            },
        )

    def test_get_attachments_path_for_procedure_errors(self):
        obj: EmailAction = baker.make("EmailAction")
        procedure = baker.make("Procedure", directory="invalid path")
        with self.assertRaises(TypeError):
            obj._get_attachments_path_for_procedure(13)
        with self.assertRaises(ValueError):
            obj._get_attachments_path_for_procedure(procedure)

    def test_get_attachments_path_for_procedure_return(self):
        expected_result = [
            (id, path) for id, path in zip(self.ids, self.abs_file_paths)
        ]
        result = self.email_action._get_attachments_path_for_procedure(self.procedure)
        self.assertEqual(result, expected_result)

    def test_get_attachments_to_form_errors(self):
        obj: EmailAction = baker.make("EmailAction")
        procedure = baker.make("Procedure", directory="invalid path")
        with self.assertRaises(TypeError):
            obj.get_attachments_to_form(13)
        with self.assertRaises(ValueError):
            obj.get_attachments_to_form(procedure)

    def test_get_attachments_to_form_return(self):
        rel_paths = [
            "URZ-N-M39B - Wniosek o zmiany aranżacyjne w mieszkaniu.pdf",
            "URZ-N-M39B - Kosztorys.ath",
            "URZ-N-M39B - Kosztorys.pdf",
            "PDF po zmianach\\plik_1.pdf",
            "PDF po zmianach\\plik_2.pdf",
        ]
        expected_result = [(id, rel_path) for id, rel_path in zip(self.ids, rel_paths)]
        result = self.email_action.get_attachments_to_form(self.procedure)
        self.assertEqual(result, expected_result)

    def test_get_attachments_by_id_errors(self):
        obj: EmailAction = baker.make("EmailAction")
        procedure = baker.make("Procedure", directory="invalid path")
        with self.assertRaises(TypeError):
            obj.get_attachments_by_id(procedure=13, id_list=[])
        with self.assertRaises(TypeError):
            obj.get_attachments_by_id(procedure=self.procedure, id_list=[1, 2])
        with self.assertRaises(ValueError):
            obj.get_attachments_by_id(procedure, id_list=[])

    def test_get_attachments_by_id_return(self):
        ids = self.ids[::2]
        expected_result = self.abs_file_paths[::2]
        result = self.email_action.get_attachments_by_id(self.procedure, ids)
        self.assertEqual(result, expected_result)

    def tearDown(self) -> None:
        rmtree(self.directory, ignore_errors=True)
        return super().tearDown()
