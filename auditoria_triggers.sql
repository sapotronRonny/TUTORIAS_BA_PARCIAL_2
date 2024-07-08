
    CREATE TRIGGER audit_Roles_after_insert
    ON Roles
    AFTER INSERT
    AS
    BEGIN
        INSERT INTO auditoria (nombre_tabla, usuario_db, accion, descripcion_cambios)
        SELECT 'Roles', SYSTEM_USER, 'INSERT', (
            SELECT 'id_rol', inserted.id_rol, 'nombre_rol', inserted.nombre_rol
            FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
        )
        FROM inserted;
    END;
    


    CREATE TRIGGER audit_Roles_after_update
    ON Roles
    AFTER UPDATE
    AS
    BEGIN
        INSERT INTO auditoria (nombre_tabla, usuario_db, accion, descripcion_cambios)
        SELECT 'Roles', SYSTEM_USER, 'UPDATE', (
            SELECT 'id_rol', deleted.id_rol, 'id_rol', inserted.id_rol, 'nombre_rol', deleted.nombre_rol, 'nombre_rol', inserted.nombre_rol
            FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
        )
        FROM inserted
        INNER JOIN deleted ON inserted.id = deleted.id; -- Suponiendo que 'id' es la clave primaria
    END;
    


    CREATE TRIGGER audit_Roles_after_delete
    ON Roles
    AFTER DELETE
    AS
    BEGIN
        INSERT INTO auditoria (nombre_tabla, usuario_db, accion, descripcion_cambios)
        SELECT 'Roles', SYSTEM_USER, 'DELETE', (
            SELECT 'id_rol', deleted.id_rol, 'nombre_rol', deleted.nombre_rol
            FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
        )
        FROM deleted;
    END;
    

