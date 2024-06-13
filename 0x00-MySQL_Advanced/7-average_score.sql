-- script that creates a stored procedure
-- that computes and store the average score for a student.
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_count INT;

    -- Calculate total score and count for the user
    SELECT SUM(score), COUNT(*) INTO total_score, total_count
    FROM corrections
    WHERE user_id = user_id;

    -- Compute average score (handle division by zero)
    IF total_count > 0 THEN
        UPDATE users
        SET average_score = total_score / total_count
        WHERE id = user_id;
    ELSE
        UPDATE users
        SET average_score = 0
        WHERE id = user_id;
    END IF;
END;
//
DELIMITER ;
