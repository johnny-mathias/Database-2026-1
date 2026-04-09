DECLARE

    v_dano_nevoa NUMBER := 10;

    CURSOR c_herois IS
        SELECT id_heroi, hp_atual, hp_max
        FROM TB_HEROIS
        WHERE status = 'ATIVO'
        FOR UPDATE;

    v_hp NUMBER;

BEGIN

    FOR r IN c_herois LOOP

        v_hp := r.hp_atual - v_dano_nevoa;

        IF v_hp <= 0 THEN
            UPDATE TB_HEROIS
            SET hp_atual = 0,
                status = 'CAIDO'
            WHERE id_heroi = r.id_heroi;
        ELSE
            UPDATE TB_HEROIS
            SET hp_atual = v_hp
            WHERE id_heroi = r.id_heroi;
        END IF;

    END LOOP;

END;