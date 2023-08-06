from pathlib import Path

from commonmodel.base import schema_from_yaml_file

from .importers.import_orders import import_orders
from .importers.import_payments import import_payments

# Schemas
SquarePayment = schema_from_yaml_file(
    Path(__file__).parent / "schemas/SquarePayment.yml"
)
SquareOrder = schema_from_yaml_file(Path(__file__).parent / "schemas/SquareOrder.yml")
