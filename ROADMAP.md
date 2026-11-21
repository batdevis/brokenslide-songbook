# Roadmap

Ultimo aggiornamento: 2026-11-21.

## Stato dei brani

| Brano | Demo | Live | Disco | Note |
|---|---|---|---|---|
| El Boogie Del Barbastrejo | ✅ | ✅ | – | vedi domande aperte |
| E Allora | – | – | – | progetto Reaper `recording/EAllora`. In `chords/` c'è `PiangiSulTuoLetto.txt`: verificare se è lo stesso brano |
| Gipsy G | – | – | – | `recording/GipsyG` |
| L'Anguana | ✅ | – | – | vedi domande aperte. Synth dal vivo |
| Sequeri | ✅ | ✅ | – | vedi domande aperte. Synth dal vivo |
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

### L'Anguana
- Demo (2026-11-21): il progetto Reaper non ha marker, le sezioni vengono dalla traccia lyrics. Tracce: kick in quarti, CBG GDG con slide (traccia `gtr`), voce. Tonalità G, strofe e PC |G|G|Bb|G| (Devis).
- Demo: accordi di Intro, Inst e PC5 scritti da Devis (2026-11-21).
- Testo dal doc Drive `L'Anguana_Tab`; nella traccia lyrics di Reaper diverse parole sono scritte diversamente (annotate nei commenti del `.cho`).
- Live: dal doc Drive ci sono uno `[strum x1]` dopo la prima parte di ogni strofa e un `[synth solo x16(?)]` dopo "El brodo de bojo", che nella demo non ci sono.

### Sequeri
- Demo (2026-11-21): tonalità G, strofa con il Main riff (tab di Devis, 4 battute x2) e accordi di Devis sul testo, rit e outro |F G F G|, CBG con slide + CBG dist (traccia `gtr drive`), basso, batteria a campioni.
- Testo: "sequeri miracoei" come nel doc Drive (Reaper e tab scrivono "miracoi"). Titolo: "Sequeri" (Devis, 2026-11-21).
- Outro: le tab in `chords/` dicono F G G#, Devis ha confermato |F G F G| come il rit.
- Live (2026-11-21, Devis): 76 BPM (tap tempo sulla registrazione), niente count-in, Main riff x2 nell'Intro e nell'Inst dopo V2 e V4, strofa di 4 battute (un verso per battuta del riff), Outro con solo di synth sul Main riff x16 che finisce sfumando. Durata 6:19 calcolata da battute e BPM, sfumato escluso.
- Demo da ricontrollare: in Reaper (90 BPM) un verso dura 2 battute e la strofa 8, con il riff x2. Nella live un verso è una battuta del riff. Forse le battute della demo vanno contate in un altro modo, o il riff nella demo è suonato più lento.

## Prossimi passi
1. Versione demo degli altri brani (procedura in `CLAUDE.md`).
2. Versioni live, partendo dalle demo. Fonti: Devis, la scaletta su Drive.
3. Creare `songs/_template.cho` quando il formato si sarà stabilizzato su 2-3 brani.

## Idee rimandate
- **Pagina**: in Inst e Pad il `{comment: ...}` divide in due la riga degli strumenti.
- **Diagrammi degli accordi** per cigar box GDG invece di disattivarli (ChordPro li fa per uno strumento a 3 corde, ma il PDF ora viene dall'HTML: da capire come).
- **HTML**: vista su misura, ad esempio una timeline della struttura, con le sezioni a colori e una riga per strumento. Dal 2026-11-21 pagina e PDF vengono dal backend HTML di ChordPro con CSS nostri (scuro e monospace per lo schermo, chiaro per la stampa); il PDF lo stampa Chromium headless. Griglie, nome dei riff in tablatura, richiami `{chorus}` e Struttura, che il backend scarta, li recupera `render.py`. Scartato per ora ChordSheetJS 18.0.0: va in errore con alcuni commenti dentro le griglie (bug non segnalato), mostra le griglie come testo grezzo e riscrive `G#` in `Ab`.
- **Richiamo di sezioni diverse dal ritornello** (ad esempio una direttiva `x_`): oggi Inst e Pad della live di El Boogie sono riscritti perché ChordPro richiama solo il chorus. Da fare se i brani riscritti diventano tanti.
- **Test** per `tools/rpp_arrangement.py` (oggi non ne ha).
- **`tools/rpp_arrangement.py`**: potrebbe estrarre anche la traccia `lyrics` (oggi si fa con il comando indicato in `CLAUDE.md`).
