# Roadmap

Ultimo aggiornamento: 2026-11-21.

## Stato dei brani

| Brano | Demo | Live | Disco | Note |
|---|---|---|---|---|
| El Boogie Del Barbastrejo | ✅ | ✅ | – | vedi domande aperte |
| E Allora | – | – | – | progetto Reaper `recording/EAllora`. In `chords/` c'è `PiangiSulTuoLetto.txt`: verificare se è lo stesso brano |
| Gipsy G | – | – | – | `recording/GipsyG` |
| L'Anguana | ✅ | ✅ | – | vedi domande aperte. Synth dal vivo |
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
- Live (2026-11-21, Devis): 72 BPM, Main riff sugli accordi della strofa (senza tab) x2 nell'Intro e una volta (Inst) dopo ogni strofa prima del PC, Inst2 di 2 battute dopo PC5, Solo di synth sul Main riff x16 prima di V6, da cui si esce con un segnale di Devis. Durata 8:53 calcolata da battute e BPM.
- Live: il Main riff non ha ancora una tablatura.

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
- **Pagine pubblicate**: un link "torna all'indice" in ogni pagina dei brani (oggi si torna indietro col browser).
- **Pagina**: in Inst e Pad il `{comment: ...}` divide in due la riga degli strumenti.
- **Diagrammi degli accordi** per cigar box GDG invece di disattivarli (ChordPro li fa per uno strumento a 3 corde, ma il PDF ora viene dall'HTML: da capire come).
- **HTML**: vista su misura, ad esempio una timeline della struttura, con le sezioni a colori e una riga per strumento. Dal 2026-11-21 pagina e PDF vengono dal backend HTML di ChordPro con CSS nostri (scuro e monospace per lo schermo, chiaro per la stampa); il PDF lo stampa Chromium headless. Griglie, nome dei riff in tablatura, richiami `{chorus}` e Struttura, che il backend scarta, li recupera `render.py`. Scartato per ora ChordSheetJS 18.0.0: va in errore con alcuni commenti dentro le griglie (bug non segnalato), mostra le griglie come testo grezzo e riscrive `G#` in `Ab`.
- **Richiamo di sezioni diverse dal ritornello** (idea di Devis, 2026-11-21; da fare più avanti). ChordPro richiama solo il chorus, quindi oggi si riscrivono le griglie che tornano: Inst e Pad nella live di El Boogie, i due Inst nella live di Sequeri (Intro e Outro hanno la stessa griglia). Il riff in tablatura si richiama già con `x_riff`: qui si tratta della griglia che lo accompagna. Proposta:
  - direttiva `{x_recall: <etichetta>}`, seguita se serve da `{x_times: N}`, come `{chorus}`;
  - cerca la sezione **per etichetta** (non l'ultima come `{chorus}`), quindi si può richiamare anche l'Intro;
  - `render.py` la mette nel Form e nella pagina mostra l'etichetta (`Inst x2`) o ricopia la griglia intera (per il palco forse meglio la griglia);
  - gli altri programmi ChordPro ignorano le `x_`: lì la sezione richiamata non compare, il file resta valido;
  - da aggiornare: `FORMAT.md` §3, `render.py`, i test, e poi le live di El Boogie e Sequeri.
- **Test** per `tools/rpp_arrangement.py` (oggi non ne ha).
- **`tools/rpp_arrangement.py`**: potrebbe estrarre anche la traccia `lyrics` (oggi si fa con il comando indicato in `CLAUDE.md`).
