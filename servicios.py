"""Clases de servicios del sistema Software FJ."""

from abc import ABC, abstractmethod

from excepciones import (
    ServicioError,
    ValidacionError,
    DisponibilidadError,
)

class Servicio(ABC):
    """Clase abstracta que define el comportamiento de un servicio."""

    def __init__(self, codigo, nombre, tarifa_base):
        self._codigo = self._validar_texto(codigo, "El código")
        self._nombre = self._validar_texto(nombre, "El nombre")
        self._tarifa_base = self._validar_tarifa(tarifa_base)

    @staticmethod
    def _validar_texto(valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise ValidacionError(
                f"{campo} del servicio es obligatorio."
            )
        return valor.strip()

    @staticmethod
    def _validar_tarifa(valor):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ServicioError("La tarifa debe ser un número.")

        if valor <= 0:
            raise ServicioError("La tarifa debe ser mayor que cero.")

        return float(valor)

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @abstractmethod
    def calcular_costo(self, duracion):
        """Calcula el costo según el tipo de servicio."""
        raise NotImplementedError

    @abstractmethod
    def obtener_descripcion(self):
        """Devuelve una descripción específica del servicio."""
        raise NotImplementedError

    def __str__(self):
        return self.obtener_descripcion()

class ReservaSala(Servicio):
    """Servicio de alquiler de salas por horas."""

    def __init__(self, codigo, nombre, tarifa_base, capacidad):
        super().__init__(codigo, nombre, tarifa_base)

        if isinstance(capacidad, bool) or not isinstance(capacidad, int):
            raise ServicioError(
                "La capacidad debe ser un número entero."
            )

        if capacidad <= 0:
            raise ServicioError(
                "La capacidad debe ser mayor que cero."
            )

        self._capacidad = capacidad

    @property
    def capacidad(self):
        return self._capacidad

    def calcular_costo(self, duracion):
        duracion = self._validar_duracion(duracion)
        return self.tarifa_base * duracion

    def obtener_descripcion(self):
        return (
            f"Sala: {self.nombre} | Capacidad: {self.capacidad} personas | "
            f"Tarifa por hora: ${self.tarifa_base:.2f}"
        )

    @staticmethod
    def _validar_duracion(duracion):
        if isinstance(duracion, bool) or not isinstance(
            duracion, (int, float)
        ):
            raise ServicioError("La duración debe ser numérica.")

        if duracion <= 0:
            raise ServicioError(
                "La duración debe ser mayor que cero."
            )

        return float(duracion)

class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos por horas."""

    def __init__(self, codigo, nombre, tarifa_base, cantidad_disponible):
        super().__init__(codigo, nombre, tarifa_base)

        if (
            isinstance(cantidad_disponible, bool)
            or not isinstance(cantidad_disponible, int)
        ):
            raise ServicioError(
                "La cantidad disponible debe ser un entero."
            )

        if cantidad_disponible < 0:
            raise ServicioError(
                "La cantidad disponible no puede ser negativa."
            )

        self._cantidad_disponible = cantidad_disponible

    @property
    def cantidad_disponible(self):
        return self._cantidad_disponible

    def reservar_equipos(self, cantidad):
        """Descuenta unidades disponibles al confirmar una reserva."""
        self._validar_cantidad(cantidad)

        if cantidad > self._cantidad_disponible:
            raise DisponibilidadError(
                "No hay suficientes equipos disponibles."
            )

        self._cantidad_disponible -= cantidad

    def devolver_equipos(self, cantidad):
        """Devuelve las unidades de una reserva cancelada."""
        self._validar_cantidad(cantidad)
        self._cantidad_disponible += cantidad

    @staticmethod
    def _validar_cantidad(cantidad):
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise ServicioError(
                "La cantidad debe ser un número entero."
            )

        if cantidad <= 0:
            raise ServicioError(
                "La cantidad debe ser mayor que cero."
            )

    def calcular_costo(self, duracion, cantidad=1):
        """Calcula el costo por duración y número de unidades."""
        duracion = ReservaSala._validar_duracion(duracion)
        self._validar_cantidad(cantidad)


        return self.tarifa_base * duracion * cantidad

    def obtener_descripcion(self):
        return (
            f"Alquiler de equipo: {self.nombre} | "
            f"Disponibles: {self.cantidad_disponible} | "
            f"Tarifa por hora y unidad: ${self.tarifa_base:.2f}"
        )

class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría especializada por horas."""

    def __init__(self, codigo, nombre, tarifa_base, especialidad):
        super().__init__(codigo, nombre, tarifa_base)
        self._especialidad = self._validar_texto(
            especialidad, "La especialidad"
        )

    @property
    def especialidad(self):
        return self._especialidad

    def calcular_costo(self, duracion):
        duracion = ReservaSala._validar_duracion(duracion)
        return self.tarifa_base * duracion

    def obtener_descripcion(self):
        return (
            f"Asesoría: {self.nombre} | "
            f"Especialidad: {self.especialidad} | "
            f"Tarifa por hora: ${self.tarifa_base:.2f}"
        )
