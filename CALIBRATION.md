# Calibração dos Servos

> ⚠️ Os ângulos definidos em `src/config.py` foram calibrados especificamente para o modelo de mão utilizado. Modelos com dimensões de articulação ou comprimento de tendão distintos **exigem recalibração individual**.

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

Ao concluir todos os dedos, o script imprime o bloco `SERVO_ANGLES` completo para substituição em `src/config.py`.

## Boas práticas

- Incremente o ângulo gradualmente (passos de 5°) e interrompa assim que o dedo atingir a posição desejada
- Não utilize 180° como padrão para a posição fechada — o limite seguro é o ângulo imediatamente anterior à resistência mecânica da articulação
- Um chiado leve em repouso é inerente ao SG90 e não indica defeito; chiado intenso em uma pose específica indica que o ângulo ultrapassa o limite físico do mecanismo