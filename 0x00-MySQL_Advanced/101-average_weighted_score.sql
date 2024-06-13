-- Create a stored procedure to compute and store the average weighted score for all students
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight INT;

    -- Calculate the total weighted score and total weight for all users
    SELECT SUM(score * weight), SUM(weight) INTO total_weighted_score, total_weight
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id;

    -- Compute the average weighted score (handle division by zero)
    IF total_weight > 0 THEN
        UPDATE users
        SET average_score = total_weighted_score / total_weight;
    ELSE
        UPDATE users
        SET average_score = 0;
    END IF;
END;
$$
DELIMITER ;
