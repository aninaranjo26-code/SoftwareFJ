
"""Gestión del ciclo de vida de las reservas de Software FJ."""

from datetime import datetime
from enum import Enum

from entidades import Cliente
from servicios import Servicio, AlquilerEquipo
from excepciones import (
    ReservaError,
    EstadoReservaError,
    DisponibilidadError,
)


class EstadoReserva(Enum):
    """Estados permitidos para una reserva."""

    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"


class Reserva:
    """Representa una reserva asociada a un cliente y un servicio."""

    def __init__(
        self,
        codigo,
        cliente,
        servicio,
        duracion,
        cantidad=1,
    ):
        self._codigo = self._validar_codigo(codigo)

        if not isinstance(cliente, Cliente):
            raise ReservaError(
                "La reserva requiere un cliente válido."
            )

        if not isinstance(servicio, Servicio):
            raise ReservaError(
                "La reserva requiere un servicio válido."
            )

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = self._validar_duracion(duracion)
        self._cantidad = self._validar_cantidad(cantidad)
        self._estado = EstadoReserva.PENDIENTE
        self._fecha_creacion = datetime.now()
        self._fecha_actualizacion = self._fecha_creacion
        self._costo = self._calcular_costo()

    @staticmethod
    def _validar_codigo(codigo):
        if codigo is None or not str(codigo).strip():
            raise ReservaError(
                "El código de la reserva es obligatorio."
            )
        return str(codigo).strip()

    @staticmethod
    def _validar_duracion(duracion):
        if isinstance(duracion, bool) or not isinstance(
            duracion, (int, float)
        ):
            raise ReservaError("La duración debe ser numérica.")

        if duracion <= 0:
            raise ReservaError(
                "La duración debe ser mayor que cero."
            )

        return float(duracion)

    @staticmethod
    def _validar_cantidad(cantidad):
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise ReservaError(
                "La cantidad debe ser un número entero."
            )

        if cantidad <= 0:
            raise ReservaError(
                "La cantidad debe ser mayor que cero."
            )

        return cantidad

    def _calcular_costo(self):
        """Calcula el costo según el tipo de servicio."""
        try:
            if isinstance(self._servicio, AlquilerEquipo):
                return self._servicio.calcular_costo(
                    self._duracion,
                    self._cantidad,
                )

            return self._servicio.calcular_costo(self._duracion)

        except Exception as error:
            raise ReservaError(
                "No fue posible calcular el costo de la reserva."
            ) from error

    @property
    def codigo(self):
        return self._codigo

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @property
    def fecha_actualizacion(self):
        return self._fecha_actualizacion

    def confirmar(self):
        """Confirma la reserva y aparta equipos cuando corresponde."""
        if self._estado is not EstadoReserva.PENDIENTE:
            raise EstadoReservaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        if isinstance(self._servicio, AlquilerEquipo):
            self._servicio.reservar_equipos(self._cantidad)

        self._estado = EstadoReserva.CONFIRMADA
        self._fecha_actualizacion = datetime.now()
        return self._estado

    def cancelar(self):
        """Cancela una reserva y libera los equipos confirmados."""
        if self._estado not in (
            EstadoReserva.PENDIENTE,
            EstadoReserva.CONFIRMADA,
        ):
            raise EstadoReservaError(
                "Solo se pueden cancelar reservas pendientes o confirmadas."
            )

        if (
            self._estado is EstadoReserva.CONFIRMADA
            and isinstance(self._servicio, AlquilerEquipo)
        ):
            self._servicio.devolver_equipos(self._cantidad)

        self._estado = EstadoReserva.CANCELADA
        self._fecha_actualizacion = datetime.now()
        return self._estado

    def procesar(self):
        """Procesa únicamente una reserva confirmada."""
        if self._estado is not EstadoReserva.CONFIRMADA:
            raise EstadoReservaError(
                "Solo se pueden procesar reservas confirmadas."
            )

        self._estado = EstadoReserva.PROCESADA
        self._fecha_actualizacion = datetime.now()
        return self._estado

    def obtener_resumen(self):
        """Genera un resumen de la reserva."""
        return (
            f"Reserva: {self.codigo} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion:g} hora(s) | "
            f"Cantidad: {self.cantidad} | "
            f"Costo: ${self.costo:.2f} | "
            f"Estado: {self.estado.value}"
        )

    def __str__(self):
        return self.obtener_resumen()
