SET SERVEROUTPUT ON;

DECLARE
    V_MULTIPLICADOR NUMBER(2,1) := 1.0;
    V_CLASS VARCHAR2(20) := UPPER('&Classe'); 

    V_ATAQUE_CRITICO BOOLEAN := FALSE;
    V_HP NUMBER(3) := 100;
    v_POCAO_ATIVA BOOLEAN := FALSE; -- Digtar só "PF" para Poção de Fúria
    IS_FLANKING BOOLEAN := '&Is_flanking'; -- Simula se o personagem está flanqueando o inimigo
    V_ARMA BOOLEAN := FALSE; 
    V_CLIMA BOOLEAN := FALSE;
    
BEGIN
    -- RN 1: Multiplicador de dano
    V_MULTIPLICADOR := CASE V_CLASS
        WHEN 'GUERREIRO' THEN 1.2;
        WHEN 'MAGO' THEN 1.5;
        WHEN 'LADINO' THEN 1.8;
        WHEN 'PALADINO' THEN 1.1;
    END;
        DBMS_OUTPUT.PUT_LINE('Multiplicador de dano para ' || V_CLASS || ': ' || V_MULTIPLICADOR);
    END CASE;

    -- RN 2: Acerto crítico
    IF (V_HP <= 15) AND (v_V_POCAO_ATIVA = 'PF') THEN
        DBMS_OUTPUT.PUT_LINE('Acerto crítico ativado! Dano aumentado em 50%');
    ELSIF (V_CLASS = 'LADINO') AND (is_flanking = TRUE) THEN
        DBMS_OUTPUT.PUT_LINE('Ladino tem chance de acerto crítico aumentada!');
    ELSIF ()
    END IF;

END;