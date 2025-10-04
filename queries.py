# queries.py

# Este archivo centraliza todas las consultas SQL para mantener el código organizado.
# Su propósito es servir las consultas de LECTURA para el dashboard de estadísticas.

# Consulta para los ingresos totales del año actual (KPI)
ingresos_anuales = """
    SELECT SUM(v.cantidad * p.precio) AS ingresos_totales
    FROM Ventas AS v JOIN Productos AS p ON v.ID_producto = p.ID
    WHERE YEAR(v.fecha) = 2025;
"""

# Consulta para la ciudad con más clientes (KPI y Gráfico)
clientes_por_ciudad = """
    SELECT ciudad, COUNT(ID) AS numero_de_clientes
    FROM Clientes GROUP BY ciudad ORDER BY numero_de_clientes DESC;
"""

# Consulta para el porcentaje de clientes por sexo (Gráfico)
clientes_por_sexo = """
    SELECT sexo, COUNT(ID) AS total
    FROM Clientes GROUP BY sexo;
"""

# Consulta para los productos más vendidos (KPI y Gráfico)
top_productos_vendidos = """
    SELECT 
        p.nombre, 
        SUM(v.cantidad) AS total_unidades_vendidas
    FROM Ventas AS v 
    JOIN Productos AS p ON v.ID_producto = p.ID
    GROUP BY p.nombre 
    ORDER BY total_unidades_vendidas DESC
    LIMIT 5;
"""

# Consulta para los ingresos por categoría (Gráfico)
ingresos_por_categoria = """
    SELECT 
        p.categoria, 
        SUM(v.cantidad * p.precio) as total_ventas
    FROM Ventas v 
    JOIN Productos p ON v.ID_producto = p.ID
    GROUP BY p.categoria 
    ORDER BY total_ventas DESC;
"""

# --- CONSULTAS PARA GESTIÓN DE CLIENTES (CRUD) ---
select_all_clientes = "SELECT * FROM Clientes ORDER BY ID ASC"

insert_cliente = """
    INSERT INTO Clientes (nombre, ciudad, edad, sexo) 
    VALUES (%s, %s, %s, %s)
"""

update_cliente = """
    UPDATE Clientes 
    SET nombre=%s, ciudad=%s, edad=%s, sexo=%s 
    WHERE ID=%s
"""

delete_cliente = "DELETE FROM Clientes WHERE ID = %s"

# --- CONSULTAS PARA GESTIÓN DE VENTAS ---

# Consulta para ver el registro de ventas con nombres de cliente y producto
select_all_ventas = """
    SELECT 
        v.ID,
        v.fecha,
        c.nombre AS nombre_cliente,
        p.nombre AS nombre_producto,
        v.cantidad,
        p.precio,
        (v.cantidad * p.precio) AS total_venta
    FROM Ventas AS v
    JOIN Clientes AS c ON v.ID_cliente = c.ID
    JOIN Productos AS p ON v.ID_producto = p.ID
    ORDER BY v.fecha DESC, v.ID DESC;
"""

insert_venta = """
    INSERT INTO Ventas (ID_cliente, ID_producto, cantidad, fecha)
    VALUES (%s, %s, %s, %s)
"""

delete_venta = "DELETE FROM Ventas WHERE ID = %s"

# --- CONSULTAS PARA ANÁLISIS DE TENDENCIAS ---

# Agrupa los ingresos totales por mes y año
ventas_mensuales = """
    SELECT
        DATE_FORMAT(fecha, '%Y-%m') AS anio_mes,
        SUM(cantidad * p.precio) AS ingresos_mensuales
    FROM Ventas AS v
    JOIN Productos AS p ON v.ID_producto = p.ID
    GROUP BY anio_mes
    ORDER BY anio_mes ASC;
"""

# Agrupa la cantidad de productos vendidos por categoría y por mes
ventas_categoria_por_mes = """
    SELECT
        DATE_FORMAT(fecha, '%Y-%m') AS anio_mes,
        p.categoria,
        SUM(v.cantidad) AS cantidad_vendida
    FROM Ventas AS v
    JOIN Productos AS p ON v.ID_producto = p.ID
    GROUP BY anio_mes, p.categoria
    ORDER BY anio_mes ASC, p.categoria ASC;
"""
# --- CONSULTAS PARA REPORTES ---

# Resumen de ventas agrupado por categoría de producto
resumen_ventas_por_categoria = """
    SELECT 
        p.categoria,
        COUNT(v.ID) AS numero_de_ventas,
        SUM(v.cantidad) AS total_unidades_vendidas,
        SUM(v.cantidad * p.precio) AS ingresos_totales
    FROM Ventas v 
    JOIN Productos p ON v.ID_producto = p.ID
    GROUP BY p.categoria
    ORDER BY ingresos_totales DESC;
"""
# Reporte de Clientes VIP: Top 10 clientes por total gastado
reporte_clientes_vip = """
    SELECT 
        c.nombre,
        c.ciudad,
        COUNT(v.ID) AS numero_de_compras,
        SUM(v.cantidad * p.precio) AS total_gastado
    FROM Clientes c
    JOIN Ventas v ON c.ID = v.ID_cliente
    JOIN Productos p ON v.ID_producto = p.ID
    GROUP BY c.ID, c.nombre, c.ciudad
    ORDER BY total_gastado DESC
    LIMIT 10;
"""

# Reporte de Productos Estancados: Productos sin ventas en los últimos 180 días
reporte_productos_estancados = f"""
    SELECT
        p.ID,
        p.nombre,
        p.categoria,
        p.precio
    FROM Productos p
    LEFT JOIN Ventas v ON p.ID = v.ID_producto AND v.fecha >= DATE_SUB(CURDATE(), INTERVAL 180 DAY)
    WHERE v.ID IS NULL
    ORDER BY p.nombre ASC;
"""
