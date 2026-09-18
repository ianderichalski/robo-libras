# Calibração dos Servos

> ⚠️ Os ângulos definidos em `src/config.py` foram calibrados especificamente para o modelo de mão utilizado. Modelos com dimensões de articulação ou comprimento de tendão distintos **exigem recalibração individual**.

## Codificação das poses

Cada caractere é representado como um vetor de 5 valores discretos (um por dedo), mapeados a ângulos de servo na tabela `SERVO_ANGLES` em `src/config.py`:

| Valor | Estado | Descrição |
|---|---|---|
| `0` | ○ Aberto | Dedo totalmente estendido |
| `0.33` | ◔ Pouco | Leve curvatura (~33% do range) |
| `0.66` | ◑ Meio | Semiflexão (~66% do range) |
| `1` | ● Fechado | Flexão máxima |

**Exemplo — letra L:**

```python
{"polegar": 0, "indicador": 0, "medio": 1, "anelar": 1, "minimo": 1}
#  ○ aberto      ○ aberto      ● fechado   ● fechado   ● fechado
```

O dicionário completo de poses (`src/poses.py`) cobre as **26 letras** do alfabeto manual da LIBRAS (A–Z), além dos dígitos 0–5 como suporte extra.

## Executar o calibrador

```bash
python -m tools.calibrate
python -m tools.calibrate --port COM3   # porta alternativa
```

## Controles interativos

| Tecla | Ação |
|---|---|
| `d` / `a` | Incrementa / decrementa ±1° |
| `D` / `A` | Incrementa / decrementa ±10° |
| `1` | Salva ângulo atual como **aberto** |
| `2` | Salva ângulo atual como **pouco** |
| `3` | Salva ângulo atual como **meio** |
| `4` | Salva ângulo atual como **fechado** |
| `t` | Executa sequência de teste completa do dedo |
| `q` | Confirma dedo atual e avança ao próximo |

A sequência de calibração segue a ordem: **polegar > indicador > médio > anelar > mínimo**.

Ao concluir todos os dedos, o script imprime o bloco `SERVO_ANGLES` completo para substituição em `src/config.py`.

## Boas práticas

- Incremente o ângulo gradualmente (passos de 5°) e interrompa assim que o dedo atingir a posição desejada
- Não utilize 180° como padrão para a posição fechada — o limite seguro é o ângulo imediatamente anterior à resistência mecânica da articulação
- Vibração leve em repouso é característica do SG90 e não indica defeito; vibração intensa em uma pose específica indica que o ângulo ultrapassa o limite físico do mecanismo