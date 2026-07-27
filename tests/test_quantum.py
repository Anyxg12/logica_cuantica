from quantum.circuits import comprobar_recuperacion


def test_recupera_estado_cero():
    conteos = comprobar_recuperacion(0, shots=100)

    assert conteos == {"000": 100}


def test_recupera_estado_uno():
    conteos = comprobar_recuperacion(1, shots=100)

    assert conteos == {"001": 100}