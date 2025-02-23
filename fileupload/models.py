from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ValidatedFile(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} - {self.result} ({self.created_at})"

class Factura(models.Model):
    file_name = models.CharField(max_length=255)
    numero_paginas = models.IntegerField()
    cufe = models.TextField()
    peso_kb = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} - {self.cufe}"