

-- numero de registros de la tabla TablaAnalisisJoin  = 13690
select count(*)  from FinalProyecto.TablasAnalisisJoin

-- numero de docentes unicos en la tabla TablasAnalisisJoin
select count(*),nombre_docente  from FinalProyecto.TablasAnalisisJoin group by nombre_docente  order by count(*)desc

-- numero de docentes materias y qrs de forma unica de cada anio
SELECT
  YEAR(fecha) AS Anio,
  COUNT(DISTINCT nombre_asignatura) AS TotalMaterias,
  COUNT(DISTINCT nombre_docente) AS TotalDocentes,
  COUNT(DISTINCT qr_code) AS qrs
FROM FinalProyecto.TablasAnalisisJoin
WHERE YEAR(fecha) BETWEEN 2020 AND 2025
GROUP BY YEAR(fecha)
ORDER BY Anio;

-- Nombres de docentes y asignaturas
SELECT nombre_asignatura,nombre_docente,count(*)
FROM  FinalProyecto.TablasAnalisisJoin
group by nombre_asignatura, nombre_docente


-- numero de asiganaturas unicos en la tabla TablasAnalisisJoin
select count(*),nombre_asignatura  from FinalProyecto.TablasAnalisisJoin group by nombre_asignatura order by count(*)desc

-- qr materia profesor donde no exista el 1 en los sentiminetos osea q no habido calificacion
SELECT qr_code, nombre_asignatura, nombre_docente, fecha
FROM FinalProyecto.TablasAnalisisJoin
WHERE feliz = 0
  AND interesado = 0
  AND motivado = 0
  AND entusiasmado = 0
  AND preocupado = 0
  AND temeroso = 0
  AND triste = 0
  AND cansado = 0;

-- Total de registros sin calificación por materia y docente
SELECT nombre_asignatura, nombre_docente, COUNT(*) AS sin_calificacion
FROM FinalProyecto.TablasAnalisisJoin
WHERE feliz = 0
  AND interesado = 0
  AND motivado = 0
  AND entusiasmado = 0
  AND preocupado = 0
  AND temeroso = 0
  AND triste = 0
  AND cansado = 0
GROUP BY nombre_asignatura, nombre_docente
ORDER BY sin_calificacion DESC;

-- Top 10 docentes con más clases registradas
SELECT nombre_docente, COUNT(DISTINCT qr_code) AS total_clases
FROM FinalProyecto.TablasAnalisisJoin
GROUP BY nombre_docente
ORDER BY total_clases DESC
LIMIT 10;

-- Top 10 materias con más evaluaciones
SELECT nombre_asignatura, COUNT(*) AS total_registros
FROM FinalProyecto.TablasAnalisisJoin
GROUP BY nombre_asignatura
ORDER BY total_registros DESC
LIMIT 10;

-- Distribución anual de emociones (ejemplo: felicidad)
SELECT YEAR(fecha) AS Anio, SUM(feliz) AS total_felicidad, SUM(interesado)   AS total_interesado,
  SUM(motivado)     AS total_motivado
FROM FinalProyecto.TablasAnalisisJoin
GROUP BY YEAR(fecha)
ORDER BY Anio;

-- Distribución anual de emociones (ejemplo: triste)
SELECT YEAR(fecha) AS Anio, SUM(preocupado) AS total_preocupado, SUM(temeroso)   AS total_temeroso,
  SUM(triste)     AS total_triste,SUM(cansado) AS total_cansado
FROM FinalProyecto.TablasAnalisisJoin
GROUP BY YEAR(fecha)
ORDER BY Anio;

-- Distribución anual de emociones  positivas vs negativas
    SELECT
    YEAR(fecha) AS Anio,
    -- Suma de emociones positivas
    SUM(feliz + interesado + motivado) AS total_emociones_positivas,
    -- Suma de emociones negativas
    SUM(preocupado + temeroso + triste + cansado) AS total_emociones_negativas
FROM
    FinalProyecto.TablasAnalisisJoin
GROUP BY
    YEAR(fecha)
ORDER BY
    Anio;
--  Cantidad de emociones activadas por clase
SELECT
  qr_code,
  nombre_docente,
  nombre_asignatura,
  fecha,
  (feliz + interesado + motivado + entusiasmado +
   preocupado + temeroso + triste + cansado) AS total_emociones
FROM FinalProyecto.TablasAnalisisJoin
ORDER BY total_emociones DESC
LIMIT 50;

-- TotalDeClasesUnicasDictadasPorCadadocentes en todo el peridodo por qr
SELECT
  nombre_docente,nombre_asignatura,
  COUNT(DISTINCT qr_code) AS clases_unicas
FROM FinalProyecto.TablasAnalisisJoin
GROUP BY nombre_docente,nombre_asignatura
ORDER BY clases_unicas DESC;

-- Top 5 docentes con más emociones positivas registradas sql
SELECT nombre_docente,nombre_asignatura,
       SUM(feliz + interesado + motivado + entusiasmado) AS emociones_positivas
FROM FinalProyecto.TablasAnalisisJoin
GROUP BY nombre_docente,nombre_asignatura
ORDER BY emociones_positivas DESC
LIMIT 5;

-- Promedio de emociones por asignatura
SELECT nombre_asignatura,
       AVG(feliz) AS avg_feliz,
       AVG(interesado) AS avg_interesado,
       AVG(motivado) AS avg_motivado,
       AVG(entusiasmado) AS avg_entusiasmado,
       AVG(preocupado) AS avg_preocupado,
       AVG(temeroso) AS avg_temeroso,
       AVG(triste) AS avg_triste,
       AVG(cansado) AS avg_cansado
FROM FinalProyecto.TablasAnalisisJoin
GROUP BY nombre_asignatura;

-- que materias generan mas emociones
    SELECT
  nombre_asignatura,
  SUM(feliz)        AS total_feliz,
  SUM(triste)       AS total_triste,
  SUM(entusiasmado) AS total_entusiasmado,
  SUM(preocupado)   AS total_preocupado,
  SUM(temeroso)     AS total_temeroso,
  SUM(cansado)      AS total_cansado,
  SUM(interesado)   AS total_interesado,
  SUM(motivado)     AS total_motivado
FROM FinalProyecto.TablasAnalisisJoin
GROUP BY nombre_asignatura
ORDER BY total_feliz DESC;

-- simulando q cada qrcode calificado lo asimulamos con un estudiante
SELECT qr_code, COUNT(*) AS total_estudiantes,COUNT(*) AS vecesCalfico,nombre_asignatura
FROM FinalProyecto.TablasAnalisisJoin
GROUP BY qr_code,nombre_asignatura
ORDER BY total_estudiantes DESC;


-- Consulta: Total de calificaciones (estudiantes) por año
SELECT
  YEAR(fecha) AS anio,
  COUNT(*) AS total_calificaciones
FROM FinalProyecto.TablasAnalisisJoin
GROUP BY YEAR(fecha)
ORDER BY anio;

-- Consulta: Estudiantes únicos (qr_code) por año
SELECT
  YEAR(fecha) AS anio,
  COUNT(DISTINCT qr_code) AS estudiantes_unicos
FROM FinalProyecto.TablasAnalisisJoin
GROUP BY YEAR(fecha)
ORDER BY anio;


-- Sesiones (qr_code) con más emociones positivas
SELECT qr_code,
       nombre_asignatura,
       SUM(feliz + interesado + motivado + entusiasmado) AS emociones_positivas
FROM  FinalProyecto.TablasAnalisisJoin
GROUP BY qr_code,nombre_asignatura
ORDER BY emociones_positivas DESC
LIMIT 10;

-- Promedio de emociones por docente
SELECT nombre_docente,
       AVG(feliz) AS feliz,
       AVG(triste) AS triste,
       AVG(preocupado) AS preocupado,
       AVG(cansado) AS cansado
FROM FinalProyecto.TablasAnalisisJoin

GROUP BY nombre_docente;

--  ¿Qué docentes usaron más el sistema?
SELECT nombre_docente, COUNT(DISTINCT qr_code) AS ClasesRegistradas
FROM  FinalProyecto.TablasAnalisisJoin
GROUP BY nombre_docente
ORDER BY ClasesRegistradas DESC;

-- Top 5 materias con más clases distintas por año (según QR único)
SELECT nombre_asignatura, COUNT(DISTINCT qr_code) AS clases_distintas
FROM FinalProyecto.TablasAnalisisJoin
WHERE EXTRACT(YEAR FROM fecha) = 2025
  AND qr_code IS NOT NULL
GROUP BY nombre_asignatura
ORDER BY clases_distintas DESC
LIMIT 5;



-- TENDENCIA POR MES
SELECT
  MONTH(fecha) AS mes,
  SUM(
    COALESCE(feliz, 0) +
    COALESCE(interesado, 0) +
    COALESCE(motivado, 0) +
    COALESCE(entusiasmado, 0)
  ) AS sentimientos_positivos,
  SUM(
    COALESCE(preocupado, 0) +
    COALESCE(temeroso, 0) +
    COALESCE(triste, 0) +
    COALESCE(cansado, 0)
  ) AS sentimientos_negativos
FROM FinalProyecto.TablasAnalisisJoin
WHERE YEAR(fecha) = 2024
GROUP BY MONTH(fecha)
ORDER BY mes;


-- Top 10 materias con más calificaciones y emociones por anio filtrado
SELECT
  nombre_asignatura,

  COUNT(*) AS veces_calificada,
  SUM(COALESCE(feliz, 0) + COALESCE(interesado, 0) + COALESCE(motivado, 0) + COALESCE(entusiasmado, 0)) AS sentimientos_positivos,
  SUM(COALESCE(preocupado, 0) + COALESCE(temeroso, 0) + COALESCE(triste, 0) + COALESCE(cansado, 0)) AS sentimientos_negativos
FROM Analisis.TablaAnalisis
WHERE YEAR(fecha) = 2025
GROUP BY nombre_asignatura
ORDER BY veces_calificada DESC
LIMIT 10;

-- Top 10 materias CON PROFESORES con más calificaciones y emociones por anio filtrado

SELECT
  nombre_asignatura,
  nombre_docente,
  COUNT(*) AS veces_calificada,
  SUM(COALESCE(feliz, 0) + COALESCE(interesado, 0) + COALESCE(motivado, 0) + COALESCE(entusiasmado, 0)) AS sentimientos_positivos,
  SUM(COALESCE(preocupado, 0) + COALESCE(temeroso, 0) + COALESCE(triste, 0) + COALESCE(cansado, 0)) AS sentimientos_negativos
FROM Analisis.TablaAnalisis
WHERE YEAR(fecha) = 2025
GROUP BY nombre_asignatura, nombre_docente
ORDER BY veces_calificada DESC
LIMIT 10;
