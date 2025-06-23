SELECT
    rc.random AS qr_code,
    rc.id,
    rq.fecha,
    rq.det,
    do.nombres AS nombre_docente,
    asig.nombre AS nombre_asignatura,
    rc.id AS result_id,
    rc.senti1 AS feliz,
    rc.senti2 AS interesado,
    rc.senti3 AS motivado,
    rc.senti4 AS entusiasmado,
    rc.senti5 AS preocupado,
    rc.senti6 AS temeroso,
    rc.senti7 AS triste,
    rc.senti8 AS cansado,
    rc.UIDE,
    rq.numrandom,
    ROW_NUMBER() OVER (ORDER BY rq.fecha DESC) AS rn
FROM
    FinalProyecto.resultclass_limpio rc
right join  FinalProyecto.registroqr_limpio rq ON rc.random = rq.numrandom
right JOIN FinalProyecto.asignatura_limpia asig ON rq.id_asig = asig.idAsignatura
right JOIN FinalProyecto.docenteasignatura_limpio da ON da.idAsignatura = asig.idAsignatura
right JOIN FinalProyecto.docente_limpio do ON da.idDocente = do.idDocente
ORDER BY rq.fecha DESC;