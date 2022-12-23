from django.contrib.auth import get_user_model
from django.test import TestCase

from zmiany_aranz.models import (
    Procedure, 
    Investment, 
    InvestmentStage, 
    Building, 
    Premises, 
    KindOfPremises, 
    Person, 
    Customer
)


class UsermanagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
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
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='foo')


    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
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
                email='super@user.com', password='foo', is_superuser=False)


class ProcedureTests(TestCase):
    
    def setUp(self) -> None:
        Procedure.objects.create()
        Procedure.objects.create()

    def test_procedure_number_one(self):
        from datetime import date
        current_year = date.today().year
        expected_number = f"001/{str(current_year)[-2:]}"
        procedure = Procedure.objects.get(pk=1)
        self.assertEqual(procedure.number, expected_number)

    def test_procedure_number_two(self):
        from datetime import date
        current_year = date.today().year
        expected_number = f"002/{str(current_year)[-2:]}"
        procedure = Procedure.objects.get(pk=2)
        self.assertEqual(procedure.number, expected_number)


class InvestmentTests(TestCase):
    def test_investment_str(self):
        investment = Investment(name='Urzecze', symbol='URZ')
        excected_str = 'Urzecze (URZ)'
        self.assertEqual(str(investment), excected_str)
class InvestmentStageTests(TestCase):
    def test_investment_stage_str(self):
        obj = InvestmentStage(name='Urzecze II', symbol='URZ-K')
        excected_str = 'Urzecze II (URZ-K)'
        self.assertEqual(str(obj), excected_str)


class BuildingTests(TestCase):
    def test_building_str(self):
        obj = Building(name='Urzecze II, budynek A', symbol='URZ-K-A')
        excected_str = 'Urzecze II, budynek A (URZ-K-A)'
        self.assertEqual(str(obj), excected_str)


class PremisesTests(TestCase):
    def test_premises_str(self):
        obj = Premises(symbol='T2-M39B')
        expected_str = 'T2-M39B'
        self.assertEqual(str(obj), expected_str)


class KindOfPremisesTests(TestCase):
    def test_kind_of_premises_str(self):
        obj = KindOfPremises(name='lokal mieszkalny', symbol='M')
        expected_str = 'lokal mieszkalny (M)'
        self.assertEqual(str(obj), expected_str)


class PersonTests(TestCase):
    def test_person_str(self):
        obj1 = Person(first_name='Jan', last_name='Kowalski', role='Kierownik budowy', company='LECH')
        obj2 = Person(first_name='Jan', last_name='Kowalski', role='Kierownik budowy')
        obj3 = Person(first_name='Jan', last_name='Kowalski', company='LECH')
        obj4 = Person(first_name='Jan', last_name='Kowalski')
        obj5 = Person(first_name='Jan')
        obj6 = Person(last_name='Kowalski')
        obj7 = Person(first_name='Jan', role='Kierownik budowy', company='LECH')
        obj8 = Person(first_name='Jan', role='Kierownik budowy')
        obj9 = Person(first_name='Jan', company='LECH')
        obj10 = Person(last_name='Kowalski', role='Kierownik budowy', company='LECH')
        obj11 = Person(last_name='Kowalski', role='Kierownik budowy')
        obj12 = Person(last_name='Kowalski', company='LECH')
        expected_str1 = 'Jan Kowalski (LECH - Kierownik budowy)'
        expected_str2 = 'Jan Kowalski (Kierownik budowy)'
        expected_str3 = 'Jan Kowalski (LECH)'
        expected_str4 = 'Jan Kowalski'
        expected_str5 = 'Jan'
        expected_str6 = 'Kowalski'
        expected_str7 = 'Jan (LECH - Kierownik budowy)'
        expected_str8 = 'Jan (Kierownik budowy)'
        expected_str9 = 'Jan (LECH)'
        expected_str10 = 'Kowalski (LECH - Kierownik budowy)'
        expected_str11 = 'Kowalski (Kierownik budowy)'
        expected_str12 = 'Kowalski (LECH)'
        self.assertEqual(str(obj1), expected_str1)
        self.assertEqual(str(obj2), expected_str2)
        self.assertEqual(str(obj3), expected_str3)
        self.assertEqual(str(obj4), expected_str4)
        self.assertEqual(str(obj5), expected_str5)
        self.assertEqual(str(obj6), expected_str6)
        self.assertEqual(str(obj7), expected_str7)
        self.assertEqual(str(obj8), expected_str8)
        self.assertEqual(str(obj9), expected_str9)
        self.assertEqual(str(obj10), expected_str10)
        self.assertEqual(str(obj11), expected_str11)
        self.assertEqual(str(obj12), expected_str12)


class CustomerTest(TestCase):
    def test_customer_str(self):
        obj1 = Customer(first_name='Jan', last_name='Kowalski')
        obj2 = Customer(first_name='Jan')
        obj3 = Customer(last_name='Kowalski')
        expected_str1 = 'Jan Kowalski'
        expected_str2 = 'Jan'
        expected_str3 = 'Kowalski'
        self.assertEqual(str(obj1), expected_str1)
        self.assertEqual(str(obj2), expected_str2)
        self.assertEqual(str(obj3), expected_str3)

