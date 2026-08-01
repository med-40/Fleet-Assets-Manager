import sqlite3
from pathlib import Path


DATABASE_DIR = Path.home() / "FleetAssetsManager"
DATABASE_FILE = DATABASE_DIR / "fleet.db"


def get_connection():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT NOT NULL UNIQUE,
            vehicle_type TEXT,
            model TEXT,
            driver TEXT,
            license_expiry TEXT,
            status TEXT DEFAULT 'متاحة',
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER,
            destination TEXT,
            start_date TEXT,
            end_date TEXT,
            status TEXT DEFAULT 'جارية',
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER,
            maintenance_type TEXT,
            maintenance_date TEXT,
            description TEXT,
            status TEXT DEFAULT 'مستحقة',
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fuel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER,
            fuel_date TEXT,
            quantity REAL DEFAULT 0,
            odometer REAL DEFAULT 0,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faults (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER,
            fault_date TEXT,
            description TEXT,
            repair_status TEXT DEFAULT 'مفتوح',
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS batteries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER,
            installation_date TEXT,
            battery_type TEXT,
            serial_number TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tires (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER,
            installation_date TEXT,
            tire_position TEXT,
            tire_type TEXT,
            serial_number TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
        )
    """)

    connection.commit()
    connection.close()


def get_dashboard_counts():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM vehicles")
    vehicles = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM missions
        WHERE status = 'جارية'
    """)
    active_missions = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM maintenance
        WHERE status = 'مستحقة'
    """)
    due_maintenance = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(quantity), 0)
        FROM fuel
        WHERE strftime('%Y-%m', fuel_date) = strftime('%Y-%m', 'now')
    """)
    monthly_fuel = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM faults
        WHERE repair_status = 'مفتوح'
    """)
    open_faults = cursor.fetchone()[0]

    connection.close()

    return {
        "vehicles": vehicles,
        "active_missions": active_missions,
        "due_maintenance": due_maintenance,
        "monthly_fuel": monthly_fuel,
        "open_faults": open_faults,
    }
