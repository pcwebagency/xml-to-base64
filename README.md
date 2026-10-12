# XML to Base64

Piccola applicazione desktop (Tkinter) per convertire in Base64 file XML e XML firmati (`.xml.p7m`), ad esempio le fatture elettroniche, e per codificare/decodificare testo Base64.

## Funzionalità

- Caricamento di file `.xml` / `.p7m` e conversione del contenuto in Base64
- Codifica e decodifica di testo incollato
- Copia del risultato negli appunti
- Esportazione del risultato su file `.txt`

## Requisiti

- Python 3.8+ con Tkinter (incluso nelle distribuzioni standard di Python)

## Utilizzo

```bash
python3 xml_to_base64.py
```

## Build dell'app macOS

L'app può essere impacchettata con [PyInstaller](https://pyinstaller.org/) usando lo spec incluso:

```bash
pip install pyinstaller
pyinstaller "XML to Base64.spec"
```

Il risultato si trova in `dist/XML to Base64.app`.

## Autore

Ing. Carmine Palermo — PC Web Agency
