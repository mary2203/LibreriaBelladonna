from conexion import conectar
from datetime import datetime

def pedir_rango_fechas():

    print("\n")
    print("¡Ingrese el rango de fechas!")
    print("Favor de usar el formato: AAAA-MM-DD 𐔌՞ ܸ.ˬ.ܸ՞𐦯")

    while True:
        fecha_inicio = input("Fecha inicial: ")
        fecha_fin = input("Fecha final: ")

        try:
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

            if fin < inicio:
                print("\n")
                print("La fecha final no puede ser menor que la fecha inicial (◞‸◟,)")
                continue

            return fecha_inicio, fecha_fin

        except ValueError:
            print("\n")
            print("Formato de fecha incorrecto (◞‸◟,)")

def mostrar_catalogo():
    conexion = conectar()

    if conexion:
        cursor = conexion.cursor()

        consulta = """
            SELECT
                producto_id,
                titulo,
                autor,
                precio,
                existencia
            FROM productos
            WHERE activo = TRUE
            ORDER BY producto_id ASC
        """

        cursor.execute(consulta)
        libros = cursor.fetchall()

        print("\n")
        print("──────── ୨୧ ────────")
        print(" Catálogo de libros")
        print("──────── ୨୧ ────────")
        print("\n")

        for libro in libros:
            producto_id, titulo, autor, precio, existencia = libro

            print(
                f"{producto_id}. {titulo} - {autor} "
                f"| Q{precio:.2f} | Existencia: {existencia}"
            )

        cursor.close()
        conexion.close()

def mostrar_clientes():
    conexion = conectar()

    if conexion:
        cursor = conexion.cursor()

        consulta = """
            SELECT
                c.cliente_id,
                CONCAT(c.nombre, ' ', c.apellido) AS cliente,
                c.nit,
                c.correo,
                m.municipio
            FROM clientes c
            INNER JOIN municipios m
                ON c.municipio_id = m.municipio_id
            WHERE c.activo = TRUE
            ORDER BY c.cliente_id ASC;
        """

        cursor.execute(consulta)
        clientes = cursor.fetchall()

        print("\n")
        print("──────── ୨୧ ────────")
        print("     Clientes")
        print("──────── ୨୧ ────────")
        print("\n")

        for cliente in clientes:
            cliente_id, nombre, nit, correo, municipio = cliente

            print(
                f"{cliente_id}. {nombre} "
                f"| NIT: {nit} "
                f"| {correo} "
                f"| {municipio}"
            )

        cursor.close()
        conexion.close()

def mostrar_empleados():
    conexion = conectar()

    if conexion:
        cursor = conexion.cursor()

        consulta = """
            SELECT
                empleado_id,
                CONCAT(nombre, ' ', apellido) AS empleado,
                puesto
            FROM empleados
            WHERE activo = TRUE
            ORDER BY empleado_id ASC;
        """

        cursor.execute(consulta)
        empleados = cursor.fetchall()

        print("\n")
        print("──────── ୨୧ ────────")
        print("     Empleados")
        print("──────── ୨୧ ────────")
        print("\n")

        for empleado in empleados:
            empleado_id, nombre, puesto = empleado

            print(
                f"{empleado_id}. {nombre} | {puesto}"
            )

        cursor.close()
        conexion.close()

def registrar_venta():
    conexion = conectar()

    if not conexion:
        return

    cursor = conexion.cursor()

    try:
        print("\n")
        print("──────── ୨୧ ────────")
        print("   Registrar venta")
        print("──────── ୨୧ ────────")

        cursor.execute("""
            SELECT cliente_id, nombre, apellido
            FROM clientes
            WHERE activo = TRUE
            ORDER BY cliente_id ASC;
        """)

        clientes = cursor.fetchall()

        print("\n")
        print("──────── ୨୧ ────────")
        print("Clientes disponibles")
        print("──────── ୨୧ ────────")

        for cliente in clientes:
            print(f"{cliente[0]}. {cliente[1]} {cliente[2]}")

        cliente_id = int(input("\nSeleccione el ID del cliente: "))

        cursor.execute("""
            SELECT cliente_id
            FROM clientes
            WHERE cliente_id = %s
              AND activo = TRUE;
        """, (cliente_id,))

        if cursor.fetchone() is None:
            print("\n")
            print("Cliente no encontrado (◞‸◟,)")
            return

        cursor.execute("""
            SELECT empleado_id, nombre, apellido
            FROM empleados
            WHERE activo = TRUE
            ORDER BY empleado_id ASC;
        """)

        empleados = cursor.fetchall()

        print("\n")
        print("──────── ୨୧ ────────")
        print("Empleados disponibles")
        print("──────── ୨୧ ────────")

        for empleado in empleados:
            print(f"{empleado[0]}. {empleado[1]} {empleado[2]}")

        empleado_id = int(input("\nSeleccione el ID del empleado: "))

        cursor.execute("""
            SELECT empleado_id
            FROM empleados
            WHERE empleado_id = %s
              AND activo = TRUE;
        """, (empleado_id,))

        if cursor.fetchone() is None:
            print("\n")
            print("Empleado no encontrado (◞‸◟,)")
            return

        carrito = []

        while True:

            cursor.execute("""
                SELECT
                    producto_id,
                    titulo,
                    autor,
                    precio,
                    existencia
                FROM productos
                WHERE activo = TRUE
                ORDER BY producto_id ASC;
            """)

            libros = cursor.fetchall()

            print("\n")
            print("──────── ୨୧ ────────")
            print(" Libros disponibles")
            print("──────── ୨୧ ────────")
            print()

            for libro in libros:
                print(
                    f"{libro[0]}. {libro[1]} - {libro[2]} "
                    f"| Q{libro[3]:.2f} | Existencia: {libro[4]}"
                )

            producto_id = int(
                input("\nIngrese ID del libro ó 0 para terminar: ")
            )

            if producto_id == 0:
                break

            cursor.execute("""
                SELECT titulo, precio, existencia
                FROM productos
                WHERE producto_id = %s
                  AND activo = TRUE;
            """, (producto_id,))

            producto = cursor.fetchone()

            if producto is None:
                print("\n")
                print("Libro no encontrado (◞‸◟,)")
                continue

            titulo, precio, existencia = producto

            try:
                cantidad = int(input("Cantidad: "))

                if cantidad <= 0:
                    print("\n")
                    print("La cantidad debe ser mayor a cero (◞‸◟,)")
                    continue

            except ValueError:
                print("\n")
                print("Debe ingresar un número (◞‸◟,)")
                continue

            cantidad_previa = 0

            for item in carrito:
                if item["producto_id"] == producto_id:
                    cantidad_previa = item["cantidad"]

            if cantidad + cantidad_previa > existencia:
                print("\n")
                print("No hay suficiente existencia (◞‸◟,)")
                print(f"Disponibles: {existencia}")
                continue

            encontrado = False

            for item in carrito:
                if item["producto_id"] == producto_id:
                    item["cantidad"] += cantidad
                    encontrado = True

            if not encontrado:
                carrito.append({
                    "producto_id": producto_id,
                    "titulo": titulo,
                    "precio": precio,
                    "cantidad": cantidad
                })

            print("\n")
            print(f"{titulo} agregado a la venta ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧")

        if not carrito:
            print("\n")
            print("No se agregaron libros, venta cancelada (◞‸◟,)")
            return

        print("\n")
        print("──────── ୨୧ ────────")
        print(" Resumen de la venta")
        print("──────── ୨୧ ────────")
        print()

        total = 0

        for item in carrito:
            subtotal = item["cantidad"] * item["precio"]
            total += subtotal

            print(
                f"{item['titulo']} "
                f"x{item['cantidad']} "
                f"| Q{subtotal:.2f}"
            )

        print("\n")
        print(f"TOTAL: Q{total:.2f}")

        print("\n")
        confirmar = input("¿Desea confirmar la venta? (s/n): ").lower()

        if confirmar != "s":
            print("\n")
            print("Venta cancelada (◞‸◟,)")
            return

        cursor.execute("""
            INSERT INTO ventas
            (cliente_id, empleado_id, fecha_venta)
            VALUES (%s, %s, NOW());
        """, (cliente_id, empleado_id))

        venta_id = cursor.lastrowid

        for item in carrito:

            cursor.execute("""
                INSERT INTO detalle_venta
                (venta_id, producto_id, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s);
            """, (
                venta_id,
                item["producto_id"],
                item["cantidad"],
                item["precio"]
            ))

            cursor.execute("""
                UPDATE productos
                SET existencia = existencia - %s
                WHERE producto_id = %s;
            """, (
                item["cantidad"],
                item["producto_id"]
            ))

        conexion.commit()

        print("\n")
        print("Venta registrada correctamente ദ്ദി(˵ •̀ ᴗ - ˵ ) ✧")
        print(f"Número de venta: {venta_id}")
        print(f"Total: Q{total:.2f}")

    except ValueError:
        conexion.rollback()
        print("\n")
        print("Debe ingresar valores numéricos válidos (◞‸◟,)")

    except Exception as error:
        conexion.rollback()
        print("\n")
        print(f"Ocurrió un error (◞‸◟,): {error}")

    finally:
        cursor.close()
        conexion.close()

def consultar_ventas():

    fecha_inicio, fecha_fin = pedir_rango_fechas()

    conexion = conectar()

    if not conexion:
        return

    cursor = conexion.cursor()

    consulta = """
        SELECT
            v.venta_id,
            v.fecha_venta,
            CONCAT(c.nombre, ' ', c.apellido) AS cliente,
            CONCAT(e.nombre, ' ', e.apellido) AS empleado,
            p.titulo,
            dv.cantidad,
            dv.precio_unitario,
            (dv.cantidad * dv.precio_unitario) AS subtotal

        FROM ventas v

        INNER JOIN clientes c
            ON v.cliente_id = c.cliente_id

        INNER JOIN empleados e
            ON v.empleado_id = e.empleado_id

        INNER JOIN detalle_venta dv
            ON v.venta_id = dv.venta_id

        INNER JOIN productos p
            ON dv.producto_id = p.producto_id

        WHERE v.fecha_venta >= %s
          AND v.fecha_venta < DATE_ADD(%s, INTERVAL 1 DAY)

        ORDER BY v.venta_id ASC, dv.detalle_id ASC;
    """

    cursor.execute(consulta, (fecha_inicio, fecha_fin))

    resultados = cursor.fetchall()

    if not resultados:
        print("\n")
        print("No existen ventas dentro de ese rango (◞‸◟,)")
        cursor.close()
        conexion.close()
        return

    print("\n")
    print("──────── ୨୧ ────────")
    print("  Ventas registradas")
    print("──────── ୨୧ ────────")

    venta_actual = None
    total_venta = 0

    for fila in resultados:

        venta_id, fecha, cliente, empleado, libro, cantidad, precio, subtotal = fila

        if venta_actual != venta_id:

            if venta_actual is not None:
                print(f"\nTOTAL: Q{total_venta:.2f}")
                print("-" * 60)

            venta_actual = venta_id
            total_venta = 0

            print(f"\nVenta #{venta_id}")
            print(f"Fecha: {fecha.strftime('%d/%m/%Y %H:%M')}")
            print(f"Cliente: {cliente}")
            print(f"Atendido por: {empleado}")
            print()

        print(
            f"{libro} | "
            f"{cantidad} x Q{precio:.2f} "
            f"= Q{subtotal:.2f}"
        )

        total_venta += subtotal

    print(f"\nTOTAL: Q{total_venta:.2f}")
    print("-" * 60)

    cursor.close()
    conexion.close()

def ventas_cliente_producto():

    fecha_inicio, fecha_fin = pedir_rango_fechas()

    conexion = conectar()

    if not conexion:
        return

    cursor = conexion.cursor()

    consulta = """
        SELECT
            CONCAT(c.nombre, ' ', c.apellido) AS cliente,
            p.titulo,
            SUM(dv.cantidad) AS cantidad_vendida,
            SUM(dv.cantidad * dv.precio_unitario) AS total_vendido

        FROM ventas v

        INNER JOIN clientes c
            ON v.cliente_id = c.cliente_id

        INNER JOIN detalle_venta dv
            ON v.venta_id = dv.venta_id

        INNER JOIN productos p
            ON dv.producto_id = p.producto_id

        WHERE v.fecha_venta >= %s
          AND v.fecha_venta < DATE_ADD(%s, INTERVAL 1 DAY)

        GROUP BY
            c.cliente_id,
            c.nombre,
            c.apellido,
            p.producto_id,
            p.titulo

        ORDER BY total_vendido DESC;
    """

    cursor.execute(consulta, (fecha_inicio, fecha_fin))

    resultados = cursor.fetchall()

    print("\n")
    print("    ──────── ୨୧ ────────")
    print("Ventas por cliente y producto")
    print("    ──────── ୨୧ ────────")
    print()

    if not resultados:
        print("No existen ventas en ese rango (◞‸◟,)")

    else:
        for cliente, producto, cantidad, total in resultados:

            print(
                f"{cliente} | "
                f"{producto} | "
                f"Cantidad: {cantidad} | "
                f"Total: Q{total:.2f}"
            )

    cursor.close()
    conexion.close()

def kpi_total_vendido():

    fecha_inicio, fecha_fin = pedir_rango_fechas()

    conexion = conectar()

    if not conexion:
        return

    cursor = conexion.cursor()

    consulta = """
        SELECT
            COALESCE(
                SUM(dv.cantidad * dv.precio_unitario),
                0
            )

        FROM ventas v

        INNER JOIN detalle_venta dv
            ON v.venta_id = dv.venta_id

        WHERE v.fecha_venta >= %s
          AND v.fecha_venta < DATE_ADD(%s, INTERVAL 1 DAY);
    """

    cursor.execute(consulta, (fecha_inicio, fecha_fin))

    total = cursor.fetchone()[0]

    print("\n")
    print("──────── ୨୧ ────────")
    print("    Total vendido")
    print("──────── ୨୧ ────────")
    print()

    print(f"Total vendido: Q{total:.2f}")

    cursor.close()
    conexion.close()

def kpi_mejor_cliente():

    fecha_inicio, fecha_fin = pedir_rango_fechas()

    conexion = conectar()

    if not conexion:
        return

    cursor = conexion.cursor()

    consulta = """
        SELECT
            CONCAT(c.nombre, ' ', c.apellido) AS cliente,
            SUM(dv.cantidad) AS libros_comprados,
            SUM(dv.cantidad * dv.precio_unitario) AS total_comprado

        FROM clientes c

        INNER JOIN ventas v
            ON c.cliente_id = v.cliente_id

        INNER JOIN detalle_venta dv
            ON v.venta_id = dv.venta_id

        WHERE v.fecha_venta >= %s
          AND v.fecha_venta < DATE_ADD(%s, INTERVAL 1 DAY)

        GROUP BY
            c.cliente_id,
            c.nombre,
            c.apellido

        ORDER BY total_comprado DESC

        LIMIT 1;
    """

    cursor.execute(consulta, (fecha_inicio, fecha_fin))

    resultado = cursor.fetchone()

    print("\n")
    print("──────── ୨୧ ────────")
    print("     Mejor cliente")
    print("──────── ୨୧ ────────")
    print()

    if resultado:

        cliente, libros, total = resultado

        print(f"Cliente: {cliente}")
        print(f"Libros comprados: {libros}")
        print(f"Total comprado: Q{total:.2f}")

    else:
        print("No existen ventas en ese rango (◞‸◟,)")

    cursor.close()
    conexion.close()

def kpi_libro_mas_vendido():

    fecha_inicio, fecha_fin = pedir_rango_fechas()

    conexion = conectar()

    if not conexion:
        return

    cursor = conexion.cursor()

    consulta = """
        SELECT
            p.titulo,
            p.autor,
            SUM(dv.cantidad) AS unidades,
            SUM(dv.cantidad * dv.precio_unitario) AS ingresos

        FROM productos p

        INNER JOIN detalle_venta dv
            ON p.producto_id = dv.producto_id

        INNER JOIN ventas v
            ON dv.venta_id = v.venta_id

        WHERE v.fecha_venta >= %s
          AND v.fecha_venta < DATE_ADD(%s, INTERVAL 1 DAY)

        GROUP BY
            p.producto_id,
            p.titulo,
            p.autor

        ORDER BY unidades DESC, ingresos DESC

        LIMIT 1;
    """

    cursor.execute(consulta, (fecha_inicio, fecha_fin))

    resultado = cursor.fetchone()

    print("\n")
    print("──────── ୨୧ ────────")
    print("  Libro más vendido")
    print("──────── ୨୧ ────────")
    print()

    if resultado:

        titulo, autor, unidades, ingresos = resultado

        print(f"Libro: {titulo}")
        print(f"Autor: {autor}")
        print(f"Unidades vendidas: {unidades}")
        print(f"Ingresos generados: Q{ingresos:.2f}")

    else:
        print("No existen ventas en ese rango (◞‸◟,)")

    cursor.close()
    conexion.close()

def kpi_mejor_empleado():

    fecha_inicio, fecha_fin = pedir_rango_fechas()

    conexion = conectar()

    if not conexion:
        return

    cursor = conexion.cursor()

    consulta = """
        SELECT
            CONCAT(e.nombre, ' ', e.apellido) AS empleado,
            e.puesto,
            COUNT(DISTINCT v.venta_id) AS ventas_atendidas,
            SUM(dv.cantidad) AS libros_vendidos,
            SUM(dv.cantidad * dv.precio_unitario) AS total_vendido

        FROM empleados e

        INNER JOIN ventas v
            ON e.empleado_id = v.empleado_id

        INNER JOIN detalle_venta dv
            ON v.venta_id = dv.venta_id

        WHERE v.fecha_venta >= %s
          AND v.fecha_venta < DATE_ADD(%s, INTERVAL 1 DAY)

        GROUP BY
            e.empleado_id,
            e.nombre,
            e.apellido,
            e.puesto

        ORDER BY total_vendido DESC

        LIMIT 1;
    """

    cursor.execute(consulta, (fecha_inicio, fecha_fin))

    resultado = cursor.fetchone()

    print("\n")
    print("──────── ୨୧ ────────")
    print(" Empleado destacado")
    print("──────── ୨୧ ────────")
    print()

    if resultado:

        empleado, puesto, ventas, libros, total = resultado

        print(f"Empleado: {empleado}")
        print(f"Puesto: {puesto}")
        print(f"Ventas atendidas: {ventas}")
        print(f"Libros vendidos: {libros}")
        print(f"Total vendido: Q{total:.2f}")

    else:
        print("No existen ventas en ese rango (◞‸◟,)")

    cursor.close()
    conexion.close()

def kpi_categorias():

    fecha_inicio, fecha_fin = pedir_rango_fechas()

    conexion = conectar()

    if not conexion:
        return

    cursor = conexion.cursor()

    consulta = """
        SELECT
            cat.nombre,
            SUM(dv.cantidad) AS libros_vendidos,
            SUM(dv.cantidad * dv.precio_unitario) AS total_vendido

        FROM categorias cat

        INNER JOIN productos p
            ON cat.categoria_id = p.categoria_id

        INNER JOIN detalle_venta dv
            ON p.producto_id = dv.producto_id

        INNER JOIN ventas v
            ON dv.venta_id = v.venta_id

        WHERE v.fecha_venta >= %s
          AND v.fecha_venta < DATE_ADD(%s, INTERVAL 1 DAY)

        GROUP BY
            cat.categoria_id,
            cat.nombre

        ORDER BY total_vendido DESC;
    """

    cursor.execute(consulta, (fecha_inicio, fecha_fin))

    resultados = cursor.fetchall()

    print("\n")
    print(" ──────── ୨୧ ────────")
    print("Categorías más vendidas")
    print(" ──────── ୨୧ ────────")
    print()

    if not resultados:
        print("No existen ventas en ese rango (◞‸◟,)")

    else:

        posicion = 1

        for categoria, libros, total in resultados:

            print(
                f"{posicion}. {categoria} "
                f"| Libros: {libros} "
                f"| Total: Q{total:.2f}"
            )

            posicion += 1

    cursor.close()
    conexion.close()

def menu_kpis():
    while True:

        print("\n")    
        print("──────── ୨୧ ────────")
        print("        KPIs")
        print("──────── ୨୧ ────────")
        print("\n")
        print("1. Total vendido")
        print("2. Cliente que más compró")
        print("3. Libro más vendido")
        print("4. Empleado con más ventas")
        print("5. Categorías más vendidas")

        print("\n")
        print("0. Volver al menú principal (๑•᎑•๑)")

        print("\n")
        opcion = input("Seleccione una opción (˶ᵔ ᵕ ᵔ˶): ")

        if opcion == "1":
            kpi_total_vendido()

        elif opcion == "2":
            kpi_mejor_cliente()

        elif opcion == "3":
            kpi_libro_mas_vendido()

        elif opcion == "4":
            kpi_mejor_empleado()

        elif opcion == "5":
            kpi_categorias()

        elif opcion == "0":
            break

        else:
            print("\n")
            print("Opción no válida (◞‸◟,) intente de nuevo")

def mostrar_menu():
    while True:

        print("\n")
        print("──────── ୨୧ ────────")
        print("    Bienvenido a")
        print("Librería Belladonna ❀")
        print("──────── ୨୧ ────────")
        print("\n")
        print("1. Ver catálogo de libros")
        print("2. Ver clientes")
        print("3. Ver empleados")
        print("4. Registrar venta")
        print("5. Consultar ventas")
        print("6. Ventas por cliente y producto")
        print("7. KPIs")
        print("\n")
        print("0. Salir")

        opcion = input("\nSeleccione una opción (˶ᵔ ᵕ ᵔ˶): ")

        if opcion == "1":
            mostrar_catalogo()

        elif opcion == "2":
            mostrar_clientes()

        elif opcion == "3":
            mostrar_empleados()

        elif opcion == "4":
            registrar_venta()

        elif opcion == "5":
            consultar_ventas()

        elif opcion == "6":
            ventas_cliente_producto()

        elif opcion == "7":
            menu_kpis()

        elif opcion == "0":
            print("\n¡Gracias por utilizar Librería Belladonna! Vuelva pronto („• ֊ •„)੭")
            break

        else:
            print("\nOpción no válida (◞‸◟,) intente de nuevo")

mostrar_menu()