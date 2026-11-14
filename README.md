# BrokenSlide Songbook

La struttura dei brani di **BrokenSlide**, progetto Psych Garage Blues: forma, testo, accordi, riff e arrangiamento, in testo semplice.

Formazione attuale:
- Devis Battisti: voce e cigar box
- Daniele Maniero: batteria e cori
- Livio Savioli: basso e synth

Sito: https://brokenslideband.web.app/

## Formato

I brani sono scritti in [ChordPro](https://www.chordpro.org), un formato aperto, con alcune estensioni `x_` per quello che lo standard non copre: forma sintetica, battute, cue, parti dei singoli strumenti.
La specifica completa è in [FORMAT.md](FORMAT.md).

Ogni brano può avere due versioni:

| File | Contenuto |
|---|---|
| `<brano>.disco.cho` | il brano come registrato, ricavato dal progetto Reaper |
| `<brano>.live.cho` | il brano come lo suona il trio dal vivo, ricavato dalla versione disco |

## Brani

| Brano | Disco | Live |
|---|---|---|
| El Boogie Del Barbastrejo | [sì](el-boogie-del-barbastrejo.disco.cho) | – |

## Stampare un brano

Con il programma di riferimento ChordPro (open source):

```sh
chordpro el-boogie-del-barbastrejo.disco.cho   # genera il PDF
```

Le direttive `x_` vengono ignorate in stampa. Le righe `#` sono commenti.

## Strumenti

`tools/rpp_arrangement.py` legge un progetto Reaper (`.RPP`) e mostra, per ogni sezione definita dai marker, quali tracce suonano e per quanta parte della sezione. Tiene conto dei mute e delle automazioni di volume.

```sh
python3 tools/rpp_arrangement.py <percorso>/<Brano>.RPP
```

Richiede solo Python 3, senza dipendenze esterne.
