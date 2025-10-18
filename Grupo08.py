
from enum import Enum
from datetime import date
from typing import List, Union

SUELDO_MINIMO_VITAL = 1130.0

class TipoCese(Enum):
    RENUNCIA = "Renuncia Voluntaria"
    DESPIDO = "Despido"
    TERMINO_DE_CONTRATO = "Término de Contrato"

class EstadoTrabajador(Enum):
    ACTIVO = "Activo"
    CESADO = "Cesado"

class Direccion:
    def __init__(self, direccion: str, referencia: str, distrito: str, provincia: str, departamento: str):
        self.__Direccion = direccion
        self.__Referencia = referencia
        self.__Distrito = distrito
        self.__Provincia = provincia
        self.__Departamento = departamento
    
    def __str__(self):
        return f"{self.__Direccion}, {self.__Distrito}"

class Persona:
    def __init__(self, tipo_documento: str, nro_documento: str, nombre: str, apellido_paterno: str, apellido_materno: str, direccion: Direccion):
        self.__TipDocIdentidad = tipo_documento
        self.__NroDocIdentidad = nro_documento
        self.__Nombre = nombre
        self.__ApellidoPaterno = apellido_paterno
        self.__ApellidoMaterno = apellido_materno
        self.__Direccion = direccion
    
    @property
    def TipDocIdentidad(self):
        return self.__TipDocIdentidad
    
    @property
    def NroDocIdentidad(self):
        return self.__NroDocIdentidad
        
    def NombreCompleto(self):
        return f"{self.__Nombre} {self.__ApellidoPaterno} {self.__ApellidoMaterno}"

class ONP:
    def __init__(self, aportacion_unica: float = 0.13):
        self.__AportacionUnica = aportacion_unica
        
    def calcular_descuento(self, sueldo_bruto: float, es_comision_flujo: bool = None) -> float:
        return sueldo_bruto * self.__AportacionUnica
        
    def __str__(self):
        return "ONP"

class AFP:
    def __init__(self, nombre: str, aporte_obligatorio: float, prima_seguro: float, comision_flujo: float):
        self.__Nombre = nombre
        self.__AporteObligatorio = aporte_obligatorio
        self.__PrimaSeguro = prima_seguro
        self.__ComisionFlujo = comision_flujo
        
    def calcular_descuento(self, sueldo_bruto: float, es_comision_flujo: bool) -> float:
        aporte = sueldo_bruto * self.__AporteObligatorio
        prima = sueldo_bruto * self.__PrimaSeguro
        comision = 0.0
        # --- Calculo de Comision ---
        if es_comision_flujo:
            comision = sueldo_bruto * self.__ComisionFlujo
        return aporte + prima + comision
        
    def __str__(self):
        return f"AFP {self.__Nombre}"

class Integra(AFP):
    def __init__(self): 
        super().__init__(nombre="Integra", aporte_obligatorio=0.10, prima_seguro=0.0184, comision_flujo=0.0155)
        
class Prima(AFP):
    def __init__(self): 
        super().__init__(nombre="Prima", aporte_obligatorio=0.10, prima_seguro=0.0184, comision_flujo=0.0160)
        
class Habitat(AFP):
    def __init__(self): 
        super().__init__(nombre="Habitat", aporte_obligatorio=0.10, prima_seguro=0.0184, comision_flujo=0.0147)
        
class Profuturo(AFP):
    def __init__(self): 
        super().__init__(nombre="Profuturo", aporte_obligatorio=0.10, prima_seguro=0.0184, comision_flujo=0.0162)

class TipoDeContrato:
    def __init__(self, fecha_inicio: date, sueldo_base: float):
        self.__FechaInicio = fecha_inicio
        self.__SueldoBase = sueldo_base
    
    @property
    def sueldoBase(self):
        return self.__SueldoBase

class Trabajador(Persona):
    def __init__(self, tipo_documento: str, nro_documento: str, nombre: str, apellido_paterno: str, apellido_materno: str, direccion: Direccion, contrato: TipoDeContrato, sistema_pension: Union[AFP, ONP], tiene_asignacion: bool, es_comision_flujo: bool):
        super().__init__(tipo_documento, nro_documento, nombre, apellido_paterno, apellido_materno, direccion)
        self.__Contrato = contrato
        self.__SistemaPension = sistema_pension
        self.__AsignacionFamiliar = tiene_asignacion
        self.__ComisionFlujo = es_comision_flujo 
        self.__Estado = EstadoTrabajador.ACTIVO
        self.__IngresosAdicionales: List[Ingreso] = []
        self.__DescuentosAdicionales: List[Descuento] = []
    
    @property
    def contrato(self):
        return self.__Contrato
    
    @property
    def estado(self):
        return self.__Estado
    
    @property
    def ingresosAdicionales(self):
        return self.__IngresosAdicionales
    
    @property
    def descuentosAdicionales(self):
        return self.__DescuentosAdicionales
        
    @property
    def sistemaPension(self):
        return self.__SistemaPension
    
    @property
    def asignacionFamiliar(self):
        return self.__AsignacionFamiliar
    
    @property
    def comisionFlujo(self):
        return self.__ComisionFlujo
        
    def darBajaTrabajador(self, tipo_cese: TipoCese):
        self.__Estado = EstadoTrabajador.CESADO
        print(f"\n El trabajador {self.NombreCompleto()} ha sido dado de baja por: {tipo_cese.value}.")
        
    def limpiar_registros_mensuales(self):
        self.__IngresosAdicionales.clear()
        self.__DescuentosAdicionales.clear()

class Ingreso:
    def __init__(self, tipo_ingreso: str, monto: float): 
        self.__TipoIngreso = tipo_ingreso
        self.__Monto = monto
    
    @property
    def tipoIngreso(self):
        return self.__TipoIngreso
    
    @property
    def monto(self):
        return self.__Monto
        
class Descuento:
    def __init__(self, tipo_descuento: str, monto: float): 
        self.__TipoDescuento = tipo_descuento
        self.__Monto = monto
    
    @property
    def tipoDescuento(self):
        return self.__TipoDescuento
    
    @property
    def monto(self):
        return self.__Monto

class Empresa:
    def __init__(self, ruc: str, razon_social: str, direccion_fiscal: str):
        self.__Ruc = ruc
        self.__RazonSocial = razon_social
        self.__DireccionFiscal = direccion_fiscal
        self.__Trabajadores: List[Trabajador] = []
        
    def contratar_trabajador(self, trabajador: Trabajador):
        self.__Trabajadores.append(trabajador)
        print(f"\n {trabajador.NombreCompleto()} ha sido contratado/a exitosamente.")
    
    @property
    def ruc(self):
        return self.__Ruc
    
    @property
    def razonSocial(self):
        return self.__RazonSocial
        
    @property
    def direccionFiscal(self):
        return self.__DireccionFiscal
    
    @property
    def trabajadores(self):
        return self.__Trabajadores
        
def registrar_empresa() -> Empresa:
    print("="*40)
    print("Bienvenido al Sistema de Gestión de Planillas")
    print("Para comenzar, registre los datos de su empresa.")
    print("="*40)
    ruc = input("Ingrese el RUC de la empresa: ")
    razon_social = input("Ingrese la Razón Social: ")
    direccion_fiscal = input("Ingrese la Dirección Fiscal: ")
    print("\n Empresa registrada correctamente.")
    return Empresa(ruc, razon_social, direccion_fiscal)
    
def mostrar_datos_empresa(empresa: Empresa):
    print("\n--- Datos de la Empresa Registrada ---")
    print(f"RUC: {empresa.ruc}")
    print(f"Razón Social: {empresa.razonSocial}")
    print(f"Dirección Fiscal: {empresa.direccionFiscal}")

def seleccionar_trabajador_activo(empresa: Empresa) -> Union[Trabajador, None]:
    activos = [t for t in empresa.trabajadores if t.estado == EstadoTrabajador.ACTIVO]
    if not activos: 
        print("\nNo hay trabajadores activos registrados.")
        return None
    
    print("\nSeleccione un trabajador:")
    for i, t in enumerate(activos): 
        print(f"{i+1}. {t.NombreCompleto()}")
    try:
        opcion = int(input("Opción: "))
        return activos[opcion - 1] if 1 <= opcion <= len(activos) else print("Elección fuera de rango.")
    except (ValueError, IndexError):
        print("Selección no válida.")
        return None

def registrar_nuevo_trabajador(empresa: Empresa):
    print("\n--- Registro de Nuevo Trabajador ---")
    nombre = input("Nombres: ")
    paterno = input("Apellido Paterno: ")
    materno = input("Apellido Materno: ")
    nro_doc = input("Nro Documento (DNI): ")
    dir_calle = input("Dirección (Calle y Nro): ")
    distrito = input("Distrito: ")
    try: 
        sueldo = float(input("Sueldo Base: S/ "))
    except ValueError: print("Error: El sueldo debe ser un número."); return

    tiene_asignacion = True if input("¿Tiene derecho a Asignación Familiar? (s/n): ").lower() == 's' else False

    es_flujo = False
    sistema_pension = None
    while not sistema_pension:
        print("\nSistema de Pensiones: \n1.AFP Integra\n2.AFP Prima\n3.AFP Habitat\n4.AFP Profuturo\n5.ONP")
        op = input("Opción: ")
        if op in ["1", "2", "3", "4"]:
            if op == "1": sistema_pension = Integra()
            elif op == "2": sistema_pension = Prima()
            elif op == "3": sistema_pension = Habitat()
            elif op == "4": sistema_pension = Profuturo()
      
            while True:
                comision_op = input(f"Seleccione el tipo de comisión para {sistema_pension}:\n  1. Comisión por Flujo\n  2. Comisión Mixta (sobre Saldo)\nOpción: ")
                if comision_op == "1": es_flujo = True; break
                elif comision_op == "2": es_flujo = False; break
                else: print("Opción no válida.")
        elif op == "5": sistema_pension = ONP(); break
        else: print("Opción no válida.")
    
    empresa.contratar_trabajador(Trabajador("DNI", nro_doc, nombre, paterno, materno, Direccion(dir_calle, "N/A", distrito, "Lima", "Lima"), TipoDeContrato(date.today(), sueldo), sistema_pension, tiene_asignacion, es_flujo))

def generar_boleta_pago(empresa: Empresa):
    print("\n--- Generar Boleta de Pago ---")
    trabajador = seleccionar_trabajador_activo(empresa)
    if not trabajador: return
    
    ingresos = [Ingreso("Sueldo Básico", trabajador.contrato.sueldoBase)]
    if trabajador.asignacionFamiliar: ingresos.append(Ingreso("Asignación Familiar", SUELDO_MINIMO_VITAL * 0.10))
    ingresos.extend(trabajador.ingresosAdicionales)
    sueldo_bruto = sum(ing.monto for ing in ingresos)
    
    descuentos = []
       
    descuento_pension = trabajador.sistemaPension.calcular_descuento(sueldo_bruto, trabajador.comisionFlujo)
    descuentos.append(Descuento(f"Aporte {trabajador.sistemaPension}", descuento_pension))
        
    if sueldo_bruto > 2400: descuentos.append(Descuento("Renta 5ta Categoría", (sueldo_bruto - 2400) * 0.08))
    descuentos.extend(trabajador.descuentosAdicionales)
    total_descuentos = sum(desc.monto for desc in descuentos)
    sueldo_neto = sueldo_bruto - total_descuentos
        
    print("\n" + "="*45); print(f"BOLETA DE PAGO - {date.today().strftime('%B %Y')}".upper().center(45)); print("="*45)
    print(f"Empresa: {empresa.razonSocial} (RUC: {empresa.ruc})")
    print(f"Trabajador: {trabajador.NombreCompleto()} (DNI: {trabajador.NroDocIdentidad})")
    print("-"*45); print("INGRESOS:")
    for ing in ingresos: print(f"  {ing.tipoIngreso:<25} S/ {ing.monto:12.2f}")
    print(f"{'TOTAL INGRESOS':<27} S/ {sueldo_bruto:12.2f}"); print("-"*45); print("DESCUENTOS:")
    for desc in descuentos: print(f"  {desc.tipoDescuento:<25} S/ {desc.monto:12.2f}")
    print(f"{'TOTAL DESCUENTOS':<27} S/ {total_descuentos:12.2f}"); print("-"*45)
    print(f"{'SUELDO NETO A PAGAR':<27} S/ {sueldo_neto:12.2f}"); print("="*45)
    
    if isinstance(trabajador.sistemaPension, AFP):
        tipo_comision_str = "Comisión por Flujo" if trabajador.comisionFlujo else "Comisión Mixta"
        print(f"Nota: El cálculo AFP se realizó con {tipo_comision_str}.")
        if not trabajador.comisionFlujo:
             print("(La comisión sobre saldo no se incluye según el UML).")
    
    trabajador.limpiar_registros_mensuales()

def registrar_ingreso_trabajador(empresa: Empresa):
    print("\n--- Registrar Ingreso (Bono, Movilidad, etc.) ---")
    trabajador = seleccionar_trabajador_activo(empresa)
    if not trabajador: return
    tipo_ingreso = input("Tipo de Ingreso: ")
    monto = float(input(f"Monto de '{tipo_ingreso}': S/ "))
    trabajador.ingresosAdicionales.append(Ingreso(tipo_ingreso, monto))
    print(f"\n Ingreso registrado.")

def registrar_descuento_trabajador(empresa: Empresa):
    print("\n--- Registrar Descuento (Adelanto, Préstamo, etc.) ---")
    trabajador = seleccionar_trabajador_activo(empresa)
    if not trabajador: return
    tipo_descuento = input("Tipo de Descuento: ")
    monto = float(input(f"Monto de '{tipo_descuento}': S/ "))
    trabajador.descuentosAdicionales.append(Descuento(tipo_descuento, monto))
    print(f"\n Descuento registrado.")
    
def dar_baja_trabajador(empresa: Empresa):
    print("\n--- Dar de Baja a un Trabajador ---")
    trabajador = seleccionar_trabajador_activo(empresa)
    if not trabajador: return
    print("\nSeleccione el motivo del cese:"); [print(f"{i+1}. {c.value}") for i,c in enumerate(TipoCese)]
    try: op_cese = int(input("Motivo: ")); trabajador.darBajaTrabajador(list(TipoCese)[op_cese - 1])
    except (ValueError, IndexError): print("Motivo no válido.")
    
def listar_trabajadores(empresa: Empresa, estado: EstadoTrabajador):
    print(f"\n--- Lista de Trabajadores {estado.name.capitalize()}s ---")
    lista = [t for t in empresa.trabajadores if t.estado == estado]
    if not lista: print(f"No se encontraron trabajadores con estado '{estado.value}'."); return
    for t in lista: print(f"- {t.NombreCompleto()} (DNI: {t.NroDocIdentidad})")

if __name__ == "__main__":
    mi_empresa = registrar_empresa()
    while True:
        print("\n" + "="*20 + f" MENU: {mi_empresa.razonSocial} " + "="*20)
        print("1. Registrar Nuevo Trabajador")
        print("2. Registrar Ingreso Adicional (Bono, etc.)")
        print("3. Registrar Descuento Adicional (Adelanto, etc.)")
        print("4. Generar Boleta de Pago")
        print("5. Dar de Baja a un Trabajador")
        print("6. Lista de Trabajadores Activos")
        print("7. Lista de Trabajadores Cesados")
        print("8. Ver Datos de la Empresa")
        print("9. Salir")
        print("="*(50 + len(mi_empresa.razonSocial)))
        opcion = input("Seleccione una opción: ")
        if opcion == "1": registrar_nuevo_trabajador(mi_empresa)
        elif opcion == "2": registrar_ingreso_trabajador(mi_empresa)
        elif opcion == "3": registrar_descuento_trabajador(mi_empresa)
        elif opcion == "4": generar_boleta_pago(mi_empresa)
        elif opcion == "5": dar_baja_trabajador(mi_empresa)
        elif opcion == "6": listar_trabajadores(mi_empresa, EstadoTrabajador.ACTIVO)
        elif opcion == "7": listar_trabajadores(mi_empresa, EstadoTrabajador.CESADO)
        elif opcion == "8": mostrar_datos_empresa(mi_empresa)
        elif opcion == "9": print("\nSaliendo del programa. ¡Hasta luego!"); break
        else: print("\n Opción no válida. Por favor, intente de nuevo.")

