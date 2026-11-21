# Roadmap

Ultimo aggiornamento: 2026-11-21.

## Stato dei brani

| Brano | Demo | Live | Disco | Note |
|---|---|---|---|---|
| El Boogie Del Barbastrejo | ✅ | ✅ | – | vedi domande aperte |
| E Allora | – | – | – | progetto Reaper `recording/EAllora`. In `chords/` c'è `PiangiSulTuoLetto.txt`: verificare se è lo stesso brano |
| Gipsy G | – | – | – | `recording/GipsyG` |
| L'Anguana | – | – | – | `recording/l'Anguana`. Synth dal vivo |
| Sequeri (Miracoi) | – | – | – | `recording/Sequeri`, tab in `chords/`. Synth dal vivo |
| Spezzato | – | – | – | `recording/Spezzato`, accordi in `chords/` |
| Watchin | – | – | – | `recording/Watchin`, accordi in `chords/` |

Su Drive ci sono anche "sorpreso e deluso", delle cover ("I fought the law") e la scaletta. Chiedere a Devis se vanno nel songbook.

## Domande aperte

### El Boogie Del Barbastrejo
- Accordi scritti da Devis (2026-11-20) e verificati su Reaper (2026-11-21).
- Main riff (Intro e Inst, demo e live): manca la tablatura in un blocco `tab`.
- Live: il `[pau]` del doc Drive è una pausa di 1 tempo in più tra il bridge e l'ultimo chorus (sezione `Pause`).
- Live: struttura ricavata a orecchio dalla registrazione dell'Officina19 (2026-11-14), tempo 128 con tap tempo. Il finale è uno stop secco senza segnali.
- Testo: "barbastrejio" nella prima metà del bridge (B) e "barbastrejo" altrove, lasciato com'è.

## Prossimi passi
1. Versione demo degli altri brani (procedura in `CLAUDE.md`).
2. Versioni live, partendo dalle demo. Fonti: Devis, la scaletta su Drive.
3. Creare `_template.cho` quando il formato si sarà stabilizzato su 2-3 brani.

## Idee rimandate
- **PDF**: in Inst e Pad il `{comment: ...}` divide in due la riga degli strumenti.
- **PDF**: diagrammi degli accordi per cigar box GDG (configurazione ChordPro con strumento a 3 corde) invece di disattivarli.
- **HTML**: vista su misura, ad esempio una timeline della struttura, con le sezioni a colori e una riga per strumento. In prova (2026-11-21) il backend HTML di ChordPro (`render.py --format html`): da qui si può arrivare a un CSS nostro. Limite: i richiami `{chorus}` non compaiono. Scartato per ora ChordSheetJS 18.0.0: va in errore con alcuni commenti dentro le griglie (bug non segnalato), mostra le griglie come testo grezzo e riscrive `G#` in `Ab`.
- **Richiamo di sezioni diverse dal ritornello** (ad esempio una direttiva `x_`): oggi Inst e Pad della live di El Boogie sono riscritti perché ChordPro richiama solo il chorus. Da fare se i brani riscritti diventano tanti.
- **Test** per `tools/rpp_arrangement.py` (oggi non ne ha).
- **`tools/rpp_arrangement.py`**: potrebbe estrarre anche la traccia `lyrics` (oggi si fa con il comando indicato in `CLAUDE.md`).
