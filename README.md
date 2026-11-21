# BrokenSlide Songbook

I brani di **BrokenSlide**, progetto Psych Garage Blues, in testo semplice: struttura, testo, accordi, riff e arrangiamento.

Formazione attuale:
- Devis Battisti: voce e cigar box
- Daniele Maniero: batteria e cori
- Livio Savioli: basso e synth

Sito: https://brokenslideband.web.app/

## Formato

I brani sono scritti in [ChordPro](https://www.chordpro.org), un formato aperto, con alcune estensioni `x_` per quello che lo standard non copre: struttura sintetica, battute, cue, parti dei singoli strumenti.
La specifica completa è in [FORMAT.md](FORMAT.md), i termini da usare in [GLOSSARY.md](GLOSSARY.md).

Ogni brano può avere tre versioni:

| File | Contenuto |
|---|---|
| `<brano>.demo.cho` | la demo registrata in casa da Devis, ricavata dal progetto Reaper |
| `<brano>.live.cho` | il brano come lo suona il trio dal vivo, sviluppato in sala prove partendo dalla demo |
| `<brano>.disco.cho` | il brano registrato in studio (futuro), con le parti degli strumenti |

## Brani

| Brano | Demo | Live | Disco |
|---|---|---|---|
| El Boogie Del Barbastrejo | [sì](el-boogie-del-barbastrejo.demo.cho) | [sì](el-boogie-del-barbastrejo.live.cho) | – |

## Stampare un brano in PDF

```sh
python3 tools/render.py el-boogie-del-barbastrejo.demo.cho
# → pdf/el-boogie-del-barbastrejo.demo.pdf  (oppure: -o <file.pdf>)
```

ChordPro da solo ignora le direttive `x_`. `tools/render.py` le converte prima in commenti ChordPro, così nel PDF compaiono:
- una riga compatta per sezione con battute e parti degli strumenti
- i cue in un riquadro
- in testa al brano tonalità, tempo, accordatura e struttura

I diagrammi degli accordi sono disattivati, perché quelli di ChordPro sono per la chitarra a 6 corde. I PDF generati sono nel repository, in `pdf/`: dopo aver modificato un brano, rigenera il suo PDF prima del commit.

Serve il comando `chordpro` nel `PATH`. Su Linux il modo più semplice è l'AppImage ufficiale, dalle [release di ChordPro](https://github.com/ChordPro/chordpro/releases): scegli `wk4.1` sulle distro recenti (ad esempio Ubuntu 24.04) e crea un link che si chiami `chordpro`:

```sh
chmod +x ChordPro-*.AppImage
ln -s "$PWD/ChordPro-<versione>-wk4.1.AppImage" ~/.local/bin/chordpro
```

Il link deve chiamarsi esattamente `chordpro`, perché è il nome con cui l'AppImage capisce di dover usare la riga di comando invece dell'interfaccia grafica.

## Strumenti

`tools/rpp_arrangement.py` legge un progetto Reaper (`.RPP`) e mostra, per ogni sezione definita dai marker, quali tracce suonano e per quanta parte della sezione. Tiene conto dei mute e delle automazioni di volume.

```sh
python3 tools/rpp_arrangement.py <percorso>/<Brano>.RPP
```

Gli script richiedono solo Python 3, senza dipendenze esterne.

## Test

```sh
python3 -m unittest discover tests
```

I test non avviano mai programmi esterni: `chordpro` è simulato, e qualunque altra chiamata a un processo fa fallire il test.
