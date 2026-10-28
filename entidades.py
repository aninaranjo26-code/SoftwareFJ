
"""Entidades principales del sistema Software FJ."""

from abc import ABC, abstractmethod
import re

from excepciones import ValidacionError, ClienteError


class EntidadBase(ABC):
    """Clase abstracta que define la estructura general de una entidad."""

    def __init__(self, identificador):
        identificador = str(identificador).strip()

        if not identificador:
            raise ValidacionError("El identificador no puede estar vacío.")

        self._identificador = identificador

    @property
    def identificador(self):
        """Permite consultar el identificador sin modificarlo directamente."""
        return self._identificador

    @abstractmethod
    def obtener_resumen(self):
        """Devuelve un resumen descriptivo de la entidad."""
        raise NotImplementedError(
            "Las clases derivadas deben implementar obtener_resumen()."
        )


class Cliente(EntidadBase):
    """Representa un cliente con datos personales encapsulados."""

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)

        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ClienteError("El nombre del cliente es obligatorio.")

        nombre_limpio = " ".join(valor.split())

        if len(nombre_limpio) < 3:
            raise ClienteError("El nombre debe tener al menos 3 caracteres.")

        self._nombre = nombre_limpio

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str):
            raise ClienteError("El correo debe ser texto.")

        correo_limpio = valor.strip().lower()
        patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(patron, correo_limpio):
            raise ClienteError("El correo electrónico no tiene un formato válido.")

        self._correo = correo_limpio

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not isinstance(valor, str):
            valor = str(valor)

        telefono_limpio = re.sub(r"[\s()-]", "", valor)

        if not re.fullmatch(r"\+?\d{7,15}", telefono_limpio):
            raise ClienteError(
                "El teléfono debe contener entre 7 y 15 dígitos; "
                "puede comenzar con +."
            )

        self._telefono = telefono_limpio

    def obtener_resumen(self):
        """Devuelve información del cliente sin exponer todos sus datos."""
        return (
            f"Cliente: {self.nombre} | "
            f"Identificador: {self.identificador}"
        )

    def __str__(self):
        return self.obtener_resumen()
