
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

