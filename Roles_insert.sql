
    CREATE PROCEDURE Roles_insert(@p_id_rol int, @p_nombre_rol varchar)
    AS
    BEGIN
        INSERT INTO Roles (id_rol, nombre_rol) VALUES (@p_id_rol, @p_nombre_rol);
    END
    