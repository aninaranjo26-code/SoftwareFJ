
"""Punto de entrada y pruebas funcionales de Software FJ."""

import logging
import os

from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reservas import Reserva
from gestor import GestorSoftwareFJ


# Crear la carpeta de registros automáticamente.
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename=os.path.join("logs", "softwarefj.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

logger = logging.getLogger("SoftwareFJ")


def ejecutar_operacion(nombre, accion):
    """Ejecuta una operación, registra su resultado y controla errores."""
    print(f"\n--- {nombre} ---")

    try:
        resultado = accion()
    except Exception as error:
        logger.exception("Error durante la operación: %s", nombre)
        print(f"ERROR CONTROLADO: {error}")
        print("La aplicación continúa ejecutándose.")
        return None
    else:
        logger.info("Operación exitosa: %s", nombre)
        print(f"RESULTADO: {resultado}")
        return resultado
    finally:
        logger.info("Finalizó el intento de operación: %s", nombre)


def iniciar_sistema():
    """Ejecuta operaciones de demostración válidas e inválidas."""
    gestor = GestorSoftwareFJ()
    datos = {}

    print("=" * 55)
    print(" SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("=" * 55)

    # Operación 1: registrar un cliente válido.
    def registrar_cliente_1():
        cliente = Cliente(
            "CLI001",
            "María Fernanda López",
            "maria@example.com",
            "3001234567",
        )
        datos["cliente1"] = gestor.registrar_cliente(cliente)
        return cliente.obtener_resumen()

    ejecutar_operacion("1. Registrar cliente válido", registrar_cliente_1)

    # Operación 2: registrar un segundo cliente válido.
    def registrar_cliente_2():
        cliente = Cliente(
            "CLI002",
            "Carlos Andrés Pérez",
            "carlos@example.com",
            "3107654321",
        )
        datos["cliente2"] = gestor.registrar_cliente(cliente)
        return cliente.obtener_resumen()

    ejecutar_operacion("2. Registrar segundo cliente", registrar_cliente_2)

    # Operación 3: intentar crear un cliente con correo inválido.
    ejecutar_operacion(
        "3. Validar correo incorrecto",
        lambda: Cliente(
            "CLI003",
            "Cliente de Prueba",
            "correo-invalido",
            "3001112233",
        ),
    )

    # Operación 4: registrar una sala.
    def registrar_sala():
        servicio = ReservaSala("SER001", "Sala de reuniones", 25000, 12)
        datos["sala"] = gestor.registrar_servicio(servicio)
        return servicio.obtener_descripcion()

    ejecutar_operacion("4. Registrar servicio de sala", registrar_sala)

    # Operación 5: registrar equipos.
    def registrar_equipos():
        servicio = AlquilerEquipo(
            "SER002", "Computador portátil", 12000, 5
        )
        datos["equipo"] = gestor.registrar_servicio(servicio)
        return servicio.obtener_descripcion()

    ejecutar_operacion("5. Registrar servicio de equipos", registrar_equipos)

    # Operación 6: registrar asesorías.
    def registrar_asesoria():
        servicio = AsesoriaEspecializada(
            "SER003", "Asesoría informática", 40000, "Informática"
        )
        datos["asesoria"] = gestor.registrar_servicio(servicio)
        return servicio.obtener_descripcion()

    ejecutar_operacion(
        "6. Registrar asesoría especializada", registrar_asesoria
    )

    # Operación 7: intentar registrar un código de servicio duplicado.
    ejecutar_operacion(
        "7. Rechazar servicio duplicado",
        lambda: gestor.registrar_servicio(
            ReservaSala("SER001", "Otra sala", 30000, 8)
        ),
    )

    # Operación 8: crear y registrar una reserva válida.
    def crear_reserva_sala():
        reserva = Reserva(
            "RES001",
            datos["cliente1"],
            datos["sala"],
            2,
        )
        datos["reserva_sala"] = gestor.registrar_reserva(reserva)
        return reserva.obtener_resumen()

    ejecutar_operacion("8. Crear reserva de sala", crear_reserva_sala)

    # Operación 9: confirmar la reserva.
    ejecutar_operacion(
        "9. Confirmar reserva de sala",
        lambda: datos["reserva_sala"].confirmar().value,
    )

    # Operación 10: procesar una reserva confirmada.
    ejecutar_operacion(
        "10. Procesar reserva confirmada",
        lambda: datos["reserva_sala"].procesar().value,
    )

    # Operación 11: intentar procesar otra vez una reserva procesada.
    ejecutar_operacion(
        "11. Rechazar procesamiento repetido",
        lambda: datos["reserva_sala"].procesar().value,
    )

    # Operación 12: rechazar una reserva con duración inválida.
    ejecutar_operacion(
        "12. Rechazar duración igual a cero",
        lambda: Reserva(
            "RES002",
            datos["cliente1"],
            datos["sala"],
            0,
        ),
    )

    # Operación 13: reservar dos equipos.
    def crear_reserva_equipos():
        reserva = Reserva(
            "RES003",
            datos["cliente2"],
            datos["equipo"],
            3,
            cantidad=2,
        )
        datos["reserva_equipos"] = gestor.registrar_reserva(reserva)
        return reserva.obtener_resumen()

    ejecutar_operacion(
        "13. Crear reserva de dos equipos", crear_reserva_equipos
    )

    # Operación 14: confirmar la reserva de equipos.
    ejecutar_operacion(
        "14. Confirmar reserva de equipos",
        lambda: datos["reserva_equipos"].confirmar().value,
    )

    # Operación 15: crear y cancelar una reserva pendiente.
    def crear_reserva_asesoria():
        reserva = Reserva(
            "RES004",
            datos["cliente1"],
            datos["asesoria"],
            1,
        )
        datos["reserva_asesoria"] = gestor.registrar_reserva(reserva)
        return reserva.obtener_resumen()

    ejecutar_operacion(
        "15. Crear reserva de asesoría", crear_reserva_asesoria
    )

    ejecutar_operacion(
        "16. Cancelar reserva pendiente",
        lambda: datos["reserva_asesoria"].cancelar().value,
    )

    # Resumen final del sistema.
    print("\n" + "=" * 55)
    print("RESUMEN FINAL")
    print("=" * 55)
    print(f"Clientes registrados: {len(gestor.clientes)}")
    print(f"Servicios registrados: {len(gestor.servicios)}")
    print(f"Reservas registradas: {len(gestor.reservas)}")
    print("Consulte logs/softwarefj.log para revisar los eventos.")
    print("Fin de las operaciones de demostración.")

    logger.info("Finalizó la ejecución de demostración de Software FJ.")


if __name__ == "__main__":
    iniciar_sistema()
