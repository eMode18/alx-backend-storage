-- Compute lifespan until 2022
SELECT band_name, 
       (YEAR('2022-01-01') - YEAR(formed)) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
