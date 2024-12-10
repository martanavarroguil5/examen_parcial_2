import heapq
import json
from datetime import datetime

# mwnú que te dé a elegir una función
def menu():
    print("\nGestor de Tareas con Prioridades")
    print("1. Añadir tarea")
    print("2. Mostrar todas las tareas pendientes")
    print("3. Completar tarea")
    print("4. Obtener tarea con mayor prioridad")
    print("5. Verificar si una tarea es ejecutable")
    print("6. Salir")
    while True:
        opcion = input("Selecciona una opción: ")
        if opcion.isdigit() and 1 <= int(opcion) <= 6:
            return opcion
        print("Por favor, selecciona una opción válida entre 1 y 6.")

# Función que valida una fecha en formato YYYY-MM-DD
def validar_fecha(fecha_str):
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d")
    except ValueError:
        return None

# Guardar tareas en un archivo
def guardar_tareas(heap, archivo="tareas.json"):
    with open(archivo, "w") as f:
        json.dump([(p, fecha.strftime("%Y-%m-%d"), n, d) for p, fecha, n, d in heap], f)

# Cargar tareas desde un archivo
def cargar_tareas(archivo="tareas.json"):
    try:
        with open(archivo, "r") as f:
            return [(p, validar_fecha(fecha), n, d) for p, fecha, n, d in json.load(f)]
    except FileNotFoundError:
        return []

# Función que añade una tarea pidiendo nombre, prioridad, fecha de vencimiento y dependencias
def añadir_tarea(heap):
    while True:
        nombre = input("Nombre de la tarea: ").strip()
        if nombre:
            break
        print("El nombre de la tarea no puede estar vacío.")

    while True:
        try:
            prioridad = int(input("Prioridad (número más bajo = mayor prioridad): "))
            break
        except ValueError:
            print("Por favor, introduce un número entero válido.")
    
    while True:
        fecha_vencimiento_str = input("Fecha de vencimiento (YYYY-MM-DD): ")
        fecha_vencimiento = validar_fecha(fecha_vencimiento_str)
        if fecha_vencimiento:
            break
        print("Por favor, introduce una fecha válida en formato YYYY-MM-DD.")

    dependencias = input("Dependencias (separadas por coma, o vacío si no hay): ").split(",")
    dependencias = [d.strip() for d in dependencias if d.strip()]

    heapq.heappush(heap, (prioridad, fecha_vencimiento, nombre, dependencias))
    print(f"Tarea '{nombre}' añadida con prioridad {prioridad}, fecha de vencimiento {fecha_vencimiento_str} y dependencias: {dependencias}")
    guardar_tareas(heap)

# Con esta función se muestran las tareas en orden de prioridad o fecha de vencimiento
def mostrar_tareas(heap):
    if not heap:
        print("No hay tareas pendientes.")
        return

    print("\nTareas pendientes:")
    for prioridad, fecha_vencimiento, nombre, dependencias in sorted(heap):
        dep_str = ", ".join(dependencias) if dependencias else "Sin dependencias"
        estado = "Ejecutable" if all(dep not in [n for _, _, n, _ in heap] for dep in dependencias) else "No ejecutable"
        print(f"- {nombre} (Prioridad: {prioridad}, Fecha de vencimiento: {fecha_vencimiento.strftime('%Y-%m-%d')}, Dependencias: {dep_str}, Estado: {estado})")

# Esta función sirve para completar una tarea, es decir, eliminarla por nombre
def completar_tarea(heap):
    if not heap:
        print("No hay tareas para completar.")
        return

    while True:
        nombre_tarea = input("Nombre de la tarea a completar: ").strip()
        if nombre_tarea:
            break
        print("El nombre de la tarea no puede estar vacío.")

    for i, (prioridad, fecha_vencimiento, nombre, dependencias) in enumerate(heap):
        if nombre == nombre_tarea:
            if dependencias:
                pendientes = [dep for dep in dependencias if dep in [n for _, _, n, _ in heap]]
                if pendientes:
                    print(f"No se puede completar '{nombre}' hasta que se completen sus dependencias: {', '.join(pendientes)}")
                    return
            print(f"Tarea completada: {nombre}")
            heap.pop(i)
            heapq.heapify(heap)  # Reorganizar el heap
            guardar_tareas(heap)
            return
    print(f"Tarea '{nombre_tarea}' no encontrada.")

# Esta función obtiene la tarea con mayor prioridad sin eliminarla del heap
def obtener_tarea_prioritaria(heap):
    if not heap:
        print("No hay tareas pendientes.")
        return

    prioridad, fecha_vencimiento, nombre, dependencias = heap[0]
    dep_str = ", ".join(dependencias) if dependencias else "Sin dependencias"
    estado = "Ejecutable" if all(dep not in [n for _, _, n, _ in heap] for dep in dependencias) else "No ejecutable"
    print(f"Tarea con mayor prioridad: {nombre} (Prioridad: {prioridad}, Fecha de vencimiento: {fecha_vencimiento.strftime('%Y-%m-%d')}, Dependencias: {dep_str}, Estado: {estado})")

# Verifica si una tarea específica es ejecutable
def verificar_tarea_ejecutable(heap):
    while True:
        nombre_tarea = input("Nombre de la tarea a verificar: ").strip()
        if nombre_tarea:
            break
        print("El nombre de la tarea no puede estar vacío.")

    for _, _, nombre, dependencias in heap:
        if nombre == nombre_tarea:
            estado = "Ejecutable" if all(dep not in [n for _, _, n, _ in heap] for dep in dependencias) else "No ejecutable"
            print(f"La tarea '{nombre}' es: {estado}")
            return
    print(f"Tarea '{nombre_tarea}' no encontrada.")

def main():
    heap = cargar_tareas()  # Cargar tareas desde el archivo
    while True:
        opcion = menu()
        if opcion == "1":
            añadir_tarea(heap)
        elif opcion == "2":
            mostrar_tareas(heap)
        elif opcion == "3":
            completar_tarea(heap)
        elif opcion == "4":
            obtener_tarea_prioritaria(heap)
        elif opcion == "5":
            verificar_tarea_ejecutable(heap)
        elif opcion == "6":
            print("Saliendo del gestor de tareas.")
            guardar_tareas(heap)  # Guardar tareas antes de salir
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()
