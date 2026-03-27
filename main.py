#!/usr/bin/env python3

import sys
import time

from src.config import SERIAL_PORT
from src import servo
from src.poses import normalize_text
from src.speller import spell, format_pose_line
from src.voice import VoiceListener

def _print_header(mode: str) -> None:
    print(f"\n{'=' * 52}")
    print(f"  RoboLibras ({mode})")
    print(f"  Legenda: ab=aberto  po=pouco  me=meio  fe=fechado")
    print(f"{'=' * 52}\n")


def _on_char(c: str, p: dict | None) -> None:
    if p:
        print(format_pose_line(c, p))
    else:
        print("   ··· pausa ···")

# modo voz
def run_voice() -> None:
    _print_header("Modo Voz")
    listener = VoiceListener()
    listener.start()

    try:
        while True:
            for msg_type, content in listener.poll():
                if msg_type == "text":
                    print(f'Reconhecido: "{content}"')
                    spell(
                        content,
                        apply_fn=servo.apply_pose,
                        rest_fn=servo.open_hand,
                        on_char=_on_char,
                    )
                elif msg_type == "ready":
                    print("Pronto! Fale números ou letras. Ctrl+C para sair.\n")
                elif msg_type in ("error", "warning"):
                    print(f"   ⚠ {content}")

            time.sleep(0.1)
    except KeyboardInterrupt:
        listener.stop()
        print("\nEncerrando...")
        servo.open_hand()

# modo texto
def run_text() -> None:
    _print_header("Modo Texto")
    print("  Ctrl+C para sair.\n")

    while True:
        try:
            entry = input("Digite: ").strip()
            if entry:
                normalized = normalize_text(entry)
                print(f'\nSoletreando: "{normalized}"')
                spell(
                    entry,
                    apply_fn=servo.apply_pose,
                    rest_fn=servo.open_hand,
                    on_char=_on_char,
                )
                print("Pronto!\n")
        except KeyboardInterrupt:
            print("\nEncerrando...")
            servo.open_hand()
            break

# modo câmera
def run_camera() -> None:
    from src.camera import run
    run()

# menu
def main() -> None:
    print(f"\n{'=' * 52}")
    print("  RoboLibras")
    print(f"{'=' * 52}")
    print(f"  Porta serial: {SERIAL_PORT}")
    print()

    try:
        servo.connect(SERIAL_PORT)
    except Exception as e:
        print(f"  Erro ao conectar em {SERIAL_PORT}: {e}")
        sys.exit(1)
    print("  Arduino conectado!\n")

    while True:
        print(f"{'─' * 40}")
        print("  1. Modo Voz    (microfone)")
        print("  2. Modo Texto  (digitar)")
        print("  3. Modo Câmera (espelhamento)")
        print("  4. Teste dos servos")
        print("  0. Sair")
        print(f"{'─' * 40}")

        choice = input("  Escolha: ").strip()

        if choice == "1":
            run_voice()
        elif choice == "2":
            run_text()
        elif choice == "3":
            run_camera()
        elif choice == "4":
            servo.test_all()
        elif choice == "0":
            servo.open_hand()
            print("Até logo!")
            sys.exit(0)
        else:
            print("  Opção inválida.")

if __name__ == "__main__":
    main()