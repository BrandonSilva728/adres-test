from django.shortcuts import render
import pandas as pd
from .forms import FileUploadForm
from .models import ValidatedFile, Factura
from datetime import datetime
import os
import re
import fitz  # PyMuPDF
from django.shortcuts import render

def upload_file(request):
    errors = []
    success_message = None

    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            file_name = file.name.lower()  # Convertir a minúsculas para evitar problemas de mayúsculas
            file_extension = file_name.split(".")[-1]  # Obtener la extensión del archivo

            # Validar formato
            if file_extension not in ["csv", "txt"]:
                errors.append("Formato no permitido. Solo se aceptan archivos CSV o TXT.")
            else:
                try:
                    # Cargar archivo según el tipo
                    if file_extension == "csv":
                        df = pd.read_csv(file)
                    elif file_extension == "txt":
                        df = pd.read_csv(file, delimiter=",")  # Archivos TXT separados por tabulaciones
                    
                    # Validar estructura
                    if df.shape[1] != 5:
                        errors.append("El archivo debe contener exactamente 5 columnas.")

                    # Validar contenido
                    for index, row in df.iterrows():
                        values = row.tolist()
                        if len(values) != 5:
                            errors.append(f"Fila {index + 1}: Tiene un número incorrecto de columnas.")
                            continue  # Saltar validaciones si no tiene 5 columnas

                        col1, col2, col3, col4, col5 = values  # Extraer valores de la fila

                        if not (str(col1).isdigit() and 3 <= len(str(col1)) <= 10):
                            errors.append(f"Fila {index + 1}, Columna 1: Debe ser un número de 3 a 10 caracteres.")
                        if "@" not in str(col2):
                            errors.append(f"Fila {index + 1}, Columna 2: No es un correo válido.")
                        if col3 not in ["CC", "TI"]:
                            errors.append(f"Fila {index + 1}, Columna 3: Solo se permiten 'CC' o 'TI'.")
                        if not (500000 <= int(col4) <= 1500000):
                            errors.append(f"Fila {index + 1}, Columna 4: Fuera de rango permitido (500000-1500000).")

                except Exception as e:
                    errors.append(f"Error al procesar el archivo: {str(e)}")

            # Guardar resultado en la base de datos
            if errors:
                result_text = "\n".join(errors)  # Unir errores en un solo texto
            else:
                success_message = "Archivo validado con éxito."
                result_text = success_message  # Si no hay errores, guardar éxito

            ValidatedFile.objects.create(file_name=file_name, result=result_text)

    else:
        form = FileUploadForm()

    return render(request, "upload.html", {"form": form, "errors": errors, "success_message": success_message})

def index(request):
    return render(request, "index.html")

def validation_history(request):
    validations = ValidatedFile.objects.all().order_by("-created_at")  # Ordenado por fecha
    return render(request, "history.html", {"validations": validations})

def validate_invoices(request):
    # Directorio donde se encuentran los PDFs
    # Ajusta esta ruta según la estructura de tu proyecto
    facturas_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "facturas")
    
    # Si no existe la carpeta, se puede crear o mostrar un mensaje
    if not os.path.exists(facturas_dir):
        os.makedirs(facturas_dir)

    cufe_regex = r"\b([0-9a-fA-F]\n*){95,100}\b"

    resultados = []


    for filename in os.listdir(facturas_dir):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(facturas_dir, filename)
            try:
                doc = fitz.open(file_path)
                texto_completo = ""
                for page in doc:
                    texto_completo += page.get_text("text") + "\n"

                match = re.search(cufe_regex, texto_completo, re.MULTILINE)
                cufe = match.group(0).replace("\n", "") if match else "No encontrado"
                numero_paginas = len(doc)
                peso_kb = os.path.getsize(file_path) / 1024

                factura = Factura.objects.create(
                    file_name=filename,
                    numero_paginas=numero_paginas,
                    cufe=cufe,
                    peso_kb=peso_kb
                )
                resultados.append(factura)
            except Exception as e:
                resultados.append(f"Error procesando {filename}: {str(e)}")
    
    context = {
        "results": resultados,
        "message": "Validación de facturas completada."
    }
    return render(request, "validate_invoices.html", context)

def historial_facturas(request):
    facturas = Factura.objects.all().order_by("-created_at")
    return render(request, "historial_facturas.html", {"facturas": facturas})
