-- Close current record if update operation
UPDATE contracts
SET 
    is_current = FALSE,
    end_date = NOW()
WHERE contract_id = %(contract_id)s
  AND is_current = TRUE
  AND %(operation)s = 'update';


-- Insert new row
INSERT INTO contracts (
    contract_id,
    vendor,
    value,
    risk_level,
    summary,        
    status,
    is_current,
    start_date
)
SELECT
    COALESCE(src.contract_id, %(contract_id)s),
    COALESCE(src.vendor, %(vendor)s),
    COALESCE(src.value, %(value)s),
    COALESCE(src.risk_level, %(risk_level)s),
    COALESCE(src.summary, %(summary)s),   
    %(status)s,
    TRUE,
    NOW()
FROM (
    SELECT *
    FROM contracts
    WHERE contract_id = %(contract_id)s
    ORDER BY start_date DESC
    LIMIT 1
) src
RIGHT JOIN (SELECT 1) dummy ON TRUE
WHERE %(operation)s IN ('insert', 'update');