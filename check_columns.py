from sqlalchemy import inspect
from database import engine

inspector = inspect(engine)
columns = inspector.get_columns('citas')

print("\n=== Columnas en tabla 'citas' ===")
for col in columns:
    print(f"{col['name']:20} - {col['type']}")
