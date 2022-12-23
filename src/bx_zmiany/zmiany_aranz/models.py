from django.db import models
from django.db.models import Max
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

# https://learndjango.com/tutorials/django-custom-user-model


# Użytkownik
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# Procedura
class Procedure(models.Model):
    """Model definition for Procedure."""

    class InvoiceStatusChoices(models.IntegerChoices):
        INDETERMINATE = 0, ('Nieokreślony')
        FOR_ISSUING = 1, ('Do wystawienia')
        ISSUED = 2, ('Wystawiona')
        SENT = 3, ('Wysłana')
        PAID = 4, ('Opłacona')
        CANCELED = 5, ('Anulowana - korekta')

    class ProcedureStatus(models.IntegerChoices):
        INDETERMINATE = 0, ('Nieokreślony')
        STARTED = 1, ('Rozpoczęta')
        FINISHED = 2, ('Zakończona')

    _number = models.IntegerField(editable=False)
    _year = models.CharField(max_length=4, editable=False)
    premises = models.ManyToManyField('Premises', blank=True, related_name='precedures') # TODO: do sprawdzenia model odniesienia
    customers = models.ManyToManyField('Customer', through='CustomerOfProcedure', blank=True, related_name='proceudres')
    persons = models.ManyToManyField('Person', blank=True, related_name='procedures')
    customer_handler = models.ManyToManyField('CustomerHandler', blank=True, related_name='procedures')
    invoices = models.ManyToManyField('Invoice', blank=True, related_name='procedures')
    cost_estimates = models.ManyToManyField('CostEstimate', through='CostEstimateOfProcedure', blank=True, related_name='procedures') # or ForeignKey in CostEstimate
    costs = models.ManyToManyField('Cost', blank=True, related_name='procedures')
    status = models.IntegerField(choices=ProcedureStatus.choices, default=ProcedureStatus.INDETERMINATE)
    invoice_status = models.IntegerField(choices=InvoiceStatusChoices.choices, default=InvoiceStatusChoices.INDETERMINATE)
    invoice_month = models.DateField(null=True, blank=True)  # da się zrobić ograniczenie, że bez dnia? 
    gross_fee_for_arran_changes = models.DecimalField(max_digits=6, decimal_places=2, default=650.00)
    accepted = models.BooleanField(default=False) # do zestawienia faktur - jako przyjęte, ale faktura niekoniecznie wystawiona
    directory = models.CharField(max_length=260, null=True, blank=True)  # może models.FilePathField? 
    comment = models.TextField(null=True, blank=True)

    # umowy chyba niepotrzebne, mogą być szukane na bieżąco w crm?? może jako osobna funkcja/właściwość
    # zakres zmian? jakaś checklista? do tej pory nie miałem 

    # TODO: wykrywanie zmian osób przynależnych do procedury (zmiana właścicieli mieszkania)

    @property
    def number(self):
        number = str(self._number).zfill(3)
        year = self._year[-2:]
        return f"{number}/{year}"

    @classmethod
    def _get_new_number_and_year(cls):
        from datetime import date
        current_year = date.today().year
        max_numer = cls.objects.filter(_year__in=(current_year, str(current_year)[-2:])).aggregate(Max('_number'))['_number__max']
        number = max_numer + 1 if max_numer else 1
        year = str(current_year)
        return number, year
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self._number, self._year = self._get_new_number_and_year()
        return super().save(*args, **kwargs)

    class Meta:
        """Meta definition for Procedure."""

        verbose_name = 'Procedure'
        verbose_name_plural = 'Procedures'
        unique_together = ('_number', '_year')

    def __str__(self) -> str:
        return self.number


# Klient procedury
class CustomerOfProcedure(models.Model):
    """Model definition for CustomerOfProcedure."""

    # TODO: Define fields here
    procedure = models.ForeignKey('Procedure', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    shares = models.FloatField(null=True, blank=True)  # Udziały

    class Meta:
        """Meta definition for CustomerOfProcedure."""

        verbose_name = 'CustomerOfProcedure'
        verbose_name_plural = 'CustomerOfProcedures'

    def __str__(self):
        """Unicode representation of CustomerOfProcedure."""
        pass


# Inwestycja
class Investment(models.Model):
    """Model definition for Investment."""

    # TODO: czy jest potrzebne odniesienie od TBL_INWESTYCJE w CRM? Chyba nie
    symbol = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        """Meta definition for Investment."""

        verbose_name = 'Investment'
        verbose_name_plural = 'Investments'

    def __str__(self) -> str:
        """Unicode representation of Investment."""
        return f"{self.name} ({self.symbol})"


# Etap Inwestycji
class InvestmentStage(models.Model):
    """Model definition for InvestmentStage."""

    investment = models.ForeignKey('Investment', on_delete=models.SET_NULL, null=True)
    symbol = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=30, unique=True)
    number_of_flats = models.PositiveIntegerField(null=True, blank=True)

    # link do tabeli G-Sheets?
    # link do folderu G-Drive?

    class Meta:
        """Meta definition for InvestmentStage."""

        verbose_name = 'InvestmentStage'
        verbose_name_plural = 'InvestmentStages'

    def __str__(self) -> str:
        """Unicode representation of InvestmentStage."""
        return f"{self.name} ({self.symbol})"


# Budynek
class Building(models.Model):
    """Model definition for Building."""
    
    # TODO: czy jest potzebne odniesienie od TBL_BUDYNKI w CRM? Chyba nie
    investment_stage = models.ForeignKey('InvestmentStage', on_delete=models.SET_NULL, null=True)
    symbol = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=30, unique=True)
    location_desc = models.CharField(max_length=50)

    class Meta:
        """Meta definition for Building."""

        verbose_name = 'Building'
        verbose_name_plural = 'Buildings'

    def __str__(self) -> str:
        """Unicode representation of Building."""
        return f"{self.name} ({self.symbol})"


# Lokal
# TODO: do sprawdzenia tłumaczenie
class Premises(models.Model):
    """Model definition for Premises."""

    id_crm: int = models.IntegerField(unique=True, null=True, blank=True)
    symbol: str = models.CharField(max_length=20, unique=True)
    building = models.ForeignKey('Building', on_delete=models.SET_NULL, null=True)
    kind = models.ForeignKey('KindOfPremises', on_delete=models.SET_NULL, null=True)
    staircase: str = models.CharField(max_length=10, null=True, blank=True)  # klatka schodowa
    storey: str = models.CharField(max_length=10, null=True, blank=True)  # kondygnacja, liczona od zera

    class Meta:
        """Meta definition for Premises."""

        verbose_name = 'Premises'
        verbose_name_plural = 'Premisess'

    def __str__(self) -> str:
        """Unicode representation of Premises."""
        return self.symbol


# Typy lokali
class KindOfPremises(models.Model):
    """Model definition for KindOfPremises."""

    # TODO: Define fields here
    # mieszkalny, usługowy, miejsce postojowe, garaż, komórka lokatorska
    symbol = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        """Meta definition for KindOfPremises."""

        verbose_name = 'KindOfPremises'
        verbose_name_plural = 'KindOfPremisess'

    def __str__(self) -> str:
        """Unicode representation of KindOfPremises."""
        return f"{self.name} ({self.symbol})"


# Osoba - klasa Abstrakcyjna
class PersonAbstract(models.Model):
    """Model definition for Person."""

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone= models.CharField(max_length=15, null=True, blank=True)
    e_mail = models.EmailField(null=True, blank=True)
    
    class Meta:
        """Meta definition for Person."""

        verbose_name = 'Person'
        verbose_name_plural = 'Persons'
        abstract = True

    def __str__(self):
        """Unicode representation of PersonAbstract."""
        return f"{self.first_name or ''} {self.last_name or ''}".strip()


# Osoba
class Person(PersonAbstract):
    """
    Model definition for Person.
    
    Attributes
    ----------
    first_name : str
    last_name : str
    phone : str
    e_mail : str
    role : str
    company : str
    """

    company = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        """Meta definition for Person."""

        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

    def __str__(self):
        """Unicode representation of Person."""
        result = ''
        if self.first_name:
            result += self.first_name
        if self.last_name:
            result +=  ' ' + self.last_name
        if self.company and self.role:
            result += ' (' + self.company + ' - ' + self.role + ')'
        elif self.company:
            result += ' (' + self.company + ')'
        elif self.role:
            result += ' (' + self.role + ')'
        return result.strip()


# Klient
class Customer(PersonAbstract):
    """Model definition for Customer."""

    id_crm: int = models.IntegerField(null=True, blank=True)  # rezygnacja z unique=True ze względu na zachowanie historii

    class Meta:
        """Meta definition for Customer."""

        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        """Unicode representation of Customer."""
        return super().__str__()


# Opiekun Klienta
class CustomerHandler(PersonAbstract):
    """Model definition for CustomerHandler."""

    class BranchChoices(models.IntegerChoices):
        TORUN = 0, ('Toruń')
        BYDGOSZCZ = 1, ('Bydgoszcz')
        OLSZTYN = 2, ('Olsztyn')
        WARSZAWA = 3, ('Warszawa')

    branch = models.IntegerField(choices=BranchChoices.choices)

    class Meta:
        """Meta definition for CustomerHandler."""

        verbose_name = 'CustomerHandler'
        verbose_name_plural = 'CustomerHandlers'

    def __str__(self):
        """Unicode representation of CustomerHandler."""
        pass


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
    number: int = models.CharField(max_length=10, null=True, blank=True)
    description: str = models.TextField(null=True, blank=True)

    class Meta:
        """Meta definition for CostEstimate."""

        verbose_name = 'CostEstimate'
        verbose_name_plural = 'CostEstimates'

    def __str__(self):
        """Unicode representation of CostEstimate."""
        pass


# Kosztorys procedury - Through Model
class CostEstimateOfProcedure(models.Model):
    """Model definition for CostEstimateOfProcedure."""

    procedure = models.ForeignKey('Procedure', on_delete=models.CASCADE)
    cost_estimate = models.ForeignKey('CostEstimate', on_delete=models.CASCADE)
    for_customer = models.BooleanField(default=False)
    for_general_contractor = models.BooleanField(default=False)

    class Meta:
        """Meta definition for CostEstimateOfProcedure."""

        verbose_name = 'CostEstimateOfProcedure'
        verbose_name_plural = 'CostEstimateOfProcedures'

    def __str__(self):
        """Unicode representation of CostEstimateOfProcedure."""
        pass


# Faktura
class Invoice(models.Model):
    """Model definition for Invoice."""

    file = models.FileField(upload_to='invoices', null=True, blank=True)
    number: int = models.CharField(max_length=10, null=True, blank=True)
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

        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def __str__(self):
        """Unicode representation of Invoice."""
        pass


# Koszty
class Cost(models.Model):
    """Model definition for Cost.
    Like [project_replacement, `ocena koncepcji zmian`, ...]
    """

    net = models.DecimalField(max_digits=8, decimal_places=2)
    vat = models.DecimalField(max_digits=7, decimal_places=2)
    gross = models.DecimalField(max_digits=8, decimal_places=2)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    kind = models.ForeignKey('KindOfCost', on_delete=models.SET_NULL, null=True)

    class Meta:
        """Meta definition for Cost."""

        verbose_name = 'Cost'
        verbose_name_plural = 'Costs'

    def __str__(self):
        """Unicode representation of Cost."""
        pass


# Typ Kosztu
class KindOfCost(models.Model):
    """Model definition for KindOfCost."""

    # TODO: Define fields here
    name = models.CharField(max_length=100)

    class Meta:
        """Meta definition for KindOfCost."""

        verbose_name = 'KindOfCost'
        verbose_name_plural = 'KindOfCosts'

    def __str__(self):
        """Unicode representation of KindOfCost."""
        pass


# Model PozycjaKosztorysu??

# Oddzialna aplikacja do pobierania danych z CRM?
# Oddzialna aplikacja do Google API?
# Oddzialna aplikacja do Outlook?
        