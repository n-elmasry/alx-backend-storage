-- creates a stored procedure AddBonus that adds a new correction for a student.

DELIMITER //

CREATE PROCEDURE AddBonus(
    IN user_id INTEGER,
    IN project_name VARCHAR(255),
    IN score INTEGER
)
BEGIN
    -- Check if the project exists
    IF NOT EXISTS (SELECT name FROM projects WHERE name = project_name) THEN
        -- If the project does not exist, insert it
        INSERT INTO projects (name) VALUES (project_name);
    END IF;

    -- Insert the new correction
    INSERT INTO correction (user_id, project_id, score)
    VALUES (
        user_id,
        (SELECT id FROM projects WHERE name = project_name),
        score
    );
END//

DELIMITER ;
