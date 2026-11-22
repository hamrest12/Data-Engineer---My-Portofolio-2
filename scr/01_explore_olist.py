from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "docs" / "exploration"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

csv_file = sorted(RAW_DIR.glob("*.csv"))

if not csv_file:
    raise FileNotFoundError(
        f"Tidak Ada File CSV Ditemukan pada: {RAW_DIR}"
    )

summary = []
column_detail = []
quality_details = []

print("="*70)
print("Olist Dataset Exploration")
print("="*70)

for file_path in csv_file:
    print(f"\nMemeriksa: {file_path.name}")

    df = pd.read_csv(file_path)

    row_count = len(df)
    columns_count = len(df.columns)
    memory_mb = df.memory_usage(deep=True).sum()/(1024 ** 2)

    print(f"Jumlah Baris: {row_count}")
    print(f"Jumlah Kolom: {columns_count}")
    print(f"Besar File: {memory_mb:2f}")
    print("Kolom:")
    print(df.columns.tolist())

    summary.append(
        {
            "file_name" : file_path.name,
            "row_count" : row_count,
            "columns_count" : columns_count,
            "memory_mb" : memory_mb
        }
    )

    for columns in df.columns:
        column_detail.append(
            {
                "file_name" : file_path.name,
                "columns_name" : columns,
                "data_type" : str(df[columns].dtype)
            }
        )

    for columns in df.columns:
        null_count = int(df[columns].isna().sum())
        null_percentage = (null_count*100 if row_count else 0)

        quality_details.append(
            {
            "file_name": file_path.name,
            "column_name": columns,
            "null_count": null_count,
            "null_percentage": round(null_percentage, 2),
            "distinct_count": int(df[columns].nunique()),
            }
        )

    print("\nContoh Data")
    print(df.tail(3).to_string(index=False))

pd.DataFrame(summary).to_csv(REPORT_DIR / "table_summary.csv", index=False)
pd.DataFrame(column_detail).to_csv(REPORT_DIR / "columns_detail.csv", index=False)
pd.DataFrame(quality_details).to_csv(REPORT_DIR / "columns_quality.csv", index=False)

print("\n"+"-"*70)
print("Explorasi Selesai")
print(f"Laporan Disimpan di: {REPORT_DIR}")
print("-"*70)
