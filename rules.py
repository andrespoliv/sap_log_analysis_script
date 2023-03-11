from constants import MESSAGE_BY_LOG_GROUP, USER_CHANGE_MANDATORY_LENGTH
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np

def parse_time(time):
    result = None
    try:
        result = datetime.strptime(time, '%H:%M:%S')
    except Exception as e:
        print(f"Parsing date failed: {e}")
    return result

def input_file_reading(filename):
    result = []
    
    try:
        file = open(filename, "r", encoding="utf8")
        for line in file:
            line = sanitize_text(line)
            result.append(line)
            
        file.close()
    except Exception as e:
        print(f"Input file reading failed: {e}")
    return result

def sanitize_text(text):
    result = text.replace("\n","").replace("\t", "").strip()
    
    return result

# Rol creado o modificado por última vez por un usuario con altos privilegios
def role_assignment_rule_zero(data, rule_object):   
    result = []
    columns = data[0]
    data = data[1:]
    one_year_ago = (datetime.now() - relativedelta(years=1)).strftime("%Y-%m-%d")
    high_privilege_users_filename = "relevant_usernames.txt"
    high_privilege_users = input_file_reading(high_privilege_users_filename)
    
    original_data_frame = pd.DataFrame(data, columns=columns)
    temporary_data_frame = pd.DataFrame(data, columns=columns)
    
    temporary_data_frame["CHANGE_DAT"] = pd.to_datetime(temporary_data_frame["CHANGE_DAT"], errors='coerce')
    temporary_data_frame["CREATE_DAT"] = pd.to_datetime(temporary_data_frame["CREATE_DAT"], errors='coerce')
    
    outliers_change_usr = original_data_frame[((temporary_data_frame["CHANGE_USR"].isin(high_privilege_users)) & (temporary_data_frame["CHANGE_DAT"] > one_year_ago))]
    outliers_create_usr = original_data_frame[((temporary_data_frame["CREATE_USR"].isin(high_privilege_users)) & (temporary_data_frame["CREATE_DAT"] > one_year_ago))]
    result = outliers_change_usr.values.tolist() + outliers_create_usr.values.tolist()
    
    for line in result:
        remark = MESSAGE_BY_LOG_GROUP[rule_object["group"]][rule_object["rule"]]
        line[len(line) - 1] = remark
    
    return result

# Rol creado o modificado por última vez por un usuario bloqueado, con validación vencida o con contraseña inicial
def role_assignment_rule_one(data, rule_object):
    result = []
    columns = data[0]
    data = data[1:]
    one_year_ago = (datetime.now() - relativedelta(years=1)).strftime("%Y-%m-%d")
    invalid_users_filename = "invalid_usernames.txt"
    invalid_users = input_file_reading(invalid_users_filename)
    
    original_data_frame = pd.DataFrame(data, columns=columns)
    temporary_data_frame = pd.DataFrame(data, columns=columns)
    
    temporary_data_frame["CHANGE_DAT"] = pd.to_datetime(temporary_data_frame["CHANGE_DAT"], errors='coerce')
    temporary_data_frame["CREATE_DAT"] = pd.to_datetime(temporary_data_frame["CREATE_DAT"], errors='coerce')
    
    outliers_change_usr = original_data_frame[((temporary_data_frame["CHANGE_USR"].isin(invalid_users)) & (temporary_data_frame["CHANGE_DAT"] > one_year_ago))]
    outliers_create_usr = original_data_frame[((temporary_data_frame["CREATE_USR"].isin(invalid_users)) & (temporary_data_frame["CREATE_DAT"] > one_year_ago))]
    result = outliers_change_usr.values.tolist() + outliers_create_usr.values.tolist()
    
    for line in result:
        remark = MESSAGE_BY_LOG_GROUP[rule_object["group"]][rule_object["rule"]]
        line[len(line) - 1] = remark
    
    return result

 # Rol que se deriva de rol maestro con altos privilegios
def role_assignment_rule_two(data, rule_object):
    result = []
    columns = data[0]
    data = data[1:]
    relevant_roles_filename = "relevant_roles.txt"
    relevant_roles = input_file_reading(relevant_roles_filename)
    
    original_data_frame = pd.DataFrame(data, columns=columns)
    
    outliers = original_data_frame[original_data_frame["AGR_NAME"].isin(relevant_roles)]
    result = outliers.values.tolist()
    
    for line in result:
        remark = MESSAGE_BY_LOG_GROUP[rule_object["group"]][rule_object["rule"]]
        line[len(line) - 1] = remark
    
    return result

# Rol creado o modificado en hora atípica
def role_assignment_rule_three(data, rule_object):
    result = []
    columns = data[0]
    table_data = data[1:]
    
    original_data_frame = pd.DataFrame(table_data, columns=columns)
    temporary_data_frame = pd.DataFrame(table_data, columns=columns)
    
    temporary_data_frame["CHANGE_TIM"] = pd.to_datetime(temporary_data_frame["CHANGE_TIM"])
    outliers = original_data_frame[ np.abs(temporary_data_frame["CHANGE_TIM"] - temporary_data_frame["CHANGE_TIM"].mean()) > 2.78*temporary_data_frame["CHANGE_TIM"].std() ]
    
    result = outliers.values.tolist()
    
    for line in result:
        remark = MESSAGE_BY_LOG_GROUP[rule_object["group"]][rule_object["rule"]]
        line[len(line) - 1] = remark
    
    return result

def sanitize_date(date_string):
    return date_string.replace(".","-").strip()

def sanitize_time(time_string):
    return time_string.strip()

# Bloqueo de usuario en hora atípica
def user_change_rule_zero(data, rule_object):
    result = []
    columns = data[0]
    table_data = data[1:]
    
    original_data_frame = pd.DataFrame(table_data, columns=columns)
    temporary_data_frame = pd.DataFrame(table_data, columns=columns)
    
    temporary_data_frame["Hora"] = pd.to_datetime(temporary_data_frame["Hora"])
    outliers = original_data_frame[ np.abs(temporary_data_frame["Hora"] - temporary_data_frame["Hora"].mean()) > 1.75*temporary_data_frame["Hora"].std() ]
    
    result = outliers.values.tolist()
    
    for line in result:
        remark = MESSAGE_BY_LOG_GROUP[rule_object["group"]][rule_object["rule"]]
        line[len(line) - 1] = remark
    
    return result

# Desbloqueo de usuarios bloqueados por administrador (64) o administrador central CUA (32)
def user_change_rule_one(data, rule_object):
    result = []
    columns = data[0]
    table_data = data[1:]
    
    data_frame = pd.DataFrame(table_data, columns=columns)
    temporary_data_frame = pd.DataFrame(table_data, columns=columns)
    
    temporary_data_frame["Hora"] = pd.to_datetime(temporary_data_frame["Hora"])
    outliers = data_frame[ (np.abs(temporary_data_frame["Hora"] - temporary_data_frame["Hora"].mean()) > 1.75*temporary_data_frame["Hora"].std()) & ((data_frame["Valor ant."] == "64") | (data_frame["Valor ant."] == "32")) & (data_frame["Val.nuevo"] == "0") ]
    
    result = outliers.values.tolist()
    
    for line in result:
        remark = MESSAGE_BY_LOG_GROUP[rule_object["group"]][rule_object["rule"]]
        line[len(line) - 1] = remark
    
    return result

# Actividad realizada por usuario con más de un año sin iniciar sesión
def user_change_rule_two(data, rule_object):
    result = []
    
    columns = data[0]
    table_data = data[1:]
    unused_users_filename = "unused_usernames.txt"
    unused_users_users = input_file_reading(unused_users_filename)
    one_year_ago = (datetime.now() - relativedelta(years=1)).strftime("%Y-%m-%d")
    
    data_frame = pd.DataFrame(table_data, columns=columns)
    temporary_data_frame = pd.DataFrame(table_data, columns=columns)
    
    temporary_data_frame["Fecha"] = pd.to_datetime(temporary_data_frame["Fecha"])
    outliers = data_frame[(temporary_data_frame["Usuarios"].isin(unused_users_users)) | (temporary_data_frame["Modif.por"].isin(unused_users_users)) & (temporary_data_frame["Fecha"] > one_year_ago)]
    
    result = outliers.values.tolist()
    
    for line in result:
        remark = MESSAGE_BY_LOG_GROUP[rule_object["group"]][rule_object["rule"]]
        line[len(line) - 1] = remark
    
    return result

# Actividad realizada por usuario con validación vencida, bloqueado o con contraseña inicial
def user_change_rule_three(data, rule_object):
    result = []
    columns = data[0]
    table_data = data[1:]
    invalid_users_filename = "invalid_usernames.txt"
    invalid_users = input_file_reading(invalid_users_filename)
    one_year_ago = (datetime.now() - relativedelta(years=1)).strftime("%Y-%m-%d")
    
    data_frame = pd.DataFrame(table_data, columns=columns)
    temporary_data_frame = pd.DataFrame(table_data, columns=columns)
    
    temporary_data_frame["Fecha"] = pd.to_datetime(temporary_data_frame["Fecha"])
    outliers = data_frame[(temporary_data_frame["Usuarios"].isin(invalid_users)) | (temporary_data_frame["Modif.por"].isin(invalid_users)) & (temporary_data_frame["Fecha"] > one_year_ago)]
    
    result = outliers.values.tolist()
    
    for line in result:
        remark = MESSAGE_BY_LOG_GROUP[rule_object["group"]][rule_object["rule"]]
        line[len(line) - 1] = remark
    
    return result

def user_change_rule_four(data, rule_object):
    result = []
    tmp = []
    
    for line in data:
        if len(line) > USER_CHANGE_MANDATORY_LENGTH:  
            previous_user_status = line[12]
            current_user_status = line[5]
            username = line[1]
            
            if previous_user_status == "0" and current_user_status == "128":
                if username not in tmp:
                    tmp.append(username)
                else:
                    remark = MESSAGE_BY_LOG_GROUP[rule_object["group"]][rule_object["rule"]]
                    line[len(line) - 1] = remark
                    result.append(line)
            
            if previous_user_status != "0" and current_user_status == "0":
                if username in tmp:
                    tmp.remove(username)
    
    return result
            
            
    

# Modificación de tabla relevante en día/hora atípico (Sábado o Domingo de 22:00 a 2:00)
def datalog_table_rule_zero(data, rule_object):
    result = []
    columns = data[0]
    table_data = data[1:]
    
    relevant_tables_filename = "relevant_table_names.txt"
    relevant_tables = input_file_reading(relevant_tables_filename)
    
    original_data_frame = pd.DataFrame(table_data, columns=columns)
    temporary_data_frame = pd.DataFrame(table_data, columns=columns)
    
    temporary_data_frame["LOGTIME"] = pd.to_datetime(temporary_data_frame["LOGTIME"])
    
    outliers = original_data_frame.loc[ (temporary_data_frame["TABNAME"].isin(relevant_tables)) & (np.abs(temporary_data_frame["LOGTIME"] - temporary_data_frame["LOGTIME"].mean()) > 1.75*temporary_data_frame["LOGTIME"].std()) ]
    
    result = outliers.values.tolist()
    
    for line in result:
        remark = MESSAGE_BY_LOG_GROUP[rule_object["group"]][rule_object["rule"]]
        line[len(line) - 1] = remark
    
    return result

# Usuarios con más de un año sin iniciar sesión
def user_logon_rule_zero(data, rule_object):
    result = []
    raw_columns = data[0]
    today = datetime.now().strftime("%Y-%m-%d")
    one_year_ago = (datetime.now() - relativedelta(years=1)).strftime("%Y-%m-%d")
    
    columns = []
    count = 1
    for column in raw_columns:
        if column == 'Entr.sist.':
            columns.append(f'Entr.sist._{count}')
            count+=1
            continue
        columns.append(column)
    
    
    table_data = [line + [""] for line in data[2:]]
    original_data_frame = pd.DataFrame(table_data, columns=columns)
    temporary_data_frame = pd.DataFrame(table_data, columns=columns)
    
    temporary_data_frame["Entr.sist._1"] = pd.to_datetime(temporary_data_frame["Entr.sist._1"])
    outliers = original_data_frame[(~temporary_data_frame["Entr.sist._1"].isnull()) & ((temporary_data_frame["Entr.sist._1"] != "")) & (temporary_data_frame["Fin valid."] > today) & (temporary_data_frame["Entr.sist._1"] < one_year_ago) ]
    result = outliers.values.tolist()
    
    for line in result:
        remark = MESSAGE_BY_LOG_GROUP[rule_object["group"]][rule_object["rule"]]
        line[len(line) - 1] = remark
    
    return result

# Usuarios con validación vencida
def user_logon_rule_one(data, rule_object):
    result = []
    columns = data[0]
    one_year_ago = (datetime.now() - relativedelta(years=1)).strftime("%Y-%m-%d")
    
    
    table_data = [line + [""] for line in data[2:]]
    original_data_frame = pd.DataFrame(table_data, columns=columns)
    temporary_data_frame = pd.DataFrame(table_data, columns=columns)
    
    temporary_data_frame["Fin valid."] = pd.to_datetime(temporary_data_frame["Fin valid."], errors='coerce')
    outliers = original_data_frame[temporary_data_frame["Fin valid."] < one_year_ago]
    result = outliers.values.tolist()
    
    for line in result:
        remark = MESSAGE_BY_LOG_GROUP[rule_object["group"]][rule_object["rule"]]
        line[len(line) - 1] = remark
    
    return result

# Usuarios válidos con algoritmo de hash inseguro ({x-issha, 1024} : SAP CODVN H (PWDSALTEDHASH) iSSHA-1)
def user_logon_rule_two(data, rule_object):
    result = []
    columns = data[0]
    today = datetime.now().strftime("%Y-%m-%d")
    
    table_data = [line + [""] for line in data[2:]]
    original_data_frame = pd.DataFrame(table_data, columns=columns)
    temporary_data_frame = pd.DataFrame(table_data, columns=columns)
    
    temporary_data_frame["Fin valid."] = pd.to_datetime(temporary_data_frame["Fin valid."], errors='coerce')
    outliers = original_data_frame[temporary_data_frame["Val.ctrl.clv.acc."].str.contains("x-issha ") & (temporary_data_frame["Fin valid."] > today)]
    result = outliers.values.tolist()
    
    for line in result:
        remark = MESSAGE_BY_LOG_GROUP[rule_object["group"]][rule_object["rule"]]
        line[len(line) - 1] = remark
    
    return result

# Usuarios válidos que requieren cambio de contraseña (1, 2 y 3)
def user_logon_rule_three(data, rule_object):
    result = []
    columns = data[0]
    today = datetime.now().strftime("%Y-%m-%d")
    
    table_data = [line + [""] for line in data[2:]]
    original_data_frame = pd.DataFrame(table_data, columns=columns)
    temporary_data_frame = pd.DataFrame(table_data, columns=columns)
    
    temporary_data_frame["Fin valid."] = pd.to_datetime(temporary_data_frame["Fin valid."], errors='coerce')
    outliers = original_data_frame[((original_data_frame["Modif.cl.acceso"] == "1") | (original_data_frame["Modif.cl.acceso"] == "2") | (original_data_frame["Modif.cl.acceso"] == "3")) & (temporary_data_frame["Fin valid."] > today)]
    result = outliers.values.tolist()
    
    for line in result:
        remark = MESSAGE_BY_LOG_GROUP[rule_object["group"]][rule_object["rule"]]
        line[len(line) - 1] = remark
    
    return result

# Usuario bloqueado por administrador
def user_logon_rule_four(data, rule_object):
    result = []
    columns = data[0]
    
    table_data = [line + [""] for line in data[2:]]
    original_data_frame = pd.DataFrame(table_data, columns=columns)
    outliers = original_data_frame[(original_data_frame["Bloqueo"] == "64") | (original_data_frame["Bloqueo"] == "32")]
    result = outliers.values.tolist()
    
    for line in result:
        remark = MESSAGE_BY_LOG_GROUP[rule_object["group"]][rule_object["rule"]]
        line[len(line) - 1] = remark
    
    return result

RULES_BY_LOG_GROUP = {
    "role_assignment": {
            "0": role_assignment_rule_zero,
            "1": role_assignment_rule_one,
            "2": role_assignment_rule_two,
            "3": role_assignment_rule_three
        },
    "user_change": {
            "0": user_change_rule_zero,
            "1": user_change_rule_one,
            "2": user_change_rule_two,
            "3": user_change_rule_three,
            "4": user_change_rule_four
        },
    "datalog_table": {
            "0": datalog_table_rule_zero
        },
    "user_logon": {
            "0": user_logon_rule_zero,
            "1": user_logon_rule_one,
            "2": user_logon_rule_two,
            "3": user_logon_rule_three,
            "4": user_logon_rule_four
    }
}