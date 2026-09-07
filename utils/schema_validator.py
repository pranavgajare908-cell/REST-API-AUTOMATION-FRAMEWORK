import json
from pathlib import Path

import jsonschema


class SchemaValidator:

    @staticmethod
    def validate(response_data, schema_file):
        """
        Validate API response data against a JSON schema.
        """

        schema_path = Path(schema_file)

        if not schema_path.exists():
            raise FileNotFoundError(
                f"Schema file not found: {schema_path}"
            )

        with open(schema_path, "r", encoding="utf-8") as file:
            schema = json.load(file)

        try:
            jsonschema.validate(
                instance=response_data,
                schema=schema,
                format_checker=jsonschema.FormatChecker()
            )
        except jsonschema.ValidationError as e:
            print("\n========== JSON SCHEMA VALIDATION ERROR ==========")
            print("Message:", e.message)
            print("Path:", list(e.path))
            print("Schema Path:", list(e.schema_path))
            print("==================================================\n")

            raise AssertionError(
                f"JSON Schema validation failed: {e.message}"
            ) from e

