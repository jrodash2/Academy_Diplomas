import random

from .models import FraseMotivacional


def frase_motivacional(request):
    frases = list(FraseMotivacional.objects.all())
    frase = random.choice(frases) if frases else None
    return {
        "frase_motivacional": frase,
        "frase_del_dia": frase,
    }
