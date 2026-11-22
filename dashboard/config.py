
import os
from pathlib import Path

import clickhouse_connect
from dotenv import load_dotenv

# Lokasi folder dashboard
BASE_DIR = Path(__file__).resolve().parent

# Membaca konfigurasi dari file .env
load_dotenv(BASE_DIR / ".env")


def get_clickhouse_client():
    """
    Membuat koneksi ke ClickHouse.
    """

    client = clickhouse_connect.get_client(
        host=os.getenv("CLICKHOUSE_HOST"),
        port=int(os.getenv("CLICKHOUSE_PORT", 8123)),
        username=os.getenv("CLICKHOUSE_USER"),
        password=os.getenv("CLICKHOUSE_PASSWORD"),
        database=os.getenv("CLICKHOUSE_DATABASE"),
    )

    return client


def test_connection():
    """
    Menguji koneksi dan mengambil versi ClickHouse.
    """

    client = get_clickhouse_client()

    try:
        result = client.query("SELECT version()")
        return result.result_rows[0][0]
    finally:
        client.close()
