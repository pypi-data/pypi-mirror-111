from simple_ddl_parser import DDLParser

ddl = """
CREATE DATABASE yourdbname;
CREATE DATABASE "yourdbname2";
"""
result = DDLParser(ddl).run(group_by_type=True)

print(result)
