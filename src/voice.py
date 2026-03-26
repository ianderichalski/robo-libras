import queue
import threading

from src.config import (
    VOICE_LANGUAGE,
    VOICE_ENERGY_THRESHOLD,
    VOICE_PAUSE_THRESHOLD,
    VOICE_LISTEN_TIMEOUT,
    VOICE_PHRASE_TIME_LIMIT,
    VOICE_CALIBRATION_DURATION,
)

class VoiceListener:
    """Escuta contínua do microfone em thread separada."""

    def __init__(self) -> None:
        self._running = threading.Event()
        self._queue: queue.Queue[tuple[str, str]] = queue.Queue()
        self._thread: threading.Thread | None = None

    @property
    def is_active(self) -> bool:
        return self._running.is_set()

    def start(self) -> None:
        if self._running.is_set():
            return
        self._running.set()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running.clear()

    def poll(self) -> list[tuple[str, str]]:
        """Retorna mensagens pendentes [(tipo, conteúdo), ...]."""
        messages = []
        while not self._queue.empty():
            try:
                messages.append(self._queue.get_nowait())
            except queue.Empty:
                break
        return messages

    def _loop(self) -> None:
        try:
            import speech_recognition as sr
        except ImportError:
            self._queue.put(("error", "Instale: pip install SpeechRecognition pyaudio"))
            return

        recognizer = sr.Recognizer()
        recognizer.energy_threshold = VOICE_ENERGY_THRESHOLD
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = VOICE_PAUSE_THRESHOLD

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=VOICE_CALIBRATION_DURATION)
            self._queue.put(("ready", "Microfone calibrado"))

            while self._running.is_set():
                try:
                    audio = recognizer.listen(
                        source,
                        timeout=VOICE_LISTEN_TIMEOUT,
                        phrase_time_limit=VOICE_PHRASE_TIME_LIMIT,
                    )
                    text = recognizer.recognize_google(audio, language=VOICE_LANGUAGE)
                    self._queue.put(("text", text))
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    self._queue.put(("warning", "Não entendi, tente novamente"))
                except sr.RequestError as e:
                    self._queue.put(("error", f"Erro na API: {e}"))
                except OSError as e:
                    self._queue.put(("error", str(e)))