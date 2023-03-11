import argparse, uuid
from rules import RULES_BY_LOG_GROUP, sanitize_text

parser = argparse.ArgumentParser(description="SAP Log scan tool")
parser.add_argument("-k", "--keywords", help="Comma separated values to look for in the logs.")
parser.add_argument("-f", "--filename", help="Log file to be scanned.")
parser.add_argument("-iL", "--input-list", help="Keyword file.")
parser.add_argument("-sH", "--start-index", help="Index of headers.", default=1)
parser.add_argument("-eH", "--end-index", help="Final index line to read.")
parser.add_argument("-enc", "--encoding", help="Read encoding, by default it is set to UTF-8", default="utf8")
parser.add_argument("-g", "--log-group", help="Log groups, possible values: role_assignment, user_change, datalog_table and user_logon", default="utf8")
parser = parser.parse_args()

# EJEMPLOS DE ENCODING DE LECTURA: utf16, cp1252

DEFAULT_WRITE_ENCODING = "utf8"
NEW_HEADER_ELEMENT = ["OBSERVACIONES"]

def read_file(filename, encoding, start_index, end_index):
    result = []
    
    try:
        file = open(filename, "r", encoding=encoding)
        result = log_file_reading(start_index, end_index, result, file)
        
        file.close()
        print("- File read.")
    except Exception as e:
        print(f"Reading file failed: {e}")
    return result

def log_file_reading(start_index, end_index, result, file):
    file_read = file.read()
    file_lines = file_read.splitlines()
            
    end_index = end_index if end_index else len(file_lines)
    
    
    for number_line in range(start_index, end_index):
        line = [element.replace("\n", "").replace(",","") for element in file_lines[number_line].split("\t")]
        result.append(line)
    
    return result

def add_remarks_column(current_data_object):
    result = []
    headers = current_data_object[0] + NEW_HEADER_ELEMENT
    data = [line + [""] for line in current_data_object[1:]]
    
    result.append(headers)
    result = result + data
    
    return result

def text_parser(data):
    result = ""
    
    try:
    
        for element in data:
            if None not in element:
                result = result + ",".join(element) + "\n"
        
        print("- Text parsed.")
    except Exception as e:
        print(f"Text parser failed: {e}")
    return result

def write_file(data, preffix):
    try:
        filename = preffix + "_FILTERED_" + str(uuid.uuid4()) + ".csv"
        new_file = open(filename, "w", encoding=DEFAULT_WRITE_ENCODING)
        new_file.write(data)
        new_file.close()
        print(f"- New file written: {filename}.")
    except Exception as e:
        print(f"Writing file failed: {e}")
        
def process_filename(name):
    result = ""
    raw_list = name.split(".")
    raw_list_length = len(raw_list)
    
    if raw_list_length > 1:
        result = raw_list[len(raw_list) - 2]
    else:
        result = raw_list[0]
        
    result = sanitize_text(result).replace("/", "").replace("\\", "").replace(" ", "_")
    
    print("- Filename processed.")
    return result

def rule_processor(selected_group, data_object):
    result = []
    
    try:
        for rule in RULES_BY_LOG_GROUP[selected_group]:
            rule_object = {"group":selected_group, "rule":rule}
            rule_output = RULES_BY_LOG_GROUP[selected_group][rule](data_object, rule_object)
            result = result + rule_output
    
        result.insert(0,data_object[0])
    
    except Exception as e:
        raise Exception(f"Rule processor failed: {e}")

    return result
    
def main():
    filename = parser.filename
    start_index = int(parser.start_index)
    end_index = int(parser.end_index) if parser.end_index else None
    encoding = parser.encoding
    selected_group = parser.log_group
    
    if not selected_group:
        raise Exception("Something happened, please check your parameters.")
    
    log_sheet = read_file(filename, encoding, start_index, end_index)
    raw_data = add_remarks_column(log_sheet)
    
    
    filtered_data = rule_processor(selected_group, raw_data)
    text_data = text_parser(filtered_data)
    processed_filename = process_filename(filename)
    
    write_file(text_data, processed_filename)
    
    
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Log scan failed: {e}")