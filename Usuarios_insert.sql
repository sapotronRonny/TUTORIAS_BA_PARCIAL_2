
    CREATE PROCEDURE Usuarios_insert(@p_id_usuario int, @p_nombre_usuario varchar, @p_contrase�a varchar, @p_correo_electronico varchar, @p_creado_en datetime, @p_actualizado_en datetime)
    AS
    BEGIN
        INSERT INTO Usuarios (id_usuario, nombre_usuario, contrase�a, correo_electronico, creado_en, actualizado_en) VALUES (@p_id_usuario, @p_nombre_usuario, @p_contrase�a, @p_correo_electronico, @p_creado_en, @p_actualizado_en);
    END
    