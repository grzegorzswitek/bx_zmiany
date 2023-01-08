from django.db import models


class TblInwestycje(models.Model):
    id_inwestycji = models.AutoField(db_column="ID_INWESTYCJI", primary_key=True)
    numer_fk = models.CharField(
        db_column="NUMER_FK", max_length=15, blank=True, null=True
    )
    oznaczenie = models.CharField(
        db_column="OZNACZENIE", max_length=100, blank=True, null=True
    )
    opis = models.CharField(db_column="OPIS", max_length=2000, blank=True, null=True)
    wojewodztwo = models.CharField(
        db_column="WOJEWODZTWO", max_length=30, blank=True, null=True
    )
    miasto = models.CharField(db_column="MIASTO", max_length=30, blank=True, null=True)
    ulica = models.CharField(db_column="ULICA", max_length=30, blank=True, null=True)
    nr_dzialki = models.CharField(
        db_column="NR_DZIALKI", max_length=100, blank=True, null=True
    )
    kod = models.CharField(db_column="KOD", max_length=10, blank=True, null=True)
    poczta = models.CharField(db_column="POCZTA", max_length=30, blank=True, null=True)
    sciezka = models.CharField(
        db_column="SCIEZKA", max_length=100, blank=True, null=True
    )
    pow_dzialki = models.FloatField(db_column="POW_DZIALKI", blank=True, null=True)
    pow_uzytkowa = models.FloatField(db_column="POW_UZYTKOWA", blank=True, null=True)
    pow_komunikacyjna = models.FloatField(
        db_column="POW_KOMUNIKACYJNA", blank=True, null=True
    )
    pow_techniczna = models.FloatField(
        db_column="POW_TECHNICZNA", blank=True, null=True
    )
    pow_garazu = models.FloatField(db_column="POW_GARAZU", blank=True, null=True)
    pow_komorek = models.FloatField(db_column="POW_KOMOREK", blank=True, null=True)
    kto_dodal = models.CharField(db_column="KTO_DODAL", max_length=50)
    data_dodania = models.DateTimeField(db_column="DATA_DODANIA")
    dzielnica = models.CharField(
        db_column="DZIELNICA", max_length=30, blank=True, null=True
    )
    osiedle = models.CharField(
        db_column="OSIEDLE", max_length=30, blank=True, null=True
    )
    pozycja_x = models.IntegerField(db_column="POZYCJA_X", blank=True, null=True)
    pozycja_x_2 = models.IntegerField(db_column="POZYCJA_X_2", blank=True, null=True)
    pozycja_y = models.IntegerField(db_column="POZYCJA_Y", blank=True, null=True)
    pozycja_y_2 = models.IntegerField(db_column="POZYCJA_Y_2", blank=True, null=True)
    termin_zakonczenia = models.DateTimeField(
        db_column="TERMIN_ZAKONCZENIA", blank=True, null=True
    )
    id_spolki = models.IntegerField(db_column="ID_SPOLKI", blank=True, null=True)
    id_opiekuna = models.IntegerField(db_column="ID_OPIEKUNA", blank=True, null=True)
    pokazuj_na_www = models.CharField(
        db_column="POKAZUJ_NA_WWW", max_length=10, blank=True, null=True
    )
    jest_sklep = models.CharField(
        db_column="JEST_SKLEP", max_length=1, blank=True, null=True
    )
    jest_apteka = models.CharField(
        db_column="JEST_APTEKA", max_length=1, blank=True, null=True
    )
    jest_plac_zabaw = models.CharField(
        db_column="JEST_PLAC_ZABAW", max_length=1, blank=True, null=True
    )
    jest_szkola = models.CharField(
        db_column="JEST_SZKOLA", max_length=1, blank=True, null=True
    )
    jest_przedszkole = models.CharField(
        db_column="JEST_PRZEDSZKOLE", max_length=1, blank=True, null=True
    )
    cena_dzialki = models.DecimalField(
        db_column="CENA_DZIALKI",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    strona_www = models.CharField(
        db_column="STRONA_WWW", max_length=200, blank=True, null=True
    )
    skrot = models.CharField(db_column="SKROT", max_length=20, blank=True, null=True)
    termin_rozpoczecia = models.DateTimeField(
        db_column="TERMIN_ROZPOCZECIA", blank=True, null=True
    )
    obciazenia = models.CharField(
        db_column="OBCIAZENIA", max_length=300, blank=True, null=True
    )
    przeznaczenie = models.CharField(
        db_column="PRZEZNACZENIE", max_length=300, blank=True, null=True
    )
    wysokosc_zabudowy = models.CharField(
        db_column="WYSOKOSC_ZABUDOWY", max_length=100, blank=True, null=True
    )
    procent_zabudowy = models.CharField(
        db_column="PROCENT_ZABUDOWY", max_length=100, blank=True, null=True
    )
    otoczenie = models.CharField(
        db_column="OTOCZENIE", max_length=300, blank=True, null=True
    )
    stan_prawny = models.CharField(
        db_column="STAN_PRAWNY", max_length=100, blank=True, null=True
    )
    ksiega_wieczysta = models.CharField(
        db_column="KSIEGA_WIECZYSTA", max_length=200, blank=True, null=True
    )
    nr_pozwolenia = models.CharField(
        db_column="NR_POZWOLENIA", max_length=200, blank=True, null=True
    )
    data_uzytkowania_wieczystego = models.DateTimeField(
        db_column="DATA_UZYTKOWANIA_WIECZYSTEGO", blank=True, null=True
    )
    powiat = models.CharField(db_column="POWIAT", max_length=30, blank=True, null=True)
    gmina = models.CharField(db_column="GMINA", max_length=30, blank=True, null=True)
    ulica_typ = models.CharField(
        db_column="ULICA_TYP", max_length=5, blank=True, null=True
    )
    id_prowadzacego_usterki = models.IntegerField(
        db_column="ID_PROWADZACEGO_USTERKI", blank=True, null=True
    )
    pozwolenie_na_uzytkowanie = models.DateTimeField(
        db_column="POZWOLENIE_NA_UZYTKOWANIE", blank=True, null=True
    )
    pow_calkowita = models.FloatField(db_column="POW_CALKOWITA", blank=True, null=True)
    id_ext = models.IntegerField(db_column="ID_EXT", blank=True, null=True)
    wersja_rekordu_wymiany = models.IntegerField(
        db_column="WERSJA_REKORDU_WYMIANY", blank=True, null=True
    )
    data_zmiany = models.DateTimeField(db_column="DATA_ZMIANY", blank=True, null=True)
    kto_zmienil = models.CharField(
        db_column="KTO_ZMIENIL", max_length=50, blank=True, null=True
    )
    nazwa_przedsiewziecia = models.CharField(
        db_column="NAZWA_PRZEDSIEWZIECIA", max_length=100, blank=True, null=True
    )
    pow_komunikacyjna_garazy = models.DecimalField(
        db_column="POW_KOMUNIKACYJNA_GARAZY",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    pow_wspolna = models.DecimalField(
        db_column="POW_WSPOLNA", max_digits=18, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TBL_INWESTYCJE"


class TblBudynki(models.Model):
    id_budynku = models.BigAutoField(db_column="ID_BUDYNKU", primary_key=True)
    inwestycja = models.ForeignKey(
        TblInwestycje, models.DO_NOTHING, db_column="ID_INWESTYCJI"
    )
    typ = models.CharField(db_column="TYP", max_length=1)
    nr_budowlany = models.CharField(
        db_column="NR_BUDOWLANY", max_length=200, blank=True, null=True
    )
    oznaczenie = models.CharField(
        db_column="OZNACZENIE", max_length=100, blank=True, null=True
    )
    klatek = models.SmallIntegerField(db_column="KLATEK", blank=True, null=True)
    kondygnacji_nad = models.SmallIntegerField(
        db_column="KONDYGNACJI_NAD", blank=True, null=True
    )
    kondygnacji_pod = models.SmallIntegerField(
        db_column="KONDYGNACJI_POD", blank=True, null=True
    )
    pow_uzytkowa = models.FloatField(db_column="POW_UZYTKOWA", blank=True, null=True)
    pow_komunikacyjna = models.FloatField(
        db_column="POW_KOMUNIKACYJNA", blank=True, null=True
    )
    pow_techniczna = models.FloatField(
        db_column="POW_TECHNICZNA", blank=True, null=True
    )
    pow_garazy = models.FloatField(db_column="POW_GARAZY", blank=True, null=True)
    pow_komorek = models.FloatField(db_column="POW_KOMOREK", blank=True, null=True)
    cena_gruntu = models.DecimalField(
        db_column="CENA_GRUNTU", max_digits=38, decimal_places=10, blank=True, null=True
    )
    cena_mieszkania = models.DecimalField(
        db_column="CENA_MIESZKANIA",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    cena_balkonu = models.DecimalField(
        db_column="CENA_BALKONU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    cena_tarasu = models.DecimalField(
        db_column="CENA_TARASU", max_digits=38, decimal_places=10, blank=True, null=True
    )
    cena_komorki = models.DecimalField(
        db_column="CENA_KOMORKI",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    cena_garazu = models.DecimalField(
        db_column="CENA_GARAZU", max_digits=38, decimal_places=10, blank=True, null=True
    )
    cena_parkingu = models.DecimalField(
        db_column="CENA_PARKINGU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    cena_lokalu = models.DecimalField(
        db_column="CENA_LOKALU", max_digits=38, decimal_places=10, blank=True, null=True
    )
    cena_innej = models.DecimalField(
        db_column="CENA_INNEJ", max_digits=38, decimal_places=10, blank=True, null=True
    )
    cena_domu = models.DecimalField(
        db_column="CENA_DOMU", max_digits=38, decimal_places=10, blank=True, null=True
    )
    ceny_od = models.DateTimeField(db_column="CENY_OD", blank=True, null=True)
    ceny_do = models.DateTimeField(db_column="CENY_DO", blank=True, null=True)
    sciezka = models.CharField(
        db_column="SCIEZKA", max_length=100, blank=True, null=True
    )
    wojewodztwo = models.CharField(
        db_column="WOJEWODZTWO", max_length=30, blank=True, null=True
    )
    powiat = models.CharField(db_column="POWIAT", max_length=30, blank=True, null=True)
    gmina = models.CharField(db_column="GMINA", max_length=30, blank=True, null=True)
    miasto = models.CharField(db_column="MIASTO", max_length=30, blank=True, null=True)
    ulica_typ = models.CharField(
        db_column="ULICA_TYP", max_length=5, blank=True, null=True
    )
    ulica = models.CharField(db_column="ULICA", max_length=50, blank=True, null=True)
    nr_domu = models.CharField(db_column="NR_DOMU", max_length=5, blank=True, null=True)
    kod = models.CharField(db_column="KOD", max_length=10, blank=True, null=True)
    poczta = models.CharField(db_column="POCZTA", max_length=30, blank=True, null=True)
    kto_dodal = models.CharField(db_column="KTO_DODAL", max_length=50)
    data_dodania = models.DateTimeField(db_column="DATA_DODANIA")
    termin_oddania = models.DateTimeField(
        db_column="TERMIN_ODDANIA", blank=True, null=True
    )
    opis = models.CharField(db_column="OPIS", max_length=5000, blank=True, null=True)
    ukrywaj_sprzedaz = models.CharField(
        db_column="UKRYWAJ_SPRZEDAZ", max_length=1, blank=True, null=True
    )
    nr_dzialki = models.CharField(
        db_column="NR_DZIALKI", max_length=300, blank=True, null=True
    )
    nr_pozwolenia = models.CharField(
        db_column="NR_POZWOLENIA", max_length=600, blank=True, null=True
    )
    data_pozwolenia = models.DateTimeField(
        db_column="DATA_POZWOLENIA", blank=True, null=True
    )
    dlugosc_okresu_rekojmi = models.IntegerField(
        db_column="DLUGOSC_OKRESU_REKOJMI", blank=True, null=True
    )
    dlugosc_okresu_gwarancji = models.IntegerField(
        db_column="DLUGOSC_OKRESU_GWARANCJI", blank=True, null=True
    )
    pokazuj_na_www = models.CharField(
        db_column="POKAZUJ_NA_WWW", max_length=10, blank=True, null=True
    )
    ceny_lokali_podawane_z_gruntem = models.CharField(
        db_column="CENY_LOKALI_PODAWANE_Z_GRUNTEM", max_length=1, blank=True, null=True
    )
    pow_dzialki = models.FloatField(db_column="POW_DZIALKI", blank=True, null=True)
    cena_dzialki = models.DecimalField(
        db_column="CENA_DZIALKI",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    ksiega_wieczysta = models.CharField(
        db_column="KSIEGA_WIECZYSTA", max_length=200, blank=True, null=True
    )
    strona_www = models.CharField(
        db_column="STRONA_WWW", max_length=200, blank=True, null=True
    )
    numer_fk = models.CharField(
        db_column="NUMER_FK", max_length=15, blank=True, null=True
    )
    # id_etapu = models.ForeignKey('TblEtapy', models.DO_NOTHING, db_column='ID_ETAPU', blank=True, null=True)
    pozwolenie_ostateczne = models.BooleanField(
        db_column="POZWOLENIE_OSTATECZNE", blank=True, null=True
    )
    pozwolenie_zaskarzone = models.BooleanField(
        db_column="POZWOLENIE_ZASKARZONE", blank=True, null=True
    )
    termin_rozpoczecia_budowy = models.DateTimeField(
        db_column="TERMIN_ROZPOCZECIA_BUDOWY", blank=True, null=True
    )
    sposob_pomiaru = models.CharField(
        db_column="SPOSOB_POMIARU", max_length=2000, blank=True, null=True
    )
    sposob_finansowania = models.CharField(
        db_column="SPOSOB_FINANSOWANIA", max_length=500, blank=True, null=True
    )
    srodki_ochrony_nabywcow = models.CharField(
        db_column="SRODKI_OCHRONY_NABYWCOW", max_length=500, blank=True, null=True
    )
    zasady_zabezpieczen = models.CharField(
        db_column="ZASADY_ZABEZPIECZEN", max_length=500, blank=True, null=True
    )
    instytucja_bezpieczenstwa = models.CharField(
        db_column="INSTYTUCJA_BEZPIECZENSTWA", max_length=200, blank=True, null=True
    )
    waloryzacja = models.CharField(
        db_column="WALORYZACJA", max_length=500, blank=True, null=True
    )
    technologia_wykonania = models.CharField(
        db_column="TECHNOLOGIA_WYKONANIA", max_length=2000, blank=True, null=True
    )
    standard_wykonczenia = models.CharField(
        db_column="STANDARD_WYKONCZENIA", max_length=300, blank=True, null=True
    )
    dostepne_media = models.CharField(
        db_column="DOSTEPNE_MEDIA", max_length=500, blank=True, null=True
    )
    droga_publiczna = models.CharField(
        db_column="DROGA_PUBLICZNA", max_length=300, blank=True, null=True
    )
    minimalny_odstep_budynkow = models.CharField(
        db_column="MINIMALNY_ODSTEP_BUDYNKOW", max_length=200, blank=True, null=True
    )
    termin_zakonczenia_budowy = models.DateTimeField(
        db_column="TERMIN_ZAKONCZENIA_BUDOWY", blank=True, null=True
    )
    version = models.TextField(db_column="Version")
    kolejnosc = models.IntegerField(db_column="KOLEJNOSC")
    id_wykonawcy = models.IntegerField(db_column="ID_WYKONAWCY", blank=True, null=True)
    ksiega_wieczysta_dzialki = models.CharField(
        db_column="KSIEGA_WIECZYSTA_DZIALKI", max_length=200, blank=True, null=True
    )
    hipoteka = models.CharField(
        db_column="HIPOTEKA", max_length=1000, blank=True, null=True
    )
    data_pozw_na_uzytkowanie = models.DateTimeField(
        db_column="DATA_POZW_NA_UZYTKOWANIE", blank=True, null=True
    )
    nr_pozw_na_uzytkowanie = models.CharField(
        db_column="NR_POZW_NA_UZYTKOWANIE", max_length=600, blank=True, null=True
    )
    nr_rachunku_do_umowy = models.CharField(
        db_column="NR_RACHUNKU_DO_UMOWY", max_length=100, blank=True, null=True
    )
    data_wprowadzenia_do_sprzedazy = models.DateTimeField(
        db_column="DATA_WPROWADZENIA_DO_SPRZEDAZY", blank=True, null=True
    )
    magazyn_fk = models.CharField(
        db_column="MAGAZYN_FK", max_length=100, blank=True, null=True
    )
    data_decyzji_kredytowej = models.DateTimeField(
        db_column="DATA_DECYZJI_KREDYTOWEJ", blank=True, null=True
    )
    termin_prac_dodatkowych = models.DateTimeField(
        db_column="TERMIN_PRAC_DODATKOWYCH", blank=True, null=True
    )
    oznaczenie_aktu_zakupu_dzialki = models.CharField(
        db_column="OZNACZENIE_AKTU_ZAKUPU_DZIALKI",
        max_length=200,
        blank=True,
        null=True,
    )
    data_rachunku_umowy = models.DateTimeField(
        db_column="DATA_RACHUNKU_UMOWY", blank=True, null=True
    )
    pow_calkowita = models.FloatField(db_column="POW_CALKOWITA", blank=True, null=True)
    kto_zmienil = models.CharField(
        db_column="KTO_ZMIENIL", max_length=50, blank=True, null=True
    )
    data_zmiany = models.DateTimeField(db_column="DATA_ZMIANY", blank=True, null=True)
    id_ext = models.BigIntegerField(db_column="ID_EXT", blank=True, null=True)
    wersja_rekordu_wymiany = models.IntegerField(
        db_column="WERSJA_REKORDU_WYMIANY", blank=True, null=True
    )
    pow_komunikacyjna_garazy = models.DecimalField(
        db_column="POW_KOMUNIKACYJNA_GARAZY",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    pow_wspolna = models.DecimalField(
        db_column="POW_WSPOLNA", max_digits=18, decimal_places=2, blank=True, null=True
    )
    data_rozpoczecia = models.DateTimeField(
        db_column="DATA_ROZPOCZECIA", blank=True, null=True
    )
    data_zakonczenia = models.DateTimeField(
        db_column="DATA_ZAKONCZENIA", blank=True, null=True
    )
    data_decyzji_odrolnienie = models.DateTimeField(
        db_column="DATA_DECYZJI_ODROLNIENIE", blank=True, null=True
    )
    kwota_oplaty_odrolnienie = models.DecimalField(
        db_column="KWOTA_OPLATY_ODROLNIENIE",
        max_digits=18,
        decimal_places=2,
        blank=True,
        null=True,
    )
    liczba_kondygnacji = models.IntegerField(
        db_column="LICZBA_KONDYGNACJI", blank=True, null=True
    )
    ilosc_miejsc_garazowych = models.IntegerField(
        db_column="ILOSC_MIEJSC_GARAZOWYCH", blank=True, null=True
    )
    ilosc_miejsc_postojowych = models.IntegerField(
        db_column="ILOSC_MIEJSC_POSTOJOWYCH", blank=True, null=True
    )
    wysokosc_udzialu = models.CharField(
        db_column="WYSOKOSC_UDZIALU", max_length=200, blank=True, null=True
    )
    nr_dzialki_udzialu = models.CharField(
        db_column="NR_DZIALKI_UDZIALU", max_length=200, blank=True, null=True
    )
    numer_kw_udzialu = models.CharField(
        db_column="NUMER_KW_UDZIALU", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TBL_BUDYNKI"


class TblDokumenty(models.Model):
    id_dokumentu = models.AutoField(db_column="ID_DOKUMENTU", primary_key=True)
    numer = models.IntegerField(db_column="NUMER")
    oznaczenie_dokumentu = models.CharField(
        db_column="OZNACZENIE_DOKUMENTU", max_length=100, blank=True, null=True
    )
    grupa_szablonow = models.CharField(
        db_column="GRUPA_SZABLONOW", max_length=50, blank=True, null=True
    )
    typ = models.CharField(db_column="TYP", max_length=130, blank=True, null=True)
    opis = models.CharField(db_column="OPIS", max_length=600, blank=True, null=True)
    data_podpisania = models.DateTimeField(
        db_column="DATA_PODPISANIA", blank=True, null=True
    )
    podpisal = models.CharField(
        db_column="PODPISAL", max_length=50, blank=True, null=True
    )
    sciezka = models.CharField(
        db_column="SCIEZKA", max_length=200, blank=True, null=True
    )
    status = models.CharField(db_column="STATUS", max_length=100, blank=True, null=True)
    osoba_odpowiedzialna = models.CharField(
        db_column="OSOBA_ODPOWIEDZIALNA", max_length=50, blank=True, null=True
    )
    wersja = models.IntegerField(db_column="WERSJA", blank=True, null=True)
    id_szablonu = models.IntegerField(db_column="ID_SZABLONU", blank=True, null=True)
    dostepny_online = models.BooleanField(
        db_column="DOSTEPNY_ONLINE", blank=True, null=True
    )
    id_workflow = models.BigIntegerField(db_column="ID_WORKFLOW", blank=True, null=True)
    data_anonimizacji = models.DateTimeField(
        db_column="DATA_ANONIMIZACJI", blank=True, null=True
    )
    data_dodania = models.DateTimeField(db_column="DATA_DODANIA", blank=True, null=True)
    id_pracownika = models.IntegerField(
        db_column="ID_PRACOWNIKA", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TBL_DOKUMENTY"


class TblGrupyVat(models.Model):
    id_grupy = models.IntegerField(db_column="ID_GRUPY", primary_key=True)
    id_typu_lokalu = models.IntegerField(db_column="ID_TYPU_LOKALU")
    opis = models.CharField(db_column="OPIS", max_length=50, blank=True, null=True)
    udzial = models.FloatField(db_column="UDZIAL", blank=True, null=True)
    opis_w_rozliczeniach = models.CharField(
        db_column="OPIS_W_ROZLICZENIACH", max_length=300, blank=True, null=True
    )
    pkwiu = models.CharField(db_column="PKWIU", max_length=20, blank=True, null=True)
    numer_fk = models.CharField(
        db_column="NUMER_FK", max_length=10, blank=True, null=True
    )
    opis_na_fakt_koncowych = models.CharField(
        db_column="OPIS_NA_FAKT_KONCOWYCH", max_length=300, blank=True, null=True
    )
    magazyn_fk = models.CharField(
        db_column="MAGAZYN_FK", max_length=100, blank=True, null=True
    )
    opis_koncowych_suma_zaliczek = models.CharField(
        db_column="OPIS_KONCOWYCH_SUMA_ZALICZEK", max_length=300, blank=True, null=True
    )
    opis_koncowych_roznica = models.CharField(
        db_column="OPIS_KONCOWYCH_ROZNICA", max_length=300, blank=True, null=True
    )
    nadwyzka_od = models.DecimalField(
        db_column="NADWYZKA_OD", max_digits=18, decimal_places=2, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TBL_GRUPY_VAT"


class TblTypyLokali(models.Model):
    id_typu = models.AutoField(db_column="ID_TYPU", primary_key=True)
    nazwa = models.CharField(db_column="NAZWA", max_length=50, blank=True, null=True)
    opis = models.CharField(db_column="OPIS", max_length=100, blank=True, null=True)
    budynek_dom = models.CharField(
        db_column="BUDYNEK_DOM", max_length=1, blank=True, null=True
    )
    czy_do_sprzedazy = models.CharField(
        db_column="CZY_DO_SPRZEDAZY", max_length=1, blank=True, null=True
    )
    czy_do_udzialow = models.CharField(
        db_column="CZY_DO_UDZIALOW", max_length=1, blank=True, null=True
    )
    czy_moze_przynalezec = models.CharField(
        db_column="CZY_MOZE_PRZYNALEZEC", max_length=1, blank=True, null=True
    )
    wstawiaj_do_pola = models.CharField(
        db_column="WSTAWIAJ_DO_POLA", max_length=30, blank=True, null=True
    )
    czy_na_sztuki = models.CharField(
        db_column="CZY_NA_SZTUKI", max_length=1, blank=True, null=True
    )
    nie_chron_uprawnieniami = models.CharField(
        db_column="NIE_CHRON_UPRAWNIENIAMI", max_length=1, blank=True, null=True
    )
    czy_podrzedny = models.CharField(
        db_column="CZY_PODRZEDNY", max_length=1, blank=True, null=True
    )
    czy_nadrzedny = models.CharField(
        db_column="CZY_NADRZEDNY", max_length=1, blank=True, null=True
    )
    nie_uwzgledniaj_wart_gruntu = models.CharField(
        db_column="NIE_UWZGLEDNIAJ_WART_GRUNTU", max_length=1, blank=True, null=True
    )
    skrot = models.CharField(db_column="SKROT", max_length=30, blank=True, null=True)
    czy_mieszkalny = models.BooleanField(db_column="CZY_MIESZKALNY")
    pozycja = models.IntegerField(db_column="POZYCJA", blank=True, null=True)
    kto_dodal = models.CharField(
        db_column="KTO_DODAL", max_length=50, blank=True, null=True
    )
    data_dodania = models.DateTimeField(db_column="DATA_DODANIA", blank=True, null=True)
    kto_zmienil = models.CharField(
        db_column="KTO_ZMIENIL", max_length=50, blank=True, null=True
    )
    data_zmiany = models.DateTimeField(db_column="DATA_ZMIANY", blank=True, null=True)
    id_ext = models.IntegerField(db_column="ID_EXT", blank=True, null=True)
    wersja_rekordu_wymiany = models.IntegerField(
        db_column="WERSJA_REKORDU_WYMIANY", blank=True, null=True
    )
    umozliwiaj_dodanie_r_powierniczego = models.BooleanField(
        db_column="UMOZLIWIAJ_DODANIE_R_POWIERNICZEGO"
    )
    sprzedawany_na_sztuki = models.BooleanField(
        db_column="SPRZEDAWANY_NA_SZTUKI", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TBL_TYPY_LOKALI"


class TblLokale(models.Model):
    id_lokalu = models.BigAutoField(db_column="ID_LOKALU", primary_key=True)
    typ_lokalu = models.ForeignKey(
        TblTypyLokali, models.DO_NOTHING, verbose_name="ID typu=", db_column="ID_TYPU"
    )
    budynek = models.ForeignKey(
        TblBudynki, models.DO_NOTHING, db_column="ID_BUDYNKU", blank=True, null=True
    )
    kondygnacja = models.CharField(
        db_column="KONDYGNACJA", max_length=10, blank=True, null=True
    )
    oznaczenie_klatki = models.CharField(
        db_column="OZNACZENIE_KLATKI", max_length=10, blank=True, null=True
    )
    oznaczenie_lokalu = models.CharField(
        db_column="OZNACZENIE_LOKALU", max_length=10, blank=True, null=True
    )
    oznaczenie = models.CharField(
        db_column="OZNACZENIE", max_length=40, blank=True, null=True
    )
    pelne_oznaczenie = models.CharField(
        db_column="PELNE_OZNACZENIE", max_length=100, blank=True, null=True
    )
    klatka = models.CharField(db_column="KLATKA", max_length=20, blank=True, null=True)
    numer = models.CharField(db_column="NUMER", max_length=20, blank=True, null=True)
    pomieszczen = models.SmallIntegerField(
        db_column="POMIESZCZEN", blank=True, null=True
    )
    opis = models.CharField(db_column="OPIS", max_length=1500, blank=True, null=True)
    ukryj_lokal = models.CharField(db_column="UKRYJ_LOKAL", max_length=1)
    status = models.IntegerField(db_column="STATUS")
    pow_umowna_gruntu = models.FloatField(
        db_column="POW_UMOWNA_GRUNTU", blank=True, null=True
    )
    pow_umowna_lokalu = models.FloatField(
        db_column="POW_UMOWNA_LOKALU", blank=True, null=True
    )
    pow_umowna_balkonu = models.FloatField(
        db_column="POW_UMOWNA_BALKONU", blank=True, null=True
    )
    pow_umowna_tarasu = models.FloatField(
        db_column="POW_UMOWNA_TARASU", blank=True, null=True
    )
    pow_umowna_inna = models.FloatField(
        db_column="POW_UMOWNA_INNA", blank=True, null=True
    )
    pow_koncowa_gruntu = models.FloatField(
        db_column="POW_KONCOWA_GRUNTU", blank=True, null=True
    )
    pow_koncowa_lokalu = models.FloatField(
        db_column="POW_KONCOWA_LOKALU", blank=True, null=True
    )
    pow_koncowa_balkonu = models.FloatField(
        db_column="POW_KONCOWA_BALKONU", blank=True, null=True
    )
    pow_koncowa_tarasu = models.FloatField(
        db_column="POW_KONCOWA_TARASU", blank=True, null=True
    )
    pow_koncowa_inna = models.FloatField(
        db_column="POW_KONCOWA_INNA", blank=True, null=True
    )
    cena_gruntu = models.DecimalField(
        db_column="CENA_GRUNTU", max_digits=38, decimal_places=10, blank=True, null=True
    )
    cena_lokalu = models.DecimalField(
        db_column="CENA_LOKALU", max_digits=38, decimal_places=10, blank=True, null=True
    )
    cena_balkonu = models.DecimalField(
        db_column="CENA_BALKONU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    cena_tarasu = models.DecimalField(
        db_column="CENA_TARASU", max_digits=38, decimal_places=10, blank=True, null=True
    )
    cena_innej = models.DecimalField(
        db_column="CENA_INNEJ", max_digits=38, decimal_places=10, blank=True, null=True
    )
    id_lokalu_przynaleznego = models.IntegerField(
        db_column="ID_LOKALU_PRZYNALEZNEGO", blank=True, null=True
    )
    wykonczenie = models.CharField(
        db_column="WYKONCZENIE", max_length=50, blank=True, null=True
    )
    id_grupy_vat = models.ForeignKey(
        TblGrupyVat, models.DO_NOTHING, db_column="ID_GRUPY_VAT", blank=True, null=True
    )
    kwota_rabatu = models.DecimalField(
        db_column="KWOTA_RABATU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    rabat = models.FloatField(db_column="RABAT", blank=True, null=True)
    korekta = models.DecimalField(
        db_column="KOREKTA", max_digits=38, decimal_places=10, blank=True, null=True
    )
    wartosc_umowna_lokalu = models.DecimalField(
        db_column="WARTOSC_UMOWNA_LOKALU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    wartosc_koncowa_lokalu = models.DecimalField(
        db_column="WARTOSC_KONCOWA_LOKALU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    kwota_indeksacji = models.DecimalField(
        db_column="KWOTA_INDEKSACJI",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    wartosc_umowna_gruntu = models.DecimalField(
        db_column="WARTOSC_UMOWNA_GRUNTU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    wartosc_koncowa_gruntu = models.DecimalField(
        db_column="WARTOSC_KONCOWA_GRUNTU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    wartosc_umowna_razem = models.DecimalField(
        db_column="WARTOSC_UMOWNA_RAZEM",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    wartosc_koncowa_razem = models.DecimalField(
        db_column="WARTOSC_KONCOWA_RAZEM",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    stale_udzialy = models.CharField(
        db_column="STALE_UDZIALY", max_length=1, blank=True, null=True
    )
    udzial_w_budynku = models.FloatField(
        db_column="UDZIAL_W_BUDYNKU", blank=True, null=True
    )
    udzial_w_pow_lokali = models.FloatField(
        db_column="UDZIAL_W_POW_LOKALI", blank=True, null=True
    )
    udzial_cz_wspolnej = models.FloatField(
        db_column="UDZIAL_CZ_WSPOLNEJ", blank=True, null=True
    )
    data_przekazania = models.DateTimeField(
        db_column="DATA_PRZEKAZANIA", blank=True, null=True
    )
    data_aktu = models.DateTimeField(db_column="DATA_AKTU", blank=True, null=True)
    data_rezerwacji = models.DateTimeField(
        db_column="DATA_REZERWACJI", blank=True, null=True
    )
    kto_dodal = models.CharField(db_column="KTO_DODAL", max_length=50)
    data_dodania = models.DateTimeField(db_column="DATA_DODANIA")
    sort_klatka = models.IntegerField(db_column="SORT_KLATKA", blank=True, null=True)
    sort_kondygnacja = models.IntegerField(
        db_column="SORT_KONDYGNACJA", blank=True, null=True
    )
    sort_lokal = models.IntegerField(db_column="SORT_LOKAL", blank=True, null=True)
    plik_z_rzutem = models.CharField(
        db_column="PLIK_Z_RZUTEM", max_length=200, blank=True, null=True
    )
    plik_z_metryczka = models.CharField(
        db_column="PLIK_Z_METRYCZKA", max_length=200, blank=True, null=True
    )
    upust = models.FloatField(db_column="UPUST", blank=True, null=True)
    rata_kredytu = models.DecimalField(
        db_column="RATA_KREDYTU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    przed_upustem_netto = models.DecimalField(
        db_column="PRZED_UPUSTEM_NETTO",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    przed_upustem_brutto = models.DecimalField(
        db_column="PRZED_UPUSTEM_BRUTTO",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    ulica = models.CharField(db_column="ULICA", max_length=50, blank=True, null=True)
    kierunki_swiata = models.CharField(
        db_column="KIERUNKI_SWIATA", max_length=200, blank=True, null=True
    )
    pietro = models.CharField(db_column="PIETRO", max_length=5, blank=True, null=True)
    zablokowany = models.CharField(
        db_column="ZABLOKOWANY", max_length=1, blank=True, null=True
    )
    godzina_przekazania = models.CharField(
        db_column="GODZINA_PRZEKAZANIA", max_length=10, blank=True, null=True
    )
    jest_aneks = models.CharField(
        db_column="JEST_ANEKS", max_length=1, blank=True, null=True
    )
    jest_wc = models.CharField(db_column="JEST_WC", max_length=1, blank=True, null=True)
    jest_ogrod = models.CharField(
        db_column="JEST_OGROD", max_length=1, blank=True, null=True
    )
    jest_garaz = models.CharField(
        db_column="JEST_GARAZ", max_length=1, blank=True, null=True
    )
    id_lokalu_nadrzednego = models.IntegerField(
        db_column="ID_LOKALU_NADRZEDNEGO", blank=True, null=True
    )
    id_grupa_cenowa = models.IntegerField(
        db_column="ID_GRUPA_CENOWA", blank=True, null=True
    )
    numer_aktu = models.CharField(
        db_column="NUMER_AKTU", max_length=50, blank=True, null=True
    )
    oznaczenie_administracyjne = models.CharField(
        db_column="OZNACZENIE_ADMINISTRACYJNE", max_length=40, blank=True, null=True
    )
    pow_umowna_balkonu_2 = models.FloatField(
        db_column="POW_UMOWNA_BALKONU_2", blank=True, null=True
    )
    pow_umowna_loggia = models.FloatField(
        db_column="POW_UMOWNA_LOGGIA", blank=True, null=True
    )
    pow_umowna_ogrodka = models.FloatField(
        db_column="POW_UMOWNA_OGRODKA", blank=True, null=True
    )
    pow_koncowa_balkonu_2 = models.FloatField(
        db_column="POW_KONCOWA_BALKONU_2", blank=True, null=True
    )
    pow_koncowa_loggia = models.FloatField(
        db_column="POW_KONCOWA_LOGGIA", blank=True, null=True
    )
    pow_koncowa_ogrodka = models.FloatField(
        db_column="POW_KONCOWA_OGRODKA", blank=True, null=True
    )
    cena_balkonu_2 = models.DecimalField(
        db_column="CENA_BALKONU_2",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    cena_loggia = models.DecimalField(
        db_column="CENA_LOGGIA", max_digits=38, decimal_places=10, blank=True, null=True
    )
    cena_ogrodka = models.DecimalField(
        db_column="CENA_OGRODKA",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    jest_garderoba = models.CharField(
        db_column="JEST_GARDEROBA", max_length=1, blank=True, null=True
    )
    powierzchnia_uzytkowa_umowna = models.FloatField(
        db_column="POWIERZCHNIA_UZYTKOWA_UMOWNA", blank=True, null=True
    )
    powierzchnia_uzytkowa_koncowa = models.FloatField(
        db_column="POWIERZCHNIA_UZYTKOWA_KONCOWA", blank=True, null=True
    )
    cena_minimalna = models.DecimalField(
        db_column="CENA_MINIMALNA",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    id_promocji = models.IntegerField(db_column="ID_PROMOCJI", blank=True, null=True)
    pow_umowna_nadwyzki_lokalu = models.FloatField(
        db_column="POW_UMOWNA_NADWYZKI_LOKALU", blank=True, null=True
    )
    pow_koncowa_nadwyzki_lokalu = models.FloatField(
        db_column="POW_KONCOWA_NADWYZKI_LOKALU", blank=True, null=True
    )
    wartosc_umowna_nadwyzki_lokalu = models.DecimalField(
        db_column="WARTOSC_UMOWNA_NADWYZKI_LOKALU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    wartosc_koncowa_nadwyzki_lokalu = models.DecimalField(
        db_column="WARTOSC_KONCOWA_NADWYZKI_LOKALU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    planowana_data_przekazania = models.DateTimeField(
        db_column="PLANOWANA_DATA_PRZEKAZANIA", blank=True, null=True
    )
    udzial_cz_wspolnej_ulamek = models.CharField(
        db_column="UDZIAL_CZ_WSPOLNEJ_ULAMEK", max_length=50, blank=True, null=True
    )
    id_konta = models.IntegerField(db_column="ID_KONTA", blank=True, null=True)
    widok = models.CharField(db_column="WIDOK", max_length=1000, blank=True, null=True)
    planowana_data_sprzedazy = models.DateTimeField(
        db_column="PLANOWANA_DATA_SPRZEDAZY", blank=True, null=True
    )
    version = models.TextField(db_column="Version")
    kwartal_rozp_sprzedazy = models.CharField(
        db_column="KWARTAL_ROZP_SPRZEDAZY", max_length=3, blank=True, null=True
    )
    rok_rozp_sprzedazy = models.CharField(
        db_column="ROK_ROZP_SPRZEDAZY", max_length=4, blank=True, null=True
    )
    kto_zmienil = models.IntegerField(db_column="KTO_ZMIENIL", blank=True, null=True)
    data_zmiany = models.DateTimeField(db_column="DATA_ZMIANY", blank=True, null=True)
    data_odbioru_technicznego = models.DateTimeField(
        db_column="DATA_ODBIORU_TECHNICZNEGO", blank=True, null=True
    )
    godzina_odbioru_technicznego = models.CharField(
        db_column="GODZINA_ODBIORU_TECHNICZNEGO", max_length=10, blank=True, null=True
    )
    czy_wykonczenie = models.BooleanField(
        db_column="CZY_WYKONCZENIE", blank=True, null=True
    )
    rozkladowe = models.BooleanField(db_column="ROZKLADOWE", blank=True, null=True)
    data_przekazania_przez_wykonawce = models.DateTimeField(
        db_column="DATA_PRZEKAZANIA_PRZEZ_WYKONAWCE", blank=True, null=True
    )
    numer_fk = models.CharField(
        db_column="NUMER_FK", max_length=50, blank=True, null=True
    )
    stopa_zwrotu = models.DecimalField(
        db_column="STOPA_ZWROTU", max_digits=5, decimal_places=2, blank=True, null=True
    )
    numer_projektowy = models.CharField(
        db_column="NUMER_PROJEKTOWY", max_length=100, blank=True, null=True
    )
    atrakcyjnosc = models.CharField(
        db_column="ATRAKCYJNOSC", max_length=200, blank=True, null=True
    )
    status_odbioru = models.CharField(
        db_column="STATUS_ODBIORU", max_length=200, blank=True, null=True
    )
    niepelne_dane = models.BooleanField(
        db_column="NIEPELNE_DANE", blank=True, null=True
    )
    status_budowlany = models.CharField(
        db_column="STATUS_BUDOWLANY", max_length=200, blank=True, null=True
    )
    data_zmiany_prospekt = models.DateTimeField(db_column="DATA_ZMIANY_PROSPEKT")
    cena_lokalu_na_umowie = models.DecimalField(
        db_column="CENA_LOKALU_NA_UMOWIE",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    id_ext = models.BigIntegerField(db_column="ID_EXT", blank=True, null=True)
    wersja_rekordu_wymiany = models.IntegerField(
        db_column="WERSJA_REKORDU_WYMIANY", blank=True, null=True
    )
    ostateczna_data_zmian = models.DateTimeField(
        db_column="OSTATECZNA_DATA_ZMIAN", blank=True, null=True
    )
    koncowa_rowna_umownej = models.BooleanField(db_column="KONCOWA_ROWNA_UMOWNEJ")
    moze_przynalezec = models.CharField(
        db_column="MOZE_PRZYNALEZEC", max_length=1, blank=True, null=True
    )
    wartosc_wykonczenia = models.CharField(
        db_column="WARTOSC_WYKONCZENIA", max_length=500, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TBL_LOKALE"


class TblPodmioty(models.Model):
    id_podmiotu = models.BigAutoField(db_column="ID_PODMIOTU", primary_key=True)
    typ = models.CharField(db_column="TYP", max_length=1)
    imie = models.CharField(db_column="IMIE", max_length=50, blank=True, null=True)
    imie_2 = models.CharField(db_column="IMIE_2", max_length=50, blank=True, null=True)
    nazwisko = models.CharField(
        db_column="NAZWISKO", max_length=100, blank=True, null=True
    )
    nazwisko_rodowe = models.CharField(
        db_column="NAZWISKO_RODOWE", max_length=30, blank=True, null=True
    )
    plec = models.CharField(db_column="PLEC", max_length=1, blank=True, null=True)
    osoba_prowadzaca = models.CharField(
        db_column="OSOBA_PROWADZACA", max_length=50, blank=True, null=True
    )
    firma = models.CharField(db_column="FIRMA", max_length=200, blank=True, null=True)
    nip = models.CharField(db_column="NIP", max_length=13, blank=True, null=True)
    regon = models.CharField(db_column="REGON", max_length=10, blank=True, null=True)
    numer_krs = models.CharField(
        db_column="NUMER_KRS", max_length=20, blank=True, null=True
    )
    imie_ojca = models.CharField(
        db_column="IMIE_OJCA", max_length=30, blank=True, null=True
    )
    imie_matki = models.CharField(
        db_column="IMIE_MATKI", max_length=30, blank=True, null=True
    )
    rodzaj = models.CharField(
        db_column="RODZAJ_DOKUMENTU", max_length=25, blank=True, null=True
    )
    nr_dokumentu = models.CharField(
        db_column="NR_DOKUMENTU", max_length=30, blank=True, null=True
    )
    pesel = models.CharField(db_column="PESEL", max_length=11, blank=True, null=True)
    imie_miej = models.CharField(
        db_column="IMIE_MIEJ", max_length=20, blank=True, null=True
    )
    imie_2_miej = models.CharField(
        db_column="IMIE_2_MIEJ", max_length=20, blank=True, null=True
    )
    nazwisko_miej = models.CharField(
        db_column="NAZWISKO_MIEJ", max_length=30, blank=True, null=True
    )
    telefon = models.CharField(
        db_column="TELEFON", max_length=50, blank=True, null=True
    )
    telefon_2 = models.CharField(
        db_column="TELEFON_2", max_length=50, blank=True, null=True
    )
    e_mail = models.CharField(db_column="E_MAIL", max_length=100, blank=True, null=True)
    opis = models.CharField(db_column="OPIS", max_length=2500, blank=True, null=True)
    kraj = models.CharField(db_column="KRAJ", max_length=30, blank=True, null=True)
    wojewodztwo = models.CharField(
        db_column="WOJEWODZTWO", max_length=30, blank=True, null=True
    )
    powiat = models.CharField(db_column="POWIAT", max_length=30, blank=True, null=True)
    gmina = models.CharField(db_column="GMINA", max_length=30, blank=True, null=True)
    miasto = models.CharField(db_column="MIASTO", max_length=40, blank=True, null=True)
    ulica_typ = models.CharField(
        db_column="ULICA_TYP", max_length=5, blank=True, null=True
    )
    ulica = models.CharField(db_column="ULICA", max_length=200, blank=True, null=True)
    nr_domu = models.CharField(
        db_column="NR_DOMU", max_length=15, blank=True, null=True
    )
    nr_lokalu = models.CharField(
        db_column="NR_LOKALU", max_length=10, blank=True, null=True
    )
    kod = models.CharField(db_column="KOD", max_length=10, blank=True, null=True)
    poczta = models.CharField(db_column="POCZTA", max_length=30, blank=True, null=True)
    nazwa_adresata = models.CharField(
        db_column="NAZWA_ADRESATA", max_length=200, blank=True, null=True
    )
    kraj_2 = models.CharField(db_column="KRAJ_2", max_length=30, blank=True, null=True)
    wojewodztwo_2 = models.CharField(
        db_column="WOJEWODZTWO_2", max_length=30, blank=True, null=True
    )
    powiat_2 = models.CharField(
        db_column="POWIAT_2", max_length=30, blank=True, null=True
    )
    gmina_2 = models.CharField(
        db_column="GMINA_2", max_length=30, blank=True, null=True
    )
    miasto_2 = models.CharField(
        db_column="MIASTO_2", max_length=40, blank=True, null=True
    )
    ulica_typ_2 = models.CharField(
        db_column="ULICA_TYP_2", max_length=5, blank=True, null=True
    )
    ulica_2 = models.CharField(
        db_column="ULICA_2", max_length=200, blank=True, null=True
    )
    nr_domu_2 = models.CharField(
        db_column="NR_DOMU_2", max_length=15, blank=True, null=True
    )
    nr_lokalu_2 = models.CharField(
        db_column="NR_LOKALU_2", max_length=10, blank=True, null=True
    )
    kod_2 = models.CharField(db_column="KOD_2", max_length=10, blank=True, null=True)
    poczta_2 = models.CharField(
        db_column="POCZTA_2", max_length=30, blank=True, null=True
    )
    status_majatkowy = models.CharField(
        db_column="STATUS_MAJATKOWY", max_length=100, blank=True, null=True
    )
    data_waznosci = models.CharField(
        db_column="DATA_WAZNOSCI", max_length=10, blank=True, null=True
    )
    nie_wysylaj = models.CharField(
        db_column="NIE_WYSYLAJ", max_length=1, blank=True, null=True
    )
    kto_dodal = models.CharField(
        db_column="KTO_DODAL", max_length=50, blank=True, null=True
    )
    data_dodania = models.DateTimeField(db_column="DATA_DODANIA", blank=True, null=True)
    zgoda_na_przetwarzanie_1 = models.CharField(
        db_column="ZGODA_NA_PRZETWARZANIE_1", max_length=1, blank=True, null=True
    )
    zgoda_na_przetwarzanie_2 = models.CharField(
        db_column="ZGODA_NA_PRZETWARZANIE_2", max_length=1, blank=True, null=True
    )
    data_zmiany = models.DateTimeField(db_column="DATA_ZMIANY", blank=True, null=True)
    kto_zmienil = models.CharField(
        db_column="KTO_ZMIENIL", max_length=50, blank=True, null=True
    )
    login = models.CharField(db_column="LOGIN", max_length=50, blank=True, null=True)
    haslo = models.CharField(db_column="HASLO", max_length=50, blank=True, null=True)
    stan_cywilny = models.CharField(
        db_column="STAN_CYWILNY", max_length=50, blank=True, null=True
    )
    wydany_przez = models.CharField(
        db_column="WYDANY_PRZEZ", max_length=100, blank=True, null=True
    )
    outlook_id = models.CharField(
        db_column="OUTLOOK_ID", max_length=200, blank=True, null=True
    )
    id_urzad_skarbowy = models.IntegerField(
        db_column="ID_URZAD_SKARBOWY", blank=True, null=True
    )
    czy_rezydent = models.CharField(
        db_column="CZY_REZYDENT", max_length=1, blank=True, null=True
    )
    czy_powiazany = models.CharField(
        db_column="CZY_POWIAZANY", max_length=1, blank=True, null=True
    )
    czy_przypominac_urodziny = models.CharField(
        db_column="CZY_PRZYPOMINAC_URODZINY", max_length=1, blank=True, null=True
    )
    id_posrednika = models.IntegerField(
        db_column="ID_POSREDNIKA", blank=True, null=True
    )
    mozliwosci_finansowe = models.CharField(
        db_column="MOZLIWOSCI_FINANSOWE", max_length=200, blank=True, null=True
    )
    zrodlo_finansowania = models.CharField(
        db_column="ZRODLO_FINANSOWANIA", max_length=200, blank=True, null=True
    )
    status_kontaktow = models.CharField(
        db_column="STATUS_KONTAKTOW", max_length=200, blank=True, null=True
    )
    status_handlowy = models.IntegerField(
        db_column="STATUS_HANDLOWY", blank=True, null=True
    )
    status_ksiegowy = models.IntegerField(
        db_column="STATUS_KSIEGOWY", blank=True, null=True
    )
    status_budowlany = models.IntegerField(
        db_column="STATUS_BUDOWLANY", blank=True, null=True
    )
    id_ext = models.IntegerField(db_column="ID_EXT", blank=True, null=True)
    akronim = models.CharField(
        db_column="AKRONIM", max_length=100, blank=True, null=True
    )
    wersja_rekordu_wymiany = models.IntegerField(
        db_column="WERSJA_REKORDU_WYMIANY", blank=True, null=True
    )
    version = models.TextField(db_column="Version")
    zgoda_na_e_faktury = models.CharField(
        db_column="ZGODA_NA_E_FAKTURY", max_length=1, blank=True, null=True
    )
    cel_zakupu = models.IntegerField(db_column="CEL_ZAKUPU", blank=True, null=True)
    zrodlo_informacji = models.IntegerField(
        db_column="ZRODLO_INFORMACJI", blank=True, null=True
    )
    status = models.CharField(db_column="STATUS", max_length=50, blank=True, null=True)
    id_inwestycji = models.IntegerField(
        db_column="ID_INWESTYCJI", blank=True, null=True
    )
    zrodlo_pozyskania = models.IntegerField(
        db_column="ZRODLO_POZYSKANIA", blank=True, null=True
    )
    potencjalny = models.BooleanField(db_column="POTENCJALNY", blank=True, null=True)
    urzad_skarbowy = models.IntegerField(
        db_column="URZAD_SKARBOWY", blank=True, null=True
    )
    zawod = models.IntegerField(db_column="ZAWOD", blank=True, null=True)
    platnik_vat = models.BooleanField(db_column="PLATNIK_VAT", blank=True, null=True)
    youlead_id = models.TextField(db_column="YOULEAD_ID", blank=True, null=True)
    obywatelstwo = models.CharField(
        db_column="OBYWATELSTWO", max_length=100, blank=True, null=True
    )
    planowana_data_anonimizacji = models.DateTimeField(
        db_column="PLANOWANA_DATA_ANONIMIZACJI", blank=True, null=True
    )
    data_anonimizacji = models.DateTimeField(
        db_column="DATA_ANONIMIZACJI", blank=True, null=True
    )
    zgoda_na_kontakt_forma_elektroniczna = models.CharField(
        db_column="ZGODA_NA_KONTAKT_FORMA_ELEKTRONICZNA",
        max_length=1,
        blank=True,
        null=True,
    )
    nr_konta = models.CharField(
        db_column="NR_KONTA", max_length=200, blank=True, null=True
    )
    nazwa_banku_klienta = models.CharField(
        db_column="NAZWA_BANKU_KLIENTA", max_length=500, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TBL_PODMIOTY"


class TblStatusyUmowy(models.Model):
    id_statusu = models.IntegerField(db_column="ID_STATUSU", primary_key=True)
    nazwa = models.CharField(
        db_column="NAZWA", unique=True, max_length=20, blank=True, null=True
    )
    skrot = models.CharField(db_column="SKROT", max_length=5, blank=True, null=True)
    ukryj = models.CharField(db_column="UKRYJ", max_length=1, blank=True, null=True)
    user_available = models.CharField(
        db_column="USER_AVAILABLE", max_length=1, blank=True, null=True
    )
    podpisana = models.CharField(
        db_column="PODPISANA", max_length=1, blank=True, null=True
    )
    zakonczona = models.CharField(
        db_column="ZAKONCZONA", max_length=1, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TBL_STATUSY_UMOWY"


class TblTypyUmow(models.Model):
    id_typu = models.AutoField(db_column="ID_TYPU", primary_key=True)
    nazwa = models.CharField(db_column="NAZWA", max_length=30, blank=True, null=True)
    opis = models.CharField(db_column="OPIS", max_length=100, blank=True, null=True)
    aktywny = models.CharField(db_column="AKTYWNY", max_length=1)
    skrot = models.CharField(db_column="SKROT", max_length=5, blank=True, null=True)
    rozliczenia = models.CharField(
        db_column="ROZLICZENIA", max_length=1, blank=True, null=True
    )
    widocznosc_obszarow = models.IntegerField(
        db_column="WIDOCZNOSC_OBSZAROW", blank=True, null=True
    )
    widocznosc_pol = models.IntegerField(
        db_column="WIDOCZNOSC_POL", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TBL_TYPY_UMOW"

    def __str__(self):
        return self.nazwa


class TblRodzajeUmow(models.Model):
    id_rodzaju_umowy = models.AutoField(db_column="ID_RODZAJU_UMOWY", primary_key=True)
    typ = models.ForeignKey(TblTypyUmow, models.DO_NOTHING, db_column="ID_TYPU")
    nazwa = models.CharField(db_column="NAZWA", max_length=50, blank=True, null=True)
    opis = models.CharField(db_column="OPIS", max_length=100, blank=True, null=True)
    skrot = models.CharField(db_column="SKROT", max_length=5, blank=True, null=True)
    zawiadomienia = models.BooleanField(db_column="ZAWIADOMIENIA")
    wymagane_pola = models.IntegerField(db_column="WYMAGANE_POLA")
    zmianiaj_status_na_zakonczona = models.BooleanField(
        db_column="ZMIANIAJ_STATUS_NA_ZAKONCZONA"
    )
    domyslny_termin_rezerwacji = models.IntegerField(
        db_column="DOMYSLNY_TERMIN_REZERWACJI", blank=True, null=True
    )
    fakturowanie_zawiadomien = models.BooleanField(db_column="FAKTUROWANIE_ZAWIADOMIEN")
    rejestracja_wplaty = models.BooleanField(db_column="REJESTRACJA_WPLATY")
    podstawa_faktury = models.CharField(
        db_column="PODSTAWA_FAKTURY", max_length=500, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TBL_RODZAJE_UMOW"


class TblUmowy(models.Model):
    id_umowy = models.AutoField(db_column="ID_UMOWY", primary_key=True)
    typ = models.ForeignKey(
        TblTypyUmow, models.DO_NOTHING, db_column="ID_TYPU", blank=True, null=True
    )
    numer = models.IntegerField(db_column="NUMER", blank=True, null=True)
    rok = models.SmallIntegerField(db_column="ROK", blank=True, null=True)
    symbol = models.CharField(db_column="SYMBOL", max_length=30, blank=True, null=True)
    oznaczenie = models.CharField(
        db_column="OZNACZENIE", max_length=50, blank=True, null=True
    )
    oznaczenie_umowy_administracyjnej = models.CharField(
        db_column="OZNACZENIE_UMOWY_ADMINISTRACYJNEJ",
        max_length=50,
        blank=True,
        null=True,
    )
    data_zawarcia = models.DateTimeField(
        db_column="DATA_ZAWARCIA", blank=True, null=True
    )
    miejsce_zawarcia = models.CharField(
        db_column="MIEJSCE_ZAWARCIA", max_length=30, blank=True, null=True
    )
    status = models.CharField(db_column="STATUS", max_length=20, blank=True, null=True)
    kredyt = models.DecimalField(
        db_column="KREDYT", max_digits=38, decimal_places=10, blank=True, null=True
    )
    kredytujacy_bank = models.CharField(
        db_column="KREDYTUJACY_BANK", max_length=50, blank=True, null=True
    )
    wart_umowna_gruntu = models.DecimalField(
        db_column="WART_UMOWNA_GRUNTU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    wart_koncowa_gruntu = models.DecimalField(
        db_column="WART_KONCOWA_GRUNTU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    wartosc_umowna = models.DecimalField(
        db_column="WARTOSC_UMOWNA",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    wartosc_koncowa = models.DecimalField(
        db_column="WARTOSC_KONCOWA",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    wartosc_umowna_brutto = models.DecimalField(
        db_column="WARTOSC_UMOWNA_BRUTTO",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    wartosc_koncowa_brutto = models.DecimalField(
        db_column="WARTOSC_KONCOWA_BRUTTO",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    kwota_zaplacona = models.DecimalField(
        db_column="KWOTA_ZAPLACONA",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    kwota_wyplacona = models.DecimalField(
        db_column="KWOTA_WYPLACONA",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    kwota_do_zaplaty = models.DecimalField(
        db_column="KWOTA_DO_ZAPLATY",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    kwota_indeksacji = models.DecimalField(
        db_column="KWOTA_INDEKSACJI",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    kwota_odsetek = models.DecimalField(
        db_column="KWOTA_ODSETEK",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    nadplata = models.DecimalField(
        db_column="NADPLATA", max_digits=38, decimal_places=10, blank=True, null=True
    )
    saldo_na_dzien = models.DateTimeField(
        db_column="SALDO_NA_DZIEN", blank=True, null=True
    )
    odsetek_do_zaplaty = models.DecimalField(
        db_column="ODSETEK_DO_ZAPLATY",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    kwota_do_zwrotu = models.DecimalField(
        db_column="KWOTA_DO_ZWROTU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    indeksacja_od = models.DateTimeField(
        db_column="INDEKSACJA_OD", blank=True, null=True
    )
    kara_umowna = models.FloatField(db_column="KARA_UMOWNA", blank=True, null=True)
    liczba_rat = models.SmallIntegerField(db_column="LICZBA_RAT", blank=True, null=True)
    termin_przekazania = models.CharField(
        db_column="TERMIN_PRZEKAZANIA", max_length=30, blank=True, null=True
    )
    termin_wybudowania = models.CharField(
        db_column="TERMIN_WYBUDOWANIA", max_length=30, blank=True, null=True
    )
    przekazanie = models.CharField(
        db_column="PRZEKAZANIE", max_length=1, blank=True, null=True
    )
    podpisal = models.CharField(
        db_column="PODPISAL", max_length=50, blank=True, null=True
    )
    osoba_odpowiedzialna = models.CharField(
        db_column="OSOBA_ODPOWIEDZIALNA", max_length=50, blank=True, null=True
    )
    pelnomocnictwo_od = models.DateTimeField(
        db_column="PELNOMOCNICTWO_OD", blank=True, null=True
    )
    stanowisko = models.CharField(
        db_column="STANOWISKO", max_length=100, blank=True, null=True
    )
    rozlicz_roznice_pow_powyzej = models.FloatField(
        db_column="ROZLICZ_ROZNICE_POW_POWYZEJ"
    )
    zmiany_w_umowie = models.CharField(
        db_column="ZMIANY_W_UMOWIE", max_length=600, blank=True, null=True
    )
    nazwiska_klientow = models.CharField(
        db_column="NAZWISKA_KLIENTOW", max_length=500, blank=True, null=True
    )
    poprzednie_nadplata = models.DecimalField(
        db_column="POPRZEDNIE_NADPLATA",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    poprzednie_kwota_do_zwrotu = models.DecimalField(
        db_column="POPRZEDNIE_KWOTA_DO_ZWROTU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    poprzednie_kwota_zaplacona = models.DecimalField(
        db_column="POPRZEDNIE_KWOTA_ZAPLACONA",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    poprzednie_kwota_wyplacona = models.DecimalField(
        db_column="POPRZEDNIE_KWOTA_WYPLACONA",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    poprzednie_kwota_indeksacji = models.DecimalField(
        db_column="POPRZEDNIE_KWOTA_INDEKSACJI",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    poprzednie_kwota_odsetek = models.DecimalField(
        db_column="POPRZEDNIE_KWOTA_ODSETEK",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    poprzednie_odsetek_do_zaplaty = models.DecimalField(
        db_column="POPRZEDNIE_ODSETEK_DO_ZAPLATY",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    poprzednie_saldo_na_dzien = models.DateTimeField(
        db_column="POPRZEDNIE_SALDO_NA_DZIEN", blank=True, null=True
    )
    numer_fk = models.CharField(
        db_column="NUMER_FK", max_length=20, blank=True, null=True
    )
    powod_rezygnacji = models.CharField(
        db_column="POWOD_REZYGNACJI", max_length=300, blank=True, null=True
    )
    termin_rezerwacji = models.CharField(
        db_column="TERMIN_REZERWACJI", max_length=10, blank=True, null=True
    )
    data_aktu_notarialnego = models.CharField(
        db_column="DATA_AKTU_NOTARIALNEGO", max_length=10, blank=True, null=True
    )
    nr_aktu_notarialnego = models.CharField(
        db_column="NR_AKTU_NOTARIALNEGO", max_length=50, blank=True, null=True
    )
    zablokowana = models.CharField(
        db_column="ZABLOKOWANA", max_length=1, blank=True, null=True
    )
    id_spolki = models.IntegerField(db_column="ID_SPOLKI", blank=True, null=True)
    nr_przed_aktu_notarialnego = models.CharField(
        db_column="NR_PRZED_AKTU_NOTARIALNEGO", max_length=50, blank=True, null=True
    )
    data_przed_aktu_notarialnego = models.CharField(
        db_column="DATA_PRZED_AKTU_NOTARIALNEGO", max_length=10, blank=True, null=True
    )
    termin_zmian = models.CharField(
        db_column="TERMIN_ZMIAN", max_length=10, blank=True, null=True
    )
    kredyt_w_banku = models.CharField(
        db_column="KREDYT_W_BANKU", max_length=100, blank=True, null=True
    )
    kredyt_na_kwote = models.CharField(
        db_column="KREDYT_NA_KWOTE", max_length=20, blank=True, null=True
    )
    data_rozwiazania = models.DateTimeField(
        db_column="DATA_ROZWIAZANIA", blank=True, null=True
    )
    waloryzacja_brutto = models.DecimalField(
        db_column="WALORYZACJA_BRUTTO",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    poprzednie_waloryzacja_brutto = models.DecimalField(
        db_column="POPRZEDNIE_WALORYZACJA_BRUTTO",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    do_zaplaty_waloryzacja_brutto = models.DecimalField(
        db_column="DO_ZAPLATY_WALORYZACJA_BRUTTO",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    poprzednie_do_zaplaty_waloryzacja_brutto = models.DecimalField(
        db_column="POPRZEDNIE_DO_ZAPLATY_WALORYZACJA_BRUTTO",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    kredyt_konto = models.CharField(
        db_column="KREDYT_KONTO", max_length=50, blank=True, null=True
    )
    umowa_z_cesja = models.CharField(
        db_column="UMOWA_Z_CESJA", max_length=1, blank=True, null=True
    )
    id_umowy_rezerwacyjnej = models.IntegerField(
        db_column="ID_UMOWY_REZERWACYJNEJ", blank=True, null=True
    )
    rozlicz_roznice_sposob = models.IntegerField(
        db_column="ROZLICZ_ROZNICE_SPOSOB", blank=True, null=True
    )
    id_inwestycji = models.IntegerField(
        db_column="ID_INWESTYCJI", blank=True, null=True
    )
    katalog = models.CharField(
        db_column="KATALOG", max_length=500, blank=True, null=True
    )
    rozlicz_roznice_pow_ponizej = models.FloatField(
        db_column="ROZLICZ_ROZNICE_POW_PONIZEJ", blank=True, null=True
    )
    nr_umowy_bankowej = models.CharField(
        db_column="NR_UMOWY_BANKOWEJ", max_length=100, blank=True, null=True
    )
    prowizja_rezygnacja = models.CharField(
        db_column="PROWIZJA_REZYGNACJA", max_length=20, blank=True, null=True
    )
    kara_opoznienie = models.CharField(
        db_column="KARA_OPOZNIENIE", max_length=20, blank=True, null=True
    )
    czy_dlugoterminowa = models.CharField(
        db_column="CZY_DLUGOTERMINOWA", max_length=1, blank=True, null=True
    )
    id_konta_wplat = models.IntegerField(
        db_column="ID_KONTA_WPLAT", blank=True, null=True
    )
    wartosc_stala_netto = models.DecimalField(
        db_column="WARTOSC_STALA_NETTO",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    wartosc_stala_brutto = models.DecimalField(
        db_column="WARTOSC_STALA_BRUTTO",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    id_posrednika = models.IntegerField(
        db_column="ID_POSREDNIKA", blank=True, null=True
    )
    id_promocji = models.IntegerField(db_column="ID_PROMOCJI", blank=True, null=True)
    notariusz = models.CharField(
        db_column="NOTARIUSZ", max_length=50, blank=True, null=True
    )
    notariusz_umowy = models.CharField(
        db_column="NOTARIUSZ_UMOWY", max_length=50, blank=True, null=True
    )
    termin_gwarancji = models.DateTimeField(
        db_column="TERMIN_GWARANCJI", blank=True, null=True
    )
    termin_rekojmii = models.DateTimeField(
        db_column="TERMIN_REKOJMII", blank=True, null=True
    )
    data_cesji = models.DateTimeField(db_column="DATA_CESJI", blank=True, null=True)
    data_umowy_kredytowej = models.DateTimeField(
        db_column="DATA_UMOWY_KREDYTOWEJ", blank=True, null=True
    )
    firma_doradcza = models.CharField(
        db_column="FIRMA_DORADCZA", max_length=200, blank=True, null=True
    )
    doradca_kredytowy = models.CharField(
        db_column="DORADCA_KREDYTOWY", max_length=200, blank=True, null=True
    )
    bank_kredytowy = models.CharField(
        db_column="BANK_KREDYTOWY", max_length=200, blank=True, null=True
    )
    kwota_kredytu = models.DecimalField(
        db_column="KWOTA_KREDYTU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    waluta_kredytu = models.CharField(
        db_column="WALUTA_KREDYTU", max_length=10, blank=True, null=True
    )
    id_umowy_przedwstepnej = models.IntegerField(
        db_column="ID_UMOWY_PRZEDWSTEPNEJ", blank=True, null=True
    )
    id_konta = models.IntegerField(db_column="ID_KONTA", blank=True, null=True)
    rodzaj = models.ForeignKey(
        TblRodzajeUmow, models.DO_NOTHING, db_column="ID_RODZAJU", blank=True, null=True
    )
    dokument_workflow = models.CharField(
        db_column="DOKUMENT_WORKFLOW", max_length=500, blank=True, null=True
    )
    version = models.TextField(db_column="Version")
    planowana_data_sprzedazy = models.DateTimeField(
        db_column="PLANOWANA_DATA_SPRZEDAZY", blank=True, null=True
    )
    id_ext = models.IntegerField(db_column="ID_EXT", blank=True, null=True)
    wartosc_umowna_netto_przy_rozwiazaniu = models.DecimalField(
        db_column="WARTOSC_UMOWNA_NETTO_PRZY_ROZWIAZANIU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    wartosc_umowna_brutto_przy_rozwiazaniu = models.DecimalField(
        db_column="WARTOSC_UMOWNA_BRUTTO_PRZY_ROZWIAZANIU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    wartosc_koncowa_netto_przy_rozwiazaniu = models.DecimalField(
        db_column="WARTOSC_KONCOWA_NETTO_PRZY_ROZWIAZANIU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    wartosc_koncowa_brutto_przy_rozwiazaniu = models.DecimalField(
        db_column="WARTOSC_KONCOWA_BRUTTO_PRZY_ROZWIAZANIU",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    kto_dodal = models.CharField(
        db_column="KTO_DODAL", max_length=50, blank=True, null=True
    )
    data_dodania = models.DateTimeField(db_column="DATA_DODANIA", blank=True, null=True)
    kto_zmienil = models.CharField(
        db_column="KTO_ZMIENIL", max_length=50, blank=True, null=True
    )
    data_zmiany = models.DateTimeField(db_column="DATA_ZMIANY", blank=True, null=True)
    wyliczanie_koncowej = models.IntegerField(
        db_column="WYLICZANIE_KONCOWEJ", blank=True, null=True
    )
    sugerowany_szablon = models.CharField(
        db_column="SUGEROWANY_SZABLON", max_length=150, blank=True, null=True
    )
    data_zakonczenia = models.DateTimeField(
        db_column="DATA_ZAKONCZENIA", blank=True, null=True
    )
    stawka_prowizji_posrednika = models.DecimalField(
        db_column="STAWKA_PROWIZJI_POSREDNIKA",
        max_digits=38,
        decimal_places=10,
        blank=True,
        null=True,
    )
    id_umowy_aneksowanej = models.IntegerField(
        db_column="ID_UMOWY_ANEKSOWANEJ", blank=True, null=True
    )
    id_formy_umowy = models.IntegerField(
        db_column="ID_FORMY_UMOWY", blank=True, null=True
    )
    nr_konta_do_zwrotow = models.CharField(
        db_column="NR_KONTA_DO_ZWROTOW", max_length=100, blank=True, null=True
    )
    planowana_data_umowy_deweloperskiej = models.DateTimeField(
        db_column="PLANOWANA_DATA_UMOWY_DEWELOPERSKIEJ", blank=True, null=True
    )
    id_notariusza = models.IntegerField(
        db_column="ID_NOTARIUSZA", blank=True, null=True
    )
    id_notariusza_umowy = models.IntegerField(
        db_column="ID_NOTARIUSZA_UMOWY", blank=True, null=True
    )
    uwagi = models.TextField(db_column="UWAGI", blank=True, null=True)
    uwagirtf = models.TextField(db_column="UWAGIRTF", blank=True, null=True)
    data_wyplaty_prowizji = models.DateTimeField(
        db_column="DATA_WYPLATY_PROWIZJI", blank=True, null=True
    )
    zrodlo_finansowania = models.CharField(
        db_column="ZRODLO_FINANSOWANIA", max_length=200, blank=True, null=True
    )
    id_subkonta = models.IntegerField(db_column="ID_SUBKONTA", blank=True, null=True)
    id_budynku = models.BigIntegerField(db_column="ID_BUDYNKU", blank=True, null=True)
    data_anonimizacji = models.DateTimeField(
        db_column="DATA_ANONIMIZACJI", blank=True, null=True
    )
    nazwa_banku_konta_do_zwrotow = models.CharField(
        db_column="NAZWA_BANKU_KONTA_DO_ZWROTOW", max_length=500, blank=True, null=True
    )
    rachunek_wplat_dewelopera = models.CharField(
        db_column="RACHUNEK_WPLAT_DEWELOPERA", max_length=200, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TBL_UMOWY"


class TblObiektyUmowy(models.Model):
    umowa = models.ForeignKey(
        TblUmowy, models.DO_NOTHING, db_column="ID_UMOWY", blank=True, null=True
    )
    lokal = models.ForeignKey(
        TblLokale, models.DO_NOTHING, db_column="ID_LOKALU", blank=True, null=True
    )
    nalezy = models.CharField(db_column="NALEZY", max_length=1, blank=True, null=True)
    data_dodania = models.DateTimeField(db_column="DATA_DODANIA", blank=True, null=True)
    data_usuniecia = models.DateTimeField(
        db_column="DATA_USUNIECIA", blank=True, null=True
    )
    powod_rezygnacji = models.CharField(
        db_column="POWOD_REZYGNACJI", max_length=200, blank=True, null=True
    )
    id_obiektu_umowy = models.AutoField(db_column="ID_OBIEKTU_UMOWY", primary_key=True)
    id_pracownika_dodajacego = models.IntegerField(
        db_column="ID_PRACOWNIKA_DODAJACEGO", blank=True, null=True
    )
    id_pracownika_usuwajacego = models.IntegerField(
        db_column="ID_PRACOWNIKA_USUWAJACEGO", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TBL_OBIEKTY_UMOWY"


class TblRolePodmiotow(models.Model):
    id_roli = models.AutoField(db_column="ID_ROLI", primary_key=True)
    nazwa = models.CharField(db_column="NAZWA", max_length=30, blank=True, null=True)
    opis = models.CharField(db_column="OPIS", max_length=100, blank=True, null=True)
    ukryj = models.CharField(db_column="UKRYJ", max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "TBL_ROLE_PODMIOTOW"


class TblPodmiotyUmowy(models.Model):
    umowa = models.OneToOneField(
        TblUmowy, models.DO_NOTHING, db_column="ID_UMOWY", primary_key=True
    )
    podmiot = models.ForeignKey(TblPodmioty, models.DO_NOTHING, db_column="ID_PODMIOTU")
    rola_podmiotu = models.ForeignKey(
        TblRolePodmiotow,
        models.DO_NOTHING,
        db_column="ROLA_PODMIOTU",
        blank=True,
        null=True,
    )
    udzial_procentowy = models.FloatField(
        db_column="UDZIAL_PROCENTOWY", blank=True, null=True
    )
    moze_odebrac = models.CharField(
        db_column="MOZE_ODEBRAC", max_length=1, blank=True, null=True
    )
    strona_umowy = models.CharField(
        db_column="STRONA_UMOWY", max_length=1, blank=True, null=True
    )
    kieruj_korespondencje = models.CharField(
        db_column="KIERUJ_KORESPONDENCJE", max_length=1, blank=True, null=True
    )
    nalezy = models.CharField(db_column="NALEZY", max_length=1)
    data_dodania = models.DateTimeField(db_column="DATA_DODANIA")
    data_usuniecia = models.DateTimeField(
        db_column="DATA_USUNIECIA", blank=True, null=True
    )
    powod_usuniecia = models.CharField(
        db_column="POWOD_USUNIECIA", max_length=200, blank=True, null=True
    )
    pokazuj_na_fakturach = models.CharField(
        db_column="POKAZUJ_NA_FAKTURACH", max_length=1, blank=True, null=True
    )
    id_pracownika_dodajacego = models.IntegerField(
        db_column="ID_PRACOWNIKA_DODAJACEGO", blank=True, null=True
    )
    id_pracownika_usuwajacego = models.IntegerField(
        db_column="ID_PRACOWNIKA_USUWAJACEGO", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "TBL_PODMIOTY_UMOWY"
        unique_together = (("umowa", "podmiot"),)


class TblUmowaDokument(models.Model):
    dokument = models.ForeignKey(
        TblDokumenty, models.DO_NOTHING, db_column="ID_DOKUMENTU"
    )
    umowa = models.ForeignKey(TblUmowy, models.DO_NOTHING, db_column="ID_UMOWY")
    id_dokumentu_umowy = models.AutoField(
        db_column="ID_DOKUMENTU_UMOWY", primary_key=True
    )

    class Meta:
        managed = False
        db_table = "TBL_UMOWA_DOKUMENT"


class TblUmowaUdzialy(models.Model):
    umowa = models.ForeignKey(TblUmowy, models.DO_NOTHING, db_column="ID_UMOWY")
    podmiot = models.ForeignKey(TblPodmioty, models.DO_NOTHING, db_column="ID_PODMIOTU")
    lokal = models.ForeignKey(TblLokale, models.DO_NOTHING, db_column="ID_LOKALU")
    udzial = models.DecimalField(db_column="UDZIAL", max_digits=5, decimal_places=4)
    id_umowa_udzial = models.BigAutoField(db_column="ID_UMOWA_UDZIAL", primary_key=True)

    class Meta:
        managed = False
        db_table = "TBL_UMOWA_UDZIALY"


class Dtproperties(models.Model):
    objectid = models.IntegerField(blank=True, null=True)
    property = models.CharField(max_length=64)
    value = models.CharField(max_length=255, blank=True, null=True)
    uvalue = models.CharField(max_length=255, blank=True, null=True)
    lvalue = models.BinaryField(blank=True, null=True)
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = "dtproperties"
        unique_together = (("id", "property"),)
