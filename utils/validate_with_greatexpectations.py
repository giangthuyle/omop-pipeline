import great_expectations as gx
import pandas as pd
import os
import json
from pathlib import Path
from great_expectations.validator.validator import Validator
from great_expectations.core.expectation_suite import ExpectationSuite



# Đường dẫn gốc tới OMOP_Project
BASE_DIR = Path(__file__).resolve().parent.parent

# Đường dẫn dữ liệu và báo cáo
PARQUET_DIR = BASE_DIR / "data" / "parquet"
REPORT_DIR = BASE_DIR / "data" / "validation_reports"
GE_TMP_DIR = BASE_DIR / "utils" / "gx_tmp"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
GE_TMP_DIR.mkdir(parents=True, exist_ok=True)

# Custom rules per table
CUSTOM_EXPECTATIONS = {
    "person": {
        "expect_column_values_to_not_be_null": ["person_id"],
        "expect_column_values_to_be_between": {
            "year_of_birth": {"min_value": 1800, "max_value": 2025}
        }
    },
    "visit_occurrence": {
        "expect_column_values_to_be_of_type": {
            "visit_start_date": "datetime64[ns]"
        }
    }
}

# Auto-generate expectations from schema
def auto_generate_expectations(validator: Validator, df: pd.DataFrame):
    for col in df.columns:
        dtype = df[col].dtype
        if pd.api.types.is_numeric_dtype(dtype):
            validator.expect_column_values_to_be_of_type(col, "float64")
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            validator.expect_column_values_to_be_of_type(col, "datetime64[ns]")
        elif pd.api.types.is_string_dtype(dtype):
            validator.expect_column_values_to_be_of_type(col, "object")
        validator.expect_column_values_to_not_be_null(col)

# Run validation on 1 table
def validate_table(table_name, file_path):
    print(f"🔍 Validating {table_name}...")
    df = pd.read_parquet(file_path)

    # Tạo context (dùng Fluent API)
    context = gx.get_context()

    # ✅ Tạo expectation suite
    suite_name = f"{table_name}_suite"
    suite_identifier = ExpectationSuiteIdentifier(suite_name)

    # Kiểm tra nếu suite đã tồn tại
    try:
        suite = context.expectations_store.get(suite_identifier)
    except KeyError:
        suite = ExpectationSuite(suite_name)
        context.expectations_store.set(key=suite_identifier)

    # Tạo validator trực tiếp từ DataFrame
    validator = context.get_validator(
        dataframe=df,
        expectation_suite_name=suite_name,
    )

    # Gọi auto generate expectation hoặc thêm expectation custom
    auto_generate_expectations(validator, df)

    # # Tạo suite mới
    # suite = ExpectationSuite(name=suite_name)
    # context.suites.add(suite)
    #
    # # ✅ Tạo validator trực tiếp từ DataFrame (không cần batch hay datasource thêm)
    # validator = context.data_sources.pandas_default.add_dataframe(
    #     name=table_name,
    #     dataframe=df,
    #     expectation_suite=suite,
    # )


    # ✅ Auto-generate expectations
    auto_generate_expectations(validator, df)

    # ✅ Add custom expectations nếu có
    expectations = CUSTOM_EXPECTATIONS.get(table_name, {})
    for col in expectations.get("expect_column_values_to_not_be_null", []):
        validator.expect_column_values_to_not_be_null(col)

    for col, limits in expectations.get("expect_column_values_to_be_between", {}).items():
        validator.expect_column_values_to_be_between(col, **limits)

    for col, dtype in expectations.get("expect_column_values_to_be_of_type", {}).items():
        validator.expect_column_values_to_be_of_type(col, dtype)

    # ✅ Run validation
    result = validator.validate()

    # ✅ Save JSON report
    report_path = REPORT_DIR / f"{table_name}_report.json"
    with open(report_path, "w") as f:
        json.dump(result.to_json_dict(), f, indent=2, default=str)

    # ✅ Log result
    if result["success"]:
        print(f"✅ {table_name} passed validation. Report saved at: {report_path}\n")
    else:
        print(f"❌ {table_name} failed validation. See report at: {report_path}\n")

    print(dir(context))
    print(context.__class__)

# Validate tất cả các bảng
def validate_all():
    for file in os.listdir(PARQUET_DIR):
        if file.endswith(".parquet"):
            table_name = file.replace(".parquet", "")
            file_path = PARQUET_DIR / file
            validate_table(table_name, file_path)

if __name__ == "__main__":
    validate_all()


    #def validate():
    # Create data source
    #context = ge.get_context()

    # Follow this tutorial
    # https://legacy.017.docs.greatexpectations.io/docs/0.15.50/deployment_patterns/how_to_use_great_expectations_with_google_cloud_platform_and_bigquery/


