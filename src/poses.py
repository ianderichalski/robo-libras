Pose = dict[str, float]

FINGER_ORDER = ("polegar", "indicador", "medio", "anelar", "minimo")

POSES: dict[str, Pose] = {
    # números 0–5
    "0": {"polegar": 1,    "indicador": 1,    "medio": 1,    "anelar": 1,    "minimo": 1},
    "1": {"polegar": 1,    "indicador": 0,    "medio": 1,    "anelar": 1,    "minimo": 1},
    "2": {"polegar": 1,    "indicador": 0,    "medio": 0,    "anelar": 1,    "minimo": 1},
    "3": {"polegar": 1,    "indicador": 0,    "medio": 0,    "anelar": 0,    "minimo": 1},
    "4": {"polegar": 1,    "indicador": 0,    "medio": 0,    "anelar": 0,    "minimo": 0},
    "5": {"polegar": 0,    "indicador": 0,    "medio": 0,    "anelar": 0,    "minimo": 0},

    # vogais
    "A": {"polegar": 0,    "indicador": 1,    "medio": 1,    "anelar": 1,    "minimo": 1},
    "E": {"polegar": 0.33, "indicador": 0.66, "medio": 0.66, "anelar": 0.66, "minimo": 0.66},
    "I": {"polegar": 0.66, "indicador": 1,    "medio": 1,    "anelar": 1,    "minimo": 0},
    "O": {"polegar": 0.66, "indicador": 0.66, "medio": 0.66, "anelar": 0.66, "minimo": 0.66},
    "U": {"polegar": 0.66, "indicador": 0,    "medio": 0,    "anelar": 1,    "minimo": 1},

    # consoantes
    "B": {"polegar": 0.66, "indicador": 0,    "medio": 0,    "anelar": 0,    "minimo": 0},
    "C": {"polegar": 0.33, "indicador": 0.33, "medio": 0.33, "anelar": 0.33, "minimo": 0.33},
    "D": {"polegar": 0.33, "indicador": 0,    "medio": 1,    "anelar": 1,    "minimo": 1},
    "F": {"polegar": 0.33, "indicador": 0.66, "medio": 0,    "anelar": 0,    "minimo": 0},
    "G": {"polegar": 0,    "indicador": 0,    "medio": 1,    "anelar": 1,    "minimo": 1},
    "H": {"polegar": 0.66, "indicador": 0,    "medio": 0,    "anelar": 1,    "minimo": 1},
    "J": {"polegar": 1,    "indicador": 1,    "medio": 1,    "anelar": 1,    "minimo": 0},
    "K": {"polegar": 0.33, "indicador": 0,    "medio": 0,    "anelar": 1,    "minimo": 1},
    "L": {"polegar": 0,    "indicador": 0,    "medio": 1,    "anelar": 1,    "minimo": 1},
    "M": {"polegar": 0.33, "indicador": 0,    "medio": 0,    "anelar": 0,    "minimo": 1},
    "N": {"polegar": 0.33, "indicador": 0,    "medio": 0,    "anelar": 1,    "minimo": 1},
    "P": {"polegar": 0.33, "indicador": 0,    "medio": 0,    "anelar": 1,    "minimo": 1},
    "Q": {"polegar": 0,    "indicador": 0,    "medio": 1,    "anelar": 1,    "minimo": 1},
    "R": {"polegar": 0.66, "indicador": 0.33, "medio": 0,    "anelar": 1,    "minimo": 1},
    "S": {"polegar": 1,    "indicador": 1,    "medio": 1,    "anelar": 1,    "minimo": 1},
    "T": {"polegar": 0.33, "indicador": 1,    "medio": 0,    "anelar": 0,    "minimo": 0},
    "V": {"polegar": 0.66, "indicador": 0,    "medio": 0,    "anelar": 1,    "minimo": 1},
    "W": {"polegar": 0.66, "indicador": 0,    "medio": 0,    "anelar": 0,    "minimo": 1},
    "X": {"polegar": 1,    "indicador": 0.33, "medio": 1,    "anelar": 1,    "minimo": 1},
    "Y": {"polegar": 0,    "indicador": 1,    "medio": 1,    "anelar": 1,    "minimo": 0},
    "Z": {"polegar": 0.66, "indicador": 0,    "medio": 1,    "anelar": 1,    "minimo": 1},

    # espaço (mão aberta — pausa visual)
    " ": {"polegar": 0, "indicador": 0, "medio": 0, "anelar": 0, "minimo": 0},
}

WORD_TO_DIGIT: dict[str, str] = {
    "um": "1", "uma": "1",
    "dois": "2", "duas": "2",
    "três": "3", "tres": "3",
    "quatro": "4",
    "cinco": "5",
    "zero": "0", "nada": "0",
}

def normalize_text(text: str) -> str:
    """Converte palavras numéricas para dígitos. Ex: 'um dois três' → '1 2 3'."""
    words = text.lower().split()
    return " ".join(WORD_TO_DIGIT.get(w, w) for w in words)

def get_pose(char: str) -> Pose | None:
    return POSES.get(char.upper())