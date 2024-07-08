
    CREATE PROCEDURE Usuarios_insert(@p_id_usuario int, @p_nombre_usuario varchar, @p_contraseña varchar, @p_correo_electronico varchar, @p_creado_en datetime, @p_actualizado_en datetime)
    AS
    BEGIN
        INSERT INTO Usuarios (id_usuario, nombre_usuario, contraseña, correo_electronico, creado_en, actualizado_en) VALUES (@p_id_usuario, @p_nombre_usuario, @p_contraseña, @p_correo_electronico, @p_creado_en, @p_actualizado_en);
    END
    