# Roadmap

Ultimo aggiornamento: 2026-11-14.

## Stato dei brani

| Brano | Demo | Live | Disco | Note |
|---|---|---|---|---|
| El Boogie Del Barbastrejo | ✅ | – | – | vedi domande aperte |
| E Allora | – | – | – | progetto Reaper `recording/EAllora`. In `chords/` c'è `PiangiSulTuoLetto.txt`: verificare se è lo stesso brano |
| Gipsy G | – | – | – | `recording/GipsyG` |
| L'Anguana | – | – | – | `recording/l'Anguana`. Synth dal vivo |
| Sequeri (Miracoi) | – | – | – | `recording/Sequeri`, tab in `chords/`. Synth dal vivo |
| Spezzato | – | – | – | `recording/Spezzato`, accordi in `chords/` |
| Watchin | – | – | – | `recording/Watchin`, accordi in `chords/` |

Su Drive ci sono anche "sorpreso e deluso", delle cover ("I fought the law") e la scaletta. Chiedere a Devis se vanno nel songbook.

## Domande aperte

### El Boogie Del Barbastrejo
- Riff e accordi delle sezioni diverse dal pre-chorus: il progetto Reaper non li contiene. Li scrive Devis, poi Claude li rivede.
- Pre-chorus: va scritto `G#` (come nel progetto) o `Ab`? Per ora `G#`.
- Il doc Drive `_Tab` ha un `[pau]` (pausa?) prima del RIT 03, che non è nella demo: probabilmente riguarda la versione live.
- Testo: "barbastrejio" nella prima metà del bridge (B) e "barbastrejo" altrove, lasciato com'è.

## Prossimi passi
1. Versione demo degli altri brani (procedura in `CLAUDE.md`).
2. Versioni live, partendo dalle demo. Fonti: Devis, la scaletta su Drive.
3. Creare `_template.cho` quando il formato si sarà stabilizzato su 2-3 brani.

## Idee rimandate
- **PDF**: in Inst e Pad il `{comment: ...}` divide in due la riga degli strumenti.
- **PDF**: diagrammi degli accordi per cigar box GDG (configurazione ChordPro con strumento a 3 corde) invece di disattivarli.
- **HTML**: vista su misura, ad esempio una timeline della forma, con le sezioni a colori e una riga per strumento. È stata messa da parte per ora a favore del PDF ChordPro.
- **Test** per `tools/rpp_arrangement.py` (oggi non ne ha).
- **`tools/rpp_arrangement.py`**: potrebbe estrarre anche la traccia `lyrics` (oggi si fa con il comando indicato in `CLAUDE.md`).
