
from entidades import Cliente
from servicios import AlquilerEquipo
from reservas import Reserva
from excepciones import DisponibilidadError

cliente = Cliente(
    "CLI900",
    "Cliente de prueba",
    "prueba@example.com",
    "3001234567",
)

equipo = AlquilerEquipo(
    "EQ900",
    "Computador de prueba",
    10000,
    5,
)

print("Inventario inicial:", equipo.cantidad_disponible)

reserva1 = Reserva("RES900", cliente, equipo, 2, 4)
reserva1.confirmar()

print("Después de confirmar 4 equipos:", equipo.cantidad_disponible)

reserva2 = Reserva("RES901", cliente, equipo, 2, 2)

try:
    reserva2.confirmar()
except DisponibilidadError as error:
    print("Segunda reserva rechazada:", error)

print("Estado de la segunda reserva:", reserva2.estado.value)
print("Inventario tras el intento:", equipo.cantidad_disponible)

reserva1.cancelar()

print("Después de cancelar la primera reserva:", equipo.cantidad_disponible)
