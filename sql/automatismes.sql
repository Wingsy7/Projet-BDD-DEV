USE equipe_5;

DROP TRIGGER IF EXISTS trg_after_eleve_insert_create_dossier;
DROP TRIGGER IF EXISTS trg_before_prof_delete_notes_to_ten;
DROP TRIGGER IF EXISTS trg_before_note_update_keep_best;
DROP PROCEDURE IF EXISTS sp_recalculer_classement_eleves;

DELIMITER $$

CREATE PROCEDURE sp_recalculer_classement_eleves()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE v_eleve_id INT;
    DECLARE v_moyenne DECIMAL(5, 2);
    DECLARE v_absence INT;
    DECLARE v_warn INT;
    DECLARE v_score INT;

    DECLARE cur CURSOR FOR
        SELECT id
        FROM eleve;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    DELETE FROM classement_eleve;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO v_eleve_id;

        IF done = 1 THEN
            LEAVE read_loop;
        END IF;

        SELECT COALESCE(AVG(valeur), 0)
        INTO v_moyenne
        FROM note
        WHERE eleve_id = v_eleve_id;

        SELECT COALESCE(SUM(duree_minutes), 0)
        INTO v_absence
        FROM absence
        WHERE eleve_id = v_eleve_id;

        SELECT COALESCE(
            MAX(
                CASE
                    WHEN avertissement_travail = 1 OR avertissement_comportement = 1 THEN 1
                    ELSE 0
                END
            ),
            0
        )
        INTO v_warn
        FROM dossier
        WHERE eleve_id = v_eleve_id;

        SET v_score = 1;

        IF v_moyenne > 15 THEN
            SET v_score = v_score + 5;
        ELSEIF v_moyenne > 12 THEN
            SET v_score = v_score + 3;
        ELSEIF v_moyenne > 10 THEN
            SET v_score = v_score + 2;
        ELSEIF v_moyenne > 8 THEN
            SET v_score = v_score + 1;
        ELSEIF v_moyenne < 5 THEN
            SET v_score = v_score - 2;
        END IF;

        IF v_absence < 120 THEN
            SET v_score = v_score + 5;
        ELSEIF v_absence < 240 THEN
            SET v_score = v_score + 3;
        ELSEIF v_absence < 480 THEN
            SET v_score = v_score + 2;
        ELSEIF v_absence < 720 THEN
            SET v_score = v_score + 1;
        ELSEIF v_absence > 1080 THEN
            SET v_score = v_score - 2;
        END IF;

        IF v_warn = 1 THEN
            SET v_score = v_score - 2;
        END IF;

        SET v_score = GREATEST(1, LEAST(10, v_score));

        INSERT INTO classement_eleve (
            eleve_id,
            score,
            moyenne_generale,
            total_absence_minutes,
            a_un_avertissement
        )
        VALUES (
            v_eleve_id,
            v_score,
            v_moyenne,
            v_absence,
            v_warn
        );
    END LOOP;

    CLOSE cur;

    SELECT
        e.nom,
        c.score,
        c.moyenne_generale,
        c.total_absence_minutes,
        c.a_un_avertissement
    FROM classement_eleve c
    JOIN eleve e ON e.id = c.eleve_id
    ORDER BY c.score DESC, c.moyenne_generale DESC, e.nom ASC;
END $$

CREATE TRIGGER trg_after_eleve_insert_create_dossier
AFTER INSERT ON eleve
FOR EACH ROW
BEGIN
    INSERT INTO dossier (
        eleve_id,
        infos,
        avertissement_travail,
        avertissement_comportement
    )
    VALUES (
        NEW.id,
        CASE
            WHEN NEW.age < 18 THEN 'mineur'
            ELSE ''
        END,
        0,
        0
    );
END $$

CREATE TRIGGER trg_before_prof_delete_notes_to_ten
BEFORE DELETE ON prof
FOR EACH ROW
BEGIN
    SET @skip_keep_best_trigger = 1;

    UPDATE note
    SET valeur = 10.00,
        prof_id = NULL
    WHERE prof_id = OLD.id;

    SET @skip_keep_best_trigger = 0;
END $$

CREATE TRIGGER trg_before_note_update_keep_best
BEFORE UPDATE ON note
FOR EACH ROW
BEGIN
    IF COALESCE(@skip_keep_best_trigger, 0) = 0 AND NEW.valeur < OLD.valeur THEN
        SET NEW.valeur = OLD.valeur;
    END IF;
END $$

DELIMITER ;
