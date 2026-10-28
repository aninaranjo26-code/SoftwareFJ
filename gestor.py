
"""Gestor central de clientes, servicios y reservas de Software FJ."""

from excepciones import (
    ClienteError,
    ServicioError,
    ReservaError,
)
from entidades import Cliente
from servicios import Servicio


class GestorSoftwareFJ:
    """Administra las colecciones de objetos durante la ejecución."""

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    @property
    def clientes(self):
        return tuple(self._clientes)

    @property
    def servicios(self):
        return tuple(self._servicios)

    @property
    def reservas(self):
        return tuple(self._reservas)

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise ClienteError(
                "Solo se pueden registrar objetos de tipo Cliente."
            )

        if any(
            existente.identificador == cliente.identificador
            for existente in self._clientes
        ):
            raise ClienteError(
                f"Ya existe el cliente {cliente.identificador}."
            )

        if any(
            existente.correo == cliente.correo
            for existente in self._clientes
        ):
            raise ClienteError(
                f"El correo {cliente.correo} ya está registrado."
            )

        self._clientes.append(cliente)
        return cliente

    def buscar_cliente(self, identificador):
        identificador = str(identificador).strip()

        for cliente in self._clientes:
            if cliente.identificador == identificador:
                return cliente

        raise ClienteError(
            f"No se encontró el cliente con identificador {identificador}."
        )

    def registrar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise ServicioError(
                "Solo se pueden registrar objetos de tipo Servicio."
            )

        if any(
            existente.codigo == servicio.codigo
            for existente in self._servicios
        ):
            raise ServicioError(
                f"Ya existe el servicio {servicio.codigo}."
            )

        self._servicios.append(servicio)
        return servicio

    def buscar_servicio(self, codigo):
        codigo = str(codigo).strip()

        for servicio in self._servicios:
            if servicio.codigo == codigo:
                return servicio

        raise ServicioError(
            f"No se encontró el servicio con código {codigo}."
        )

    def registrar_reserva(self, reserva):
        from reservas import Reserva

        if not isinstance(reserva, Reserva):
            raise ReservaError(
                "Solo se pueden registrar objetos de tipo Reserva."
            )

        if any(
            existente.codigo == reserva.codigo
            for existente in self._reservas
        ):
            raise ReservaError(
                f"Ya existe la reserva {reserva.codigo}."
            )

        self._reservas.append(reserva)
        return reserva

    def buscar_reserva(self, codigo):
        codigo = str(codigo).strip()

        for reserva in self._reservas:
            if reserva.codigo == codigo:
                return reserva

        raise ReservaError(
            f"No se encontró la reserva con código {codigo}."
        )

    def listar_clientes(self):
        return [cliente.obtener_resumen() for cliente in self._clientes]

    def listar_servicios(self):
        return [servicio.obtener_descripcion() for servicio in self._servicios]

    def listar_reservas(self):
        return [reserva.obtener_resumen() for reserva in self._reservas]
