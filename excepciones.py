
"""Excepciones personalizadas del sistema Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base para los errores controlados del sistema."""


class ValidacionError(SoftwareFJError):
    """Se utiliza cuando un dato no cumple las reglas de validación."""


class ClienteError(SoftwareFJError):
    """Se utiliza cuando ocurre un problema relacionado con un cliente."""


class ServicioError(SoftwareFJError):
    """Se utiliza cuando ocurre un problema relacionado con un servicio."""


class ReservaError(SoftwareFJError):
    """Se utiliza cuando ocurre un problema relacionado con una reserva."""


class EstadoReservaError(ReservaError):
    """Se utiliza cuando una operación no está permitida por el estado de la reserva."""


class DisponibilidadError(ReservaError):
    """Se utiliza cuando un servicio no está disponible para la reserva."""

