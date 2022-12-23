from django.contrib.auth import get_user_model
from django.test import TestCase

from zmiany_aranz.models import Procedure


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

class ProcedureTeste(TestCase):
    
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
