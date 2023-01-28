from typing import *
import os.path
from glob import glob

from django.db import models
from django.db.models import Max
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.template.defaultfilters import slugify

from zmiany_aranz.string_replacer import Replacer

from .managers import CustomUserManager
from .apps import ZmianyAranzConfig

APP_NAME = ZmianyAranzConfig.name

# https://learndjango.com/tutorials/django-custom-user-model


# Użytkownik
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# Procedura
class Procedure(models.Model):
    """Model definition for Procedure."""

    class InvoiceStatusChoices(models.IntegerChoices):
        INDETERMINATE = 0, ("Nieokreślony")
        FOR_ISSUING = 1, ("Do wystawienia")
        ISSUED = 2, ("Wystawiona")
        SENT = 3, ("Wysłana")
        PAID = 4, ("Opłacona")
        CANCELED = 5, ("Anulowana - korekta")

    class ProcedureStatus(models.IntegerChoices):
        INDETERMINATE = 0, ("Nieokreślony")
        STARTED = 1, ("Rozpoczęta")
        FINISHED = 2, ("Zakończona")

    _number = models.IntegerField(editable=False)
    _year = models.CharField(max_length=4, editable=False)
    premises = models.ManyToManyField("Premises", blank=True, related_name="precedures")
    customers = models.ManyToManyField(
        "Customer", through="CustomerOfProcedure", blank=True, related_name="procedures"
    )
    persons = models.ManyToManyField("Person", blank=True, related_name="procedures")
    customer_handler = models.ManyToManyField(
        "CustomerHandler", blank=True, related_name="procedures"
    )
    invoices = models.ManyToManyField("Invoice", blank=True, related_name="procedures")
    cost_estimates = models.ManyToManyField(
        "CostEstimate",
        through="CostEstimateOfProcedure",
        blank=True,
        related_name="procedures",
    )  # or ForeignKey in CostEstimate
    costs = models.ManyToManyField("Cost", blank=True, related_name="procedures")
    status = models.IntegerField(
        choices=ProcedureStatus.choices, default=ProcedureStatus.INDETERMINATE
    )
    invoice_status = models.IntegerField(
        choices=InvoiceStatusChoices.choices, default=InvoiceStatusChoices.INDETERMINATE
    )
    invoice_month = models.DateField(
        null=True, blank=True
    )  # da się zrobić ograniczenie, że bez dnia?
    gross_fee_for_arran_changes = models.DecimalField(
        max_digits=6, decimal_places=2, default=650.00
    )
    accepted = models.BooleanField(
        default=False
    )  # do zestawienia faktur - jako przyjęte, ale faktura niekoniecznie wystawiona
    directory = models.CharField(
        max_length=260, null=True, blank=True
    )  # może models.FilePathField?
    comment = models.TextField(null=True, blank=True)
    # TODO: dodać pole customer (oprócz person)

    # umowy chyba niepotrzebne, mogą być szukane na bieżąco w crm?? może jako osobna funkcja/właściwość
    # zakres zmian? jakaś checklista? do tej pory nie miałem

    # TODO: wykrywanie zmian osób przynależnych do procedury (zmiana właścicieli mieszkania)

    @property
    def number(self):
        """
        Return a procedure number in format nn/yyyy.
        nn: next number
        yyyy: year
        """
        number = str(self._number).zfill(3)
        year = self._year[-2:]
        return f"{number}/{year}"

    @classmethod
    def _get_new_number_and_year(cls) -> Tuple[int, str]:
        """Return next procedure number and current year."""
        from datetime import date

        current_year = date.today().year
        max_numer = cls.objects.filter(
            _year__in=(current_year, str(current_year)[-2:])
        ).aggregate(Max("_number"))["_number__max"]
        number = max_numer + 1 if max_numer else 1
        year = str(current_year)
        return number, year

    def save(self, *args, **kwargs):
        if self.id is None:
            self._number, self._year = self._get_new_number_and_year()
        return super().save(*args, **kwargs)

    class Meta:
        """Meta definition for Procedure."""

        verbose_name = "Procedure"
        verbose_name_plural = "Procedures"
        unique_together = ("_number", "_year")

    def __str__(self) -> str:
        """Unicode representation of Procedure."""
        return self.number

    @property
    def building(self):
        premises_first = self.premises.first()
        if premises_first is None:
            return None
        return premises_first.building

    @property
    def investment_stage(self):
        if self.building is None:
            return None
        return self.building.investment_stage

    @property
    def investment(self):
        if self.investment_stage is None:
            return None
        return self.investment_stage.investment


# Klient procedury
class CustomerOfProcedure(models.Model):
    """Model definition for CustomerOfProcedure."""

    procedure = models.ForeignKey("Procedure", on_delete=models.CASCADE)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    shares = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True,
        blank=True,
    )  # Udziały

    class Meta:
        """Meta definition for CustomerOfProcedure."""

        verbose_name = "CustomerOfProcedure"
        verbose_name_plural = "CustomerOfProcedures"

    def __str__(self):
        """Unicode representation of CustomerOfProcedure."""
        return f"{str(self.customer)} ({str(self.procedure)})"


# Inwestycja
class Investment(models.Model):
    """Model definition for Investment."""

    # THINK: czy jest potrzebne odniesienie od TBL_INWESTYCJE w CRM? Chyba nie
    symbol = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        """Meta definition for Investment."""

        verbose_name = "Investment"
        verbose_name_plural = "Investments"

    def __str__(self) -> str:
        """Unicode representation of Investment."""
        return f"{self.name} ({self.symbol})"


# Etap Inwestycji
class InvestmentStage(models.Model):
    """Model definition for InvestmentStage."""

    investment = models.ForeignKey("Investment", on_delete=models.SET_NULL, null=True)
    symbol = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=30, unique=True)
    number_of_flats = models.PositiveIntegerField(null=True, blank=True)
    persons = models.ManyToManyField(
        "Person", through="InvestmentStagePerson", blank=True
    )

    # link do tabeli G-Sheets?
    # link do folderu G-Drive?

    class Meta:
        """Meta definition for InvestmentStage."""

        verbose_name = "InvestmentStage"
        verbose_name_plural = "InvestmentStages"

    def __str__(self) -> str:
        """Unicode representation of InvestmentStage."""
        return f"{self.name} ({self.symbol})"


# Budynek
class Building(models.Model):
    """Model definition for Building."""

    # THINK: czy jest potzebne odniesienie od TBL_BUDYNKI w CRM? Chyba nie
    investment_stage = models.ForeignKey(
        "InvestmentStage", on_delete=models.SET_NULL, null=True
    )
    symbol = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=30, unique=True)
    location_desc = models.CharField(max_length=50)

    class Meta:
        """Meta definition for Building."""

        verbose_name = "Building"
        verbose_name_plural = "Buildings"

    def __str__(self) -> str:
        """Unicode representation of Building."""
        return f"{self.name} ({self.symbol})"


# Lokal
# TODO: do sprawdzenia tłumaczenie
class Premises(models.Model):
    """Model definition for Premises."""

    id_crm: int = models.IntegerField(unique=True, null=True, blank=True)
    symbol: str = models.CharField(max_length=20, unique=True)
    building = models.ForeignKey("Building", on_delete=models.SET_NULL, null=True)
    kind = models.ForeignKey("KindOfPremises", on_delete=models.SET_NULL, null=True)
    staircase: str = models.CharField(
        max_length=10, null=True, blank=True
    )  # klatka schodowa
    storey: str = models.CharField(
        max_length=10, null=True, blank=True
    )  # kondygnacja, liczona od zera

    class Meta:
        """Meta definition for Premises."""

        verbose_name = "Premises"
        verbose_name_plural = "Premisess"

    def __str__(self) -> str:
        """Unicode representation of Premises."""
        return self.symbol


# Typy lokali - edycja raczej tylko w adminie
class KindOfPremises(models.Model):
    """Model definition for KindOfPremises."""

    symbol = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        """Meta definition for KindOfPremises."""

        verbose_name = "KindOfPremises"
        verbose_name_plural = "KindOfPremisess"

    def __str__(self) -> str:
        """Unicode representation of KindOfPremises."""
        return f"{self.name} ({self.symbol})"


# Osoba - klasa Abstrakcyjna
class PersonAbstract(models.Model):
    """Model definition for Person."""

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    e_mail = models.EmailField(null=True, blank=True)

    class Meta:
        """Meta definition for Person."""

        verbose_name = "Person"
        verbose_name_plural = "Persons"
        abstract = True

    def __str__(self) -> str:
        """Unicode representation of PersonAbstract."""
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    @property
    def email_recipient(self) -> str:
        """Return an email recipients if exist, else empty str."""
        if not self.e_mail:
            return ""
        return f"{self.first_name} {self.last_name} <{self.e_mail}>".strip()


# Osoba
class Person(PersonAbstract):
    """Model definition for Person."""

    company = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        """Meta definition for Person."""

        verbose_name = "Person"
        verbose_name_plural = "Persons"

    def __str__(self):
        """Unicode representation of Person."""
        result = super().__str__()
        if self.company and self.role:
            result += " (" + self.company + " - " + self.role + ")"
        elif self.company:
            result += " (" + self.company + ")"
        elif self.role:
            result += " (" + self.role + ")"
        return result.strip()


# Klient
class Customer(PersonAbstract):
    """Model definition for Customer."""

    id_crm: int = models.IntegerField(
        null=True, blank=True
    )  # rezygnacja z unique=True ze względu na zachowanie historii

    class Meta:
        """Meta definition for Customer."""

        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        """Unicode representation of Customer."""
        return super().__str__()

    def get_absolute_url(self) -> str:
        return reverse(f"{APP_NAME}:customer_detail", kwargs={"pk": self.pk})


# Opiekun Klienta - edycja raczej tylko w adminie
class CustomerHandler(PersonAbstract):
    """Model definition for CustomerHandler."""

    class BranchChoices(models.IntegerChoices):
        TORUN = 0, ("Toruń")
        BYDGOSZCZ = 1, ("Bydgoszcz")
        OLSZTYN = 2, ("Olsztyn")
        WARSZAWA = 3, ("Warszawa")

    branch = models.IntegerField(choices=BranchChoices.choices)

    class Meta:
        """Meta definition for CustomerHandler."""

        verbose_name = "CustomerHandler"
        verbose_name_plural = "CustomerHandlers"

    def __str__(self):
        """Unicode representation of CustomerHandler."""
        return super().__str__()


# Kosztorys
class CostEstimate(models.Model):
    """Model definition for CostEstimate."""

    file_name = models.CharField(max_length=50, null=True, blank=True)
    net = models.DecimalField(max_digits=8, decimal_places=2)
    vat = models.DecimalField(max_digits=7, decimal_places=2)
    gross = models.DecimalField(max_digits=8, decimal_places=2)
    construction_net = models.DecimalField(max_digits=8, decimal_places=2)
    sanitary_net = models.DecimalField(max_digits=8, decimal_places=2)
    electric_net = models.DecimalField(max_digits=8, decimal_places=2)
    other_net = models.DecimalField(max_digits=8, decimal_places=2)
    creation_date = models.DateField()
    added_date = models.DateTimeField(auto_now_add=True)
    number: str = models.CharField(max_length=10, null=True, blank=True)
    description: str = models.TextField(null=True, blank=True)

    class Meta:
        """Meta definition for CostEstimate."""

        verbose_name = "CostEstimate"
        verbose_name_plural = "CostEstimates"

    def __str__(self) -> str:
        """Unicode representation of CostEstimate."""
        return (
            f"{self.file_name or ''}; {self.net:.2f}; {self.description or ''}".strip(
                "; "
            )
        )


# Kosztorys procedury - Through Model
class CostEstimateOfProcedure(models.Model):
    """Model definition for CostEstimateOfProcedure."""

    procedure = models.ForeignKey("Procedure", on_delete=models.CASCADE)
    cost_estimate = models.ForeignKey("CostEstimate", on_delete=models.CASCADE)
    for_customer = models.BooleanField(default=False)
    for_general_contractor = models.BooleanField(default=False)

    class Meta:
        """Meta definition for CostEstimateOfProcedure."""

        verbose_name = "CostEstimateOfProcedure"
        verbose_name_plural = "CostEstimateOfProcedures"

    def __str__(self) -> str:
        """Unicode representation of CostEstimateOfProcedure."""
        return f"{str(self.procedure)} ({str(self.cost_estimate)})"


# Faktura
class Invoice(models.Model):
    """Model definition for Invoice."""

    file = models.FileField(upload_to="invoices", null=True, blank=True)
    number: str = models.CharField(max_length=50, null=True, blank=True)
    invoice_date = models.DateField()
    due_date = models.DateField()
    net = models.DecimalField(max_digits=8, decimal_places=2)
    vat = models.DecimalField(max_digits=7, decimal_places=2)
    gross = models.DecimalField(max_digits=8, decimal_places=2)
    description: str = models.TextField(null=True, blank=True)
    paid = models.BooleanField(default=False)

    # TODO: property "w_terminie"

    class Meta:
        """Meta definition for Invoice."""

        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self) -> str:
        """Unicode representation of Invoice."""
        return f"{self.number or ''}; {self.net:.2f}; {'paid' if self.paid else 'unpaid'}".strip(
            "; "
        )


# Koszty
class Cost(models.Model):
    """Model definition for Cost."""

    net = models.DecimalField(max_digits=8, decimal_places=2)
    vat = models.DecimalField(max_digits=7, decimal_places=2)
    gross = models.DecimalField(max_digits=8, decimal_places=2)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    kind = models.ForeignKey("KindOfCost", on_delete=models.SET_NULL, null=True)

    class Meta:
        """Meta definition for Cost."""

        verbose_name = "Cost"
        verbose_name_plural = "Costs"

    def __str__(self) -> str:
        """Unicode representation of Cost."""
        return f"{self.name}; {self.gross:.2f} zł brutto".strip("; ")


# Typ Kosztu
class KindOfCost(models.Model):
    """Model definition for KindOfCost."""

    name = models.CharField(max_length=100)

    class Meta:
        """Meta definition for KindOfCost."""

        verbose_name = "KindOfCost"
        verbose_name_plural = "KindOfCosts"

    def __str__(self):
        """Unicode representation of KindOfCost."""
        return self.name


class InvestmentStagePerson(models.Model):
    """Model definition for InvestmentStagePerson."""

    investment_stage = models.ForeignKey("InvestmentStage", on_delete=models.CASCADE)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)

    class Meta:
        """Meta definition for InvestmentStagePerson."""

        verbose_name = "InvestmentStagePerson"
        verbose_name_plural = "InvestmentStagePersons"

    def __str__(self):
        """Unicode representation of InvestmentStagePerson."""
        return f"{self.person} ({self.investment_stage.symbol})"


class EmailActionPerson(models.Model):
    """Model definition for EmailActionPerson."""

    class Role(models.IntegerChoices):
        TO = 1, "TO"
        CC = 2, "CC"
        BCC = 3, "BCC"

    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    email_action = models.ForeignKey("EmailAction", on_delete=models.CASCADE)
    role = models.IntegerField(choices=Role.choices)

    def __str__(self) -> str:
        """Unicode representation of EmailActionPerson."""
        return f"{self.email_action} ({self.person})"


class EmailAction(models.Model):
    """Model definition for EmailAction."""

    investment_stage = models.ForeignKey(
        InvestmentStage, on_delete=models.CASCADE, null=True, blank=True
    )
    persons = models.ManyToManyField("Person", through="EmailActionPerson")
    name = models.CharField(max_length=30)
    mail_subject = models.CharField(max_length=100, null=True, blank=True)
    mail_body = models.TextField(null=True, blank=True)
    mail_attachments = models.TextField(null=True, blank=True)
    is_template = models.BooleanField(default=False)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ("investment_stage", "slug")

    def get_recipients(self) -> Dict[str, List[str]]:
        """Return a dict of email recipients. Dict keys: ['to', 'cc', 'bcc']."""

        to = self.persons.filter(emailactionperson__role=EmailActionPerson.Role.TO)
        cc = self.persons.filter(emailactionperson__role=EmailActionPerson.Role.CC)
        bcc = self.persons.filter(emailactionperson__role=EmailActionPerson.Role.BCC)
        result = {
            "to": [person.email_recipient for person in to],
            "cc": [person.email_recipient for person in cc],
            "bcc": [person.email_recipient for person in bcc],
        }
        return result

    def _get_attachments_path_for_procedure(
        self, procedure, relative=False
    ) -> List[Tuple[str, str]]:
        """Return a list of tuples (id, path) for attachments.
        If `relative = True` path is relative to root directory of procedure."""
        if not isinstance(procedure, Procedure):
            raise TypeError(
                f"procedure must be a Procedure instance, not {procedure.__class__.__name__}."
            )
        root_dir = os.path.abspath(procedure.directory)
        if not os.path.isdir(root_dir):
            raise ValueError(
                "Path is incorrect. Expected path to root directory of procedure."
            )
        procedure_replacer = Replacer(procedure)
        path_patterns = [
            line
            for line in [line.strip() for line in self.mail_attachments.split("\r\n")]
            if line
        ]
        abs_path_patterns = [
            procedure_replacer(os.path.join(root_dir, pattern))
            for pattern in path_patterns
        ]
        paths = []
        for _path in abs_path_patterns:
            paths.extend(glob(_path))
        paths = [path for path in paths if os.path.isfile(path)]
        hash_list = [str(hash(path))[-6:] for path in paths]
        if relative:
            paths = [p[len(root_dir) :].strip(r"\/ ") for p in paths]
        return list(zip(hash_list, paths))

    def get_attachments_to_form(self, procedure: Procedure) -> List[Tuple]:
        """Return a list of tuples (id, path) for attachments.
        Path is relative to root directory of procedure."""

        return self._get_attachments_path_for_procedure(procedure, relative=True)

    def get_attachments_by_id(self, procedure: Procedure, id_list: List[str]):
        """Return a list of absolute path of attachments  if `hash(path)[-6:]`
        is in `id_list` and path matches the pattern specified
        in self.mail_attachments field."""
        if not isinstance(id_list, list):
            raise TypeError(
                f"id_list must be a list, not {id_list.__class__.__name__}."
            )
        if not all([isinstance(id, str) for id in id_list]):
            raise TypeError("id_list must be a list of str.")
        paths = self._get_attachments_path_for_procedure(procedure)
        return [path for (id, path) in paths if id in id_list]


# Model PozycjaKosztorysu??

# Oddzialna aplikacja do pobierania danych z CRM?
# Oddzialna aplikacja do Google API?
# Oddzialna aplikacja do Outlook?
