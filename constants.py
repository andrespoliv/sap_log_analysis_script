MESSAGE_BY_LOG_GROUP = {
    "role_assignment": {
            "0": "Rol creado o modificado por última vez por un usuario con altos privilegios",
            "1": "Rol creado o modificado por última vez por un usuario bloqueado o con contraseña inicial",
            "2": "Rol que se deriva de rol maestro con altos privilegios",
            "3": "Rol creado o modificado en hora estadísticamente atípica"
        },
    "user_change": {
            "0": "Bloqueo de usuario en hora estadísticamente atípica",
            "1": "Desbloqueo de usuarios bloqueados por administrador (64) o administrador central CUA (32)",
            "2": "Actividad realizada por usuario con más de un año sin iniciar sesión",
            "3": "Actividad realizada por usuario con validación vencida",
            "4": "Usuario vinculado a posible ataque de fuerza bruta"
        },
    "datalog_table": {
            "0": "Modificación de tabla relevante en hora estadísticamente atípica"
        },
    "user_logon": {
            "0": "Usuario con más de un año sin iniciar sesión",
            "1": "Usuario con validación vencida",
            "2": "Usuario con algoritmo de hash inseguro ({x-issha, 1024} : SAP CODVN H (PWDSALTEDHASH) iSSHA-1)",
	        "3": "Usuario que requieren cambio de contraseña (estados 1, 2 y 3)",
            "4": "Usuario bloqueado por administrador"
    }
}

USER_CHANGE_MANDATORY_LENGTH = 12