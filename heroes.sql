DECLARE
    v_dano_nevoa NUMBER := 10;
BEGIN
    FOR r IN (
        SELECT id_heroi, hp_atual
        FROM TB_HEROIS
        WHERE status = 'ATIVO'
    ) LOOP
    
        UPDATE TB_HEROIS
        SET hp_atual = hp_atual - v_dano_nevoa
        WHERE id_heroi = r.id_heroi;

        UPDATE TB_HEROIS
        SET status = 'CAIDO'
        WHERE id_heroi = r.id_heroi
        AND hp_atual - v_dano_nevoa <= 0;

    END LOOP;

END;