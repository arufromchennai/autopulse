USE DATABASE AUTOPULSE_DB;

-- Stored Procedure: Atomic Dispatch and Inventory Reservation
CREATE OR REPLACE PROCEDURE SERVICE.SP_AUTHORIZE_REPAIR_AND_RESERVE_INVENTORY(
    p_vin VARCHAR,
    p_part_number VARCHAR,
    p_dealer_id VARCHAR,
    p_service_code VARCHAR,
    p_cost FLOAT
)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    available_stock INT;
BEGIN
    -- Check local dealership inventory
    SELECT STOCK_ON_HAND INTO :available_stock
    FROM SERVICE.DEALERSHIP_INVENTORY
    WHERE DEALER_ID = :p_dealer_id AND PART_NUMBER = :p_part_number;

    IF (:available_stock IS NULL) THEN
        RETURN 'ERROR: Part number ' || :p_part_number || ' is not cataloged at dealership ' || :p_dealer_id;
    END IF;

    IF (:available_stock <= 0) THEN
        RETURN 'ERROR: Allocation failed. Zero units available on-hand at ' || :p_dealer_id;
    END IF;

    BEGIN TRANSACTION;
        -- Decrement physical stock and increment allocation
        UPDATE SERVICE.DEALERSHIP_INVENTORY
        SET STOCK_ON_HAND = STOCK_ON_HAND - 1,
            STOCK_RESERVED = STOCK_RESERVED + 1
        WHERE DEALER_ID = :p_dealer_id AND PART_NUMBER = :p_part_number;

        -- Update service queue status
        UPDATE AGENT.SERVICE_RECOMMENDATIONS
        SET APPROVAL_STATUS = 'DISPATCHED_TO_WORK_ORDER'
        WHERE VIN = :p_vin;

        -- Decrement parts on-hand in analytical snapshot
        UPDATE MART.FACT_SERVICE_MAINTENANCE_ANALYTICS
        SET DEALER_PARTS_ON_HAND = GREATEST(0, DEALER_PARTS_ON_HAND - 1)
        WHERE VIN = :p_vin AND AGGREGATION_DATE = CURRENT_DATE();
    COMMIT;

    RETURN 'SUCCESS: Work order authorized. Reserved ' || :p_part_number || ' at hub ' || :p_dealer_id || ' for asset ' || :p_vin || '.';
EXCEPTION
    WHEN OTHER THEN
        ROLLBACK;
        RETURN 'ERROR: Transaction aborted due to SQL error: ' || SQLERRM;
END;
$$;