
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
