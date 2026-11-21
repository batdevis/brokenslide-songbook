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

Ogni brano ha una cartella `songs/<brano>/`, che può contenere tre versioni (e in futuro altri file piccoli del brano, ad esempio note o immagini; audio e video restano fuori dal repository):

| File | Contenuto |
|---|---|
| `<brano>.demo.cho` | la demo registrata in casa da Devis, ricavata dal progetto Reaper |
| `<brano>.live.cho` | il brano come lo suona il trio dal vivo, sviluppato in sala prove partendo dalla demo |
| `<brano>.disco.cho` | il brano registrato in studio (futuro), con le parti degli strumenti |

## Brani

| Brano | Demo | Live | Disco |
|---|---|---|---|
| El Boogie Del Barbastrejo | [sì](songs/el-boogie-del-barbastrejo/el-boogie-del-barbastrejo.demo.cho) | [sì](songs/el-boogie-del-barbastrejo/el-boogie-del-barbastrejo.live.cho) | – |
| L'Anguana | [sì](songs/l-anguana/l-anguana.demo.cho) | – | – |

## Pagina HTML e PDF di un brano

```sh
python3 tools/render.py songs/el-boogie-del-barbastrejo/el-boogie-del-barbastrejo.demo.cho
# → out/html/el-boogie-del-barbastrejo.demo.html  (pagina per telefono e tablet)
# → out/pdf/el-boogie-del-barbastrejo.demo.pdf    (la stessa pagina stampata)
python3 tools/render.py songs/el-boogie-del-barbastrejo/el-boogie-del-barbastrejo.demo.cho --format html   # solo la pagina
python3 tools/render.py songs/   # tutti i brani (i file che iniziano con _ , come i template, si saltano)
```

ChordPro da solo ignora le direttive `x_`. `tools/render.py` le converte prima in commenti ChordPro, così compaiono:
- una riga compatta per sezione con battute e parti degli strumenti
- i cue in un riquadro
- in testa al brano tonalità, tempo, accordatura e struttura (Key, BPM, Tuning, Form)

La pagina la scrive il backend HTML di ChordPro. Il PDF è la stessa pagina stampata da un browser headless: **Chromium** (open source; su Ubuntu `sudo snap install chromium`, su Debian il pacchetto `chromium`), oppure Google Chrome se Chromium non c'è. Il browser parte con un profilo temporaneo, senza toccare quelli personali.

Lo stile è tutto nei CSS di `tools/html/`, che `render.py` copia accanto alla pagina:
- `chordpro.css`: schermo. Scuro (per il palco) e monospace, pensato per telefono e tablet.
- `chordpro_print.css`: stampa e PDF. Colori chiari, formato A4, sezioni che non si spezzano tra due pagine; in fondo a ogni pagina artista · titolo a sinistra (il testo lo aggiunge `render.py`, prendendolo da `{artist}` e `{title}`) e numero di pagina a destra.

Per provare una modifica allo stile basta cambiare il CSS copiato in `out/html/` e ricaricare la pagina nel browser; alla fine si riporta la modifica in `tools/html/` (`render.py` sovrascrive le copie in `out/html/`).

I diagrammi degli accordi sono disattivati, perché quelli di ChordPro sono per la chitarra a 6 corde. HTML e PDF generati sono nel repository, in `out/`: dopo aver modificato un brano o un CSS, rigenerali prima del commit (dopo un CSS: `python3 tools/render.py songs/`).

Il backend HTML di ChordPro scarta le righe delle griglie, i richiami `{chorus}` e i `comment_box` fuori dalle sezioni (il Form): `render.py` li trasforma in sezioni personalizzate (`chordgrid`, `chorus_recall`, `form`, `box`) che arrivano nella pagina come `div` con la loro classe. Ignora anche `{artist}`, che `render.py` ripete come `{subtitle}` sotto il titolo. Aggiunge anche doctype e viewport, e toglie lo stile `@page` di ChordPro (intestazione e piè di pagina vengono da `chordpro_print.css`).

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
