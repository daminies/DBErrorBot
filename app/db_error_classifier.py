import re

<<<<<<< HEAD
# 현재 미사용
=======
# 현재 미사용 
>>>>>>> 9a139143bf0a9f34e4e8d151ebfb797e385e1759
def classify_error_type(message: str) -> dict:
    if "ORA-" in message:
        match = re.search(r"(ORA-\d{5})", message)
        return {"db_type": "oracle", "error_key": match.group(1) if match else message}
    elif "SQL Server" in message or "MSSQL" in message:
        return {"db_type": "mssql", "error_key": message}
    elif "MySQL" in message:
        return {"db_type": "mysql", "error_key": message}
    else:
        return {"db_type": "unknown", "error_key": message}




