from django.urls import path
from . import functions

urlpatterns = [
    path("", functions.index, name="index"),
    path("upload/", functions.upload_file, name="upload_file"),
    path("history/", functions.validation_history, name="history"),
    path("validate_invoices/", functions.validate_invoices, name="validate_invoices"),
    path("historial_facturas/", functions.historial_facturas, name="historial_facturas"),
]