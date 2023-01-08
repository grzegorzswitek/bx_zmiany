from .models import (
    TblPodmioty,
    TblUmowy,
    TblLokale,
    TblPodmiotyUmowy,
    TblObiektyUmowy,
    TblInwestycje,
    TblBudynki,
    TblDokumenty,
    TblGrupyVat,
    TblTypyLokali,
    TblStatusyUmowy,
    TblTypyUmow,
    TblRodzajeUmow,
    TblRolePodmiotow,
    TblUmowaDokument,
    TblUmowaUdzialy,
)


class MyDBRouter(object):
    def db_for_read(self, model, **hints):
        if model in (
            TblPodmioty,
            TblUmowy,
            TblLokale,
            TblPodmiotyUmowy,
            TblObiektyUmowy,
            TblInwestycje,
            TblBudynki,
            TblDokumenty,
            TblGrupyVat,
            TblTypyLokali,
            TblStatusyUmowy,
            TblTypyUmow,
            TblRodzajeUmow,
            TblRolePodmiotow,
            TblUmowaDokument,
            TblUmowaUdzialy,
        ):
            return "crm"
        return None
