import os
import random
from datetime import datetime, timedelta
import snowflake.connector

def seed_fleet_and_telemetry():
    conn = snowflake.connector.connect(
        account=os.environ.get("SNOWFLAKE_ACCOUNT"),
        user=os.environ.get("SNOWFLAKE_USER"),
        password=os.environ.get("SNOWFLAKE_PASSWORD"),
        role=os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        warehouse="AUTOPULSE_WH",
        database="AUTOPULSE_DB"
    )
    cursor = conn.cursor()
    print("Seeding AutoPulse Mart and 14-day Telemetry Features...")

    # 1. Fleet Seed
    fleet_rows = [
        ("CAR-18391", "Pulse-EV", "Performance Dual-Motor", "2025", 42180, "ACTIVE", "CRITICAL", "Inverter Phase B", 3, "DLR-WEST-01"),
        ("CAR-20412", "Pulse-SUV", "AWD Long Range", "2024", 61200, "ACTIVE", "CRITICAL", "Brake Actuator", 5, "DLR-EAST-02"),
        ("CAR-99120", "Pulse-GT", "Track Edition", "2025", 18500, "ACTIVE", "HIGH", "Auxiliary 12V Cell", 9, "DLR-CENTRAL-03"),
        ("CAR-33104", "Pulse-Sedan", "Standard Range", "2023", 84300, "ACTIVE", "HIGH", "Battery Thermal Pump", 12, "DLR-WEST-01")
    ]
    cursor.executemany("""
        MERGE INTO MART.DIM_VEHICLE_FLEET_HEALTH t
        USING (SELECT %s AS VIN, %s AS MODEL, %s AS VARIANT, %s AS MODEL_YEAR, %s AS CURRENT_ODOMETER_KM,
                      %s AS WARRANTY_STATUS, %s AS HIGHEST_COMPONENT_RISK, %s AS CRITICAL_COMPONENT_AT_RISK,
                      %s AS MIN_PREDICTED_RUL_DAYS, %s AS PRIMARY_DEALER_ID) s
        ON t.VIN = s.VIN
        WHEN MATCHED THEN UPDATE SET
            t.HIGHEST_COMPONENT_RISK = s.HIGHEST_COMPONENT_RISK,
            t.CRITICAL_COMPONENT_AT_RISK = s.CRITICAL_COMPONENT_AT_RISK,
            t.MIN_PREDICTED_RUL_DAYS = s.MIN_PREDICTED_RUL_DAYS
        WHEN NOT MATCHED THEN INSERT (
            VIN, MODEL, VARIANT, MODEL_YEAR, CURRENT_ODOMETER_KM,
            WARRANTY_STATUS, HIGHEST_COMPONENT_RISK, CRITICAL_COMPONENT_AT_RISK,
            MIN_PREDICTED_RUL_DAYS, PRIMARY_DEALER_ID
        ) VALUES (
            s.VIN, s.MODEL, s.VARIANT, s.MODEL_YEAR, s.CURRENT_ODOMETER_KM,
            s.WARRANTY_STATUS, s.HIGHEST_COMPONENT_RISK, s.CRITICAL_COMPONENT_AT_RISK,
            s.MIN_PREDICTED_RUL_DAYS, s.PRIMARY_DEALER_ID
        );
    """, fleet_rows)

    # 2. Service & Maintenance Analytics Seed
    service_rows = [
        ("CAR-18391", "SRV-INV-99", 1850.00, "INV-8820-T", 4, "DLR-WEST-01"),
        ("CAR-20412", "SRV-BRK-04", 420.00, "BRK-4001-A", 8, "DLR-EAST-02"),
        ("CAR-99120", "SRV-BAT-12", 310.00, "BAT-0012-V", 14, "DLR-CENTRAL-03"),
        ("CAR-33104", "SRV-THM-08", 890.00, "THM-5509-P", 6, "DLR-WEST-01")
    ]
    cursor.executemany("""
        INSERT INTO MART.FACT_SERVICE_MAINTENANCE_ANALYTICS (
            VIN, AGGREGATION_DATE, RECOMMENDED_SERVICE_CODE, ESTIMATED_REPAIR_COST,
            PART_NUMBER_REQUIRED, DEALER_PARTS_ON_HAND, PRIMARY_DEALER_ID
        ) VALUES (%s, CURRENT_DATE(), %s, %s, %s, %s, %s)
    """, service_rows)

    # 3. Recommendations Queue Seed
    rec_rows = [
        ("CAR-18391", "SRV-INV-99", 1850.00, "PENDING_APPROVAL"),
        ("CAR-20412", "SRV-BRK-04", 420.00, "PENDING_APPROVAL")
    ]
    cursor.executemany("""
        INSERT INTO AGENT.SERVICE_RECOMMENDATIONS (VIN, SERVICE_CODE, ESTIMATED_COST, APPROVAL_STATUS)
        VALUES (%s, %s, %s, %s)
    """, rec_rows)

    # 4. 14-Day Historical Sensor Trace per VIN
    today = datetime.utcnow().date()
    history_records = []
    base_temps = {"CAR-18391": 68.0, "CAR-20412": 45.0, "CAR-99120": 38.0, "CAR-33104": 42.0}

    for vin, init_temp in base_temps.items():
        for day_offset in range(14, -1, -1):
            f_date = today - timedelta(days=day_offset)
            # Escalating degradation pattern for CAR-18391 and CAR-20412
            escalation = (14 - day_offset) * (3.8 if vin == "CAR-18391" else 1.2)
            avg_temp = init_temp + escalation + random.uniform(-1.5, 1.5)
            roughness = round(1.1 + ((14 - day_offset) * 0.22) + random.uniform(-0.1, 0.2), 2)
            history_records.append((vin, f_date.strftime("%Y-%m-%d"), round(avg_temp, 2), roughness))

    cursor.executemany("""
        INSERT INTO FEATURES.VEHICLE_TELEMETRY_DAILY_AGG (
            VIN, FEATURE_DATE, AVG_BRAKE_TEMP_C, SEVERE_ROUGHNESS_CYCLES
        ) VALUES (%s, %s, %s, %s)
    """, history_records)

    conn.commit()
    print("Database seeding completed successfully.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    seed_fleet_and_telemetry()