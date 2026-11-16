
# =====================================================
# PROYECTO: SOFTWARE FJ
# Sistema Integral de Gestión de Clientes,
# Servicios y Reservas
# Fase 4 - Componente práctico
# =====================================================

import logging
from abc import ABC, abstractmethod
from datetime import datetime

# Configuración del archivo de registro de eventos
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

print("=" * 55)
print("       SISTEMA INTEGRAL DE GESTIÓN SOFTWARE FJ")
print("=" * 55)
print("Sistema iniciado correctamente.")

# =====================================================
# CLASE ABSTRACTA: ENTIDAD
# =====================================================

class Entidad(ABC):
    """Clase abstracta para las entidades del sistema."""

    def __init__(self, identificacion):
        if not identificacion:
            raise ValueError("La identificación es obligatoria.")

        self._identificacion = identificacion

    @abstractmethod
    def mostrar_informacion(self):
        """Método que deben implementar las clases derivadas."""
        pass


# =====================================================
# CLASE CLIENTE
# =====================================================

class Cliente(Entidad):
    """Representa un cliente de Software FJ."""

    def __init__(self, identificacion, nombre, correo, telefono):
        try:
            super().__init__(identificacion)

            if not nombre or not nombre.strip():
                raise ValueError("El nombre no puede estar vacío.")

            if not correo or "@" not in correo:
                raise ValueError("El correo electrónico no es válido.")

            if not telefono.isdigit() or len(telefono) < 7:
                raise ValueError("El teléfono debe contener al menos 7 dígitos.")

            # Encapsulación de los datos personales
            self.__nombre = nombre.strip()
            self.__correo = correo.strip()
            self.__telefono = telefono

            logging.info("Cliente registrado: %s", identificacion)

        except (ValueError, AttributeError) as error:
            logging.error("Error al registrar cliente: %s", error)
            raise

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def mostrar_informacion(self):
        return (
            f"Identificación: {self._identificacion}\n"
            f"Nombre: {self.__nombre}\n"
            f"Correo: {self.__correo}\n"
            f"Teléfono: {self.__telefono}"
        )

# =====================================================
# CLASE ABSTRACTA: SERVICIO
# =====================================================

class Servicio(ABC):
    """Clase base para los servicios de Software FJ."""

    def __init__(self, codigo, nombre, precio_base):
        if not codigo or not nombre:
            raise ValueError("El código y nombre son obligatorios.")

        if not isinstance(precio_base, (int, float)) or precio_base <= 0:
            raise ValueError("El precio debe ser mayor que cero.")

        self.codigo = codigo
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, cantidad):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass


# =====================================================
# SERVICIO 1: RESERVA DE SALAS
# =====================================================

class ReservaSala(Servicio):

    def calcular_costo(self, cantidad):
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            raise ValueError("La cantidad de horas debe ser positiva.")

        return self.precio_base * cantidad

    def describir_servicio(self):
        return "Servicio de reserva de salas por horas."


# =====================================================
# SERVICIO 2: ALQUILER DE EQUIPOS
# =====================================================

class AlquilerEquipos(Servicio):

    def calcular_costo(self, cantidad):
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad de equipos debe ser un entero positivo.")

        return self.precio_base * cantidad

    def describir_servicio(self):
        return "Servicio de alquiler de equipos tecnológicos."


# =====================================================
# SERVICIO 3: ASESORÍAS ESPECIALIZADAS
# =====================================================

class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, cantidad):
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            raise ValueError("La duración de la asesoría debe ser positiva.")

        return self.precio_base * cantidad

# =====================================================
# EXCEPCIONES PERSONALIZADAS
# =====================================================

class ReservaInvalidaError(Exception):
    """Error cuando una reserva no cumple los requisitos."""
    pass


class OperacionNoPermitidaError(Exception):
    """Error cuando se intenta realizar una operación no permitida."""
    pass


# =====================================================
# CLASE RESERVA
# =====================================================

class Reserva:

    def __init__(self, codigo, cliente, servicio, duracion):
        try:
            if not isinstance(cliente, Cliente):
                raise ReservaInvalidaError("El cliente no es válido.")

            if not isinstance(servicio, Servicio):
                raise ReservaInvalidaError("El servicio no es válido.")

            if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
                raise ReservaInvalidaError("La duración debe ser mayor que cero.")

            self.codigo = codigo
            self.cliente = cliente
            self.servicio = servicio
            self.duracion = duracion
            self.estado = "Pendiente"

            logging.info("Reserva creada: %s", codigo)

        except ReservaInvalidaError as error:
            logging.error("Error al crear reserva: %s", error)
            raise

    # Cálculo del costo con impuestos y descuentos opcionales
    def calcular_total(self, impuesto=0, descuento=0):
        if not isinstance(impuesto, (int, float)) or not 0 <= impuesto <= 100:
            raise ValueError("El impuesto debe estar entre 0 y 100.")

        if not isinstance(descuento, (int, float)) or not 0 <= descuento <= 100:
            raise ValueError("El descuento debe estar entre 0 y 100.")

        subtotal = self.servicio.calcular_costo(self.duracion)
        valor_descuento = subtotal * descuento / 100
        valor_con_descuento = subtotal - valor_descuento
        total = valor_con_descuento * (1 + impuesto / 100)

        return round(total, 2)

    # Confirmación de la reserva
    def confirmar(self):
        try:
            if self.estado != "Pendiente":
                raise OperacionNoPermitidaError(
                    "Solo se pueden confirmar reservas pendientes."
                )

            self.estado = "Confirmada"
            logging.info("Reserva %s confirmada.", self.codigo)
            print(f"Reserva {self.codigo} confirmada correctamente.")

        except OperacionNoPermitidaError as error:
            logging.error("Error al confirmar reserva: %s", error)
            raise

    # Cancelación de la reserva
    def cancelar(self):
        try:
            if self.estado != "Pendiente":
                raise OperacionNoPermitidaError(
                    "No se puede cancelar una reserva que no esté pendiente."
                )

            self.estado = "Cancelada"
            logging.info("Reserva %s cancelada.", self.codigo)
            print(f"Reserva {self.codigo} cancelada correctamente.")

        except OperacionNoPermitidaError as error:
            logging.error("Error al cancelar reserva: %s", error)
            raise

    # Procesamiento de la reserva
    def procesar(self):
        try:
            total = self.calcular_total(impuesto=19, descuento=0)

            if self.estado != "Pendiente":
                raise OperacionNoPermitidaError(
                    "La reserva ya fue procesada."
                )

        except Exception as error:
            logging.error("Error durante el procesamiento: %s", error)
            raise ReservaInvalidaError(
                "No fue posible procesar la reserva."
            ) from error

        else:
            self.confirmar()
            print(f"Valor total de la reserva: ${total:,.2f}")

        finally:
            logging.info(
                "Finalizó el intento de procesamiento de la reserva %s.",
                self.codigo
            )

# =====================================================
# PRUEBAS DE FUNCIONAMIENTO DEL SISTEMA
# Mínimo 10 operaciones
# =====================================================

print("\n" + "=" * 55)
print("       PRUEBAS DEL SISTEMA SOFTWARE FJ")
print("=" * 55)

# OPERACIÓN 1: Registro de un cliente válido
try:
    cliente1 = Cliente(
        "1001",
        "Carlos Pérez",
        "carlos@gmail.com",
        "3101234567"
    )
    print("\n1. Cliente registrado correctamente.")
    print(cliente1.mostrar_informacion())
except Exception as error:
    print("1. Error:", error)

# OPERACIÓN 2: Intento de registro de cliente inválido
try:
    cliente_invalido = Cliente(
        "1002",
        "",
        "correoincorrecto",
        "123"
    )
except ValueError as error:
    print("\n2. Registro inválido controlado:", error)

# OPERACIÓN 3: Creación de servicio de sala
try:
    sala = ReservaSala("S01", "Sala de reuniones", 50000)
    print("\n3. Servicio creado:", sala.describir_servicio())
except Exception as error:
    print("3. Error:", error)

# OPERACIÓN 4: Creación de servicio de equipos
try:
    equipos = AlquilerEquipos("E01", "Alquiler de computadores", 30000)
    print("\n4. Servicio creado:", equipos.describir_servicio())
except Exception as error:
    print("4. Error:", error)

# OPERACIÓN 5: Creación de servicio de asesoría
try:
    asesoria = AsesoriaEspecializada(
        "A01", "Asesoría informática", 80000
    )
    print("\n5. Servicio creado:", asesoria.describir_servicio())
except Exception as error:
    print("5. Error:", error)

# OPERACIÓN 6: Intento de crear un servicio con precio inválido
try:
    servicio_invalido = ReservaSala(
        "S02", "Sala inválida", -5000
    )
except ValueError as error:
    print("\n6. Servicio inválido controlado:", error)

# OPERACIÓN 7: Cálculo del costo de un servicio
try:
    costo = sala.calcular_costo(2)
    print("\n7. Costo de reserva de sala por 2 horas: $", costo)
except Exception as error:
    print("7. Error:", error)

# OPERACIÓN 8: Creación y procesamiento de una reserva
try:
    reserva1 = Reserva("R001", cliente1, sala, 2)
    print("\n8. Reserva creada correctamente.")
    reserva1.procesar()
except Exception as error:
    print("8. Error:", error)

# OPERACIÓN 9: Intento de crear una reserva inválida
try:
    reserva_invalida = Reserva("R002", cliente1, sala, -3)
except ReservaInvalidaError as error:
    print("\n9. Reserva inválida controlada:", error)

# OPERACIÓN 10: Cancelación de una reserva pendiente
try:
    reserva2 = Reserva("R003", cliente1, equipos, 2)
    reserva2.cancelar()
    print("\n10. Reserva cancelada correctamente.")
except Exception as error:
    print("10. Error:", error)

# RESUMEN FINAL
print("\n" + "=" * 55)
print("PRUEBAS DEL SISTEMA FINALIZADAS")
print("Se realizaron 10 operaciones de prueba.")
print("Los errores controlados fueron registrados en los logs.")
print("=" * 55)

logging.info("Finalizaron las 10 operaciones de prueba.")
