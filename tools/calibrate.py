#!/usr/bin/env python3

import argparse
import time

from pyfirmata import Arduino, SERVO

from src.config import SERIAL_PORT, FINGER_PINS, SERVO_ANGLES

_calibration = {
    name: dict(SERVO_ANGLES[pin])
    for name, pin in FINGER_PINS.items()
}

def _move(board: Arduino, pin: int, angle: int) -> int:
    angle = max(0, min(180, angle))
    board.digital[pin].write(angle)
    time.sleep(0.05)
    return angle

def _bar(angle: int, width: int = 36) -> str:
    p = int(angle / 180 * width)
    return "[" + "█" * p + "─" * (width - p) + f"] {angle:3d}°"

def _calibrate_finger(board: Arduino, name: str, pin: int) -> None:
    cal = _calibration[name]
    angle = _move(board, pin, cal["aberto"])

    print(f'\n{"=" * 56}')
    print(f"  Calibrando: {name.upper()}  (pino {pin})")
    print(f'{"=" * 56}')
    print("  d/a = ±1°  |  D/A = ±10°")
    print("  1=salvar ABERTO  2=salvar POUCO  3=salvar MEIO  4=salvar FECHADO")
    print("  t=testar sequência  q=próximo dedo")
    print(f'{"=" * 56}\n')

    while True:
        print(
            f"\r  {_bar(angle)}  "
            f'Ab:{cal["aberto"]:3d} Po:{cal["pouco"]:3d} '
            f'Me:{cal["meio"]:3d} Fe:{cal["fechado"]:3d}  ',
            end="", flush=True,
        )

        try:
            cmd = input("\n  Comando: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if cmd == "d":
            angle = _move(board, pin, angle + 1)
        elif cmd == "a":
            angle = _move(board, pin, angle - 1)
        elif cmd == "D":
            angle = _move(board, pin, angle + 10)
        elif cmd == "A":
            angle = _move(board, pin, angle - 10)
        elif cmd == "1":
            cal["aberto"] = angle
            print(f"  ABERTO={angle}°")
        elif cmd == "2":
            cal["pouco"] = angle
            print(f"  POUCO={angle}°")
        elif cmd == "3":
            cal["meio"] = angle
            print(f"  MEIO={angle}°")
        elif cmd == "4":
            cal["fechado"] = angle
            print(f"  FECHADO={angle}°")
        elif cmd == "t":
            print("  Testando...")
            for pos in ("aberto", "pouco", "meio", "fechado", "aberto"):
                _move(board, pin, cal[pos])
                time.sleep(0.9)
            angle = cal["aberto"]
        elif cmd == "q":
            print(f"\n  {name.upper()} confirmado.\n")
            break

def _print_result() -> None:
    print(f"\n{'=' * 56}")
    print("  Cole em SERVO_ANGLES no src/config.py:")
    print(f"{'=' * 56}\n")
    print("SERVO_ANGLES = {")
    for name, pin in FINGER_PINS.items():
        cal = _calibration[name]
        print(
            f'    {pin}: {{"aberto": {cal["aberto"]:3d}, "pouco": {cal["pouco"]:3d}, '
            f'"meio": {cal["meio"]:3d}, "fechado": {cal["fechado"]:3d}}},  # {name}'
        )
    print("}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Calibração dos servos da mão robótica")
    parser.add_argument("--port", default=SERIAL_PORT, help=f"Porta serial (padrão: {SERIAL_PORT})")
    args = parser.parse_args()

    board = Arduino(args.port)
    for pin in FINGER_PINS.values():
        board.digital[pin].mode = SERVO

    print(f'{"=" * 56}')
    print("  CALIBRAÇÃO —  RoboLibras")
    print("  Valores iniciais carregados de src/config.py.")
    print("  Ajuste apenas os dedos que precisar.")
    print(f'{"=" * 56}')
    input("\n  Enter para começar...")

    for name, pin in FINGER_PINS.items():
        _calibrate_finger(board, name, pin)

    _print_result()

    for name, pin in FINGER_PINS.items():
        _move(board, pin, _calibration[name]["aberto"])

if __name__ == "__main__":
    main()