from django.db import models
from accounts.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

class Insumo(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=100)
    stock_minimo = models.DecimalField(max_digits=6, decimal_places=2)
    stock_maximo = models.DecimalField(max_digits=6, decimal_places=2)
    unidad_medida = models.CharField(max_length=20)
    precio_unitario = models.IntegerField()

class Ubicacion(models.Model):
    direccion = models.CharField(max_length=200)

class Bodega(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT)

class InsumoLote(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT)
    fecha_ingreso = models.DateField()
    cantidad_inicial = models.IntegerField()
    cantidad_actual = models.DecimalField(max_digits=6, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    bodega = models.ForeignKey(Bodega, on_delete=models.PROTECT)

class Ubicacion(models.Model):
    direccion = models.CharField(max_length=200)

class Entrada(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT)
    ordenresumen = models.ForeignKey("Ordenresumen", on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=6, decimal_places=2)
    fecha_entrada = models.DateField()

class Salida(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT)
    ordenresumen = models.ForeignKey("Ordenresumen", on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=6, decimal_places=2)
    fecha_salida = models.DateField()

class AlertaInsumo(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT)
    mensaje = models.TextField()

class OrdenInsumo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha = models.DateField()
    estado = models.CharField(max_length=50)

class OrdenInsumoDetalle(models.Model):
    orden_insumo = models.ForeignKey(OrdenInsumo, on_delete=models.CASCADE, related_name="detalles")
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT)
    cantidad_solicitada = models.DecimalField(max_digits=6, decimal_places=2)
