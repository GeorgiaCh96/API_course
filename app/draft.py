from config import settings
print(settings.database_port, type(settings.database_port))  # Should print: 5432 <class 'int'>
print(settings.database_hostname, type(settings.database_hostname))  # Should print: localhost <class 'str'>
