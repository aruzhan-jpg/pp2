-- 1. Search by pattern
CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.phone
    FROM contacts c
    WHERE c.name ILIKE '%' || pattern || '%'
       OR c.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


-- 2. Pagination
CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, offs INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.phone
    FROM contacts c
    ORDER BY c.id
    LIMIT lim OFFSET offs;
END;
$$ LANGUAGE plpgsql;