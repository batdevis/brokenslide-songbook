# BrokenSlide Songbook: istruzioni per Claude

Struttura dei brani di BrokenSlide in ChordPro esteso. Si lavora in italiano.
Il contesto sulla band e sulle fonti (Reaper, Google Drive con `gws`) è nel `CLAUDE.md` della cartella madre `BrokenSlide/`.
Lo stato del lavoro e i prossimi passi sono in [ROADMAP.md](ROADMAP.md): leggerlo a inizio sessione e aggiornarlo a fine sessione.

## File
```
FORMAT.md                  # specifica del formato: riferimento principale, aggiornarlo se il formato cambia
README.md                  # per chi legge il repo: brani, stampa, strumenti, test
ROADMAP.md                 # stato dei brani, domande aperte, prossimi passi
<brano>.disco.cho          # versione disco
<brano>.live.cho           # versione live (nessuna ancora)
tools/rpp_arrangement.py   # .RPP → tempo, sezioni (marker) e tracce attive per sezione
tools/render.py            # .cho → pdf/<brano>.pdf via chordpro, con le x_ rese visibili
tests/                     # python3 -m unittest discover tests
pdf/                       # PDF generati, versionati
```

## Decisioni prese
- **Formato**: ChordPro standard più direttive `x_` (ignorate dagli altri programmi ChordPro). Righe `#` per fonti, TODO e nome del marker Reaper (`# Reaper: str 01`).
- **Due versioni per brano**: prima la **disco** (oggettiva, ricavata dal progetto Reaper), poi la **live** ricavata dalla disco. Dal vivo la forma a volte cambia.
- **Versione disco = solo fatti**: niente interpretazioni (ad esempio sulla dinamica) che non si leggano nel progetto o che Devis non abbia confermato.
- **Etichette delle sezioni**: Intro, V1…, PC, C, B1…, Solo, Inst, Brk, Pad, Jam, Tag, Outro. Il ritornello si scrive una volta, come frase, e si ripete in `x_form` con `C x2` / `C x4`.
- **Testo**: in dialetto veneto, va riportato **così com'è**. Non correggere l'ortografia senza chiedere.
- **Accordi fuori tonalità**: possono essere voluti (ad esempio il pre-chorus di El Boogie). Segnalarli con un commento, non correggerli.
- **PDF**: diagrammi degli accordi disattivati (quelli di ChordPro sono per chitarra a 6 corde). Le parti degli strumenti stanno in una riga compatta per sezione, i cue in un riquadro.

## Procedura: versione disco di un brano
1. **Sezioni e arrangiamento**: `python3 -I tools/rpp_arrangement.py ../recording/<Brano>/<Brano>.RPP`. Battute per sezione e tracce attive con la percentuale di copertura. Ignorare le coperture minime (code di item), indicare quelle parziali ("hi-hat (3 battute)").
2. **Testo dal progetto**, se c'è la traccia `lyrics`:
   ```sh
   f=../recording/<Brano>/<Brano>.RPP
   n=$(grep -n 'NAME lyrics' "$f" | head -1 | cut -d: -f1)
   m=$(awk -v n=$n 'NR>n && /^  <TRACK/{print NR; exit}' "$f")
   sed -n "${n},${m}p" "$f" | grep -E 'POSITION|LENGTH|<NOTES|^\s*\|'
   ```
3. **Verifica del testo** sul doc Drive `<Brano>_Tab` (via `gws`, sola lettura). Nella traccia `lyrics` possono mancare dei versi.
4. **Accordi e tab**: `../recording/<Brano>/chords/*.txt`, se esistono.
5. **Domande a Devis** per quello che il progetto non dice: tonalità, accordatura e slide, chi fa il solo, significato dei nomi delle tracce non ovvi.
6. **Scrittura**: `<brano>.disco.cho`, seguendo `FORMAT.md` e usando `el-boogie-del-barbastrejo.disco.cho` come esempio.
7. **Chiusura**: `python3 tools/render.py <brano>.disco.cho`, controllo del PDF (con `pdftoppm -r 70 -png` si può guardare la pagina), tabella dei brani in `README.md`, aggiornamento di `ROADMAP.md`.

## Git
- Remote `git@github.com:batdevis/brokenslide-songbook.git`, branch `main`.
- `user.email batdevis@gmail.com` impostato **in locale** nel repo (l'email globale è quella di lavoro).
- Commit e push **solo su richiesta esplicita** di Devis. Va bene proporre quando è il momento.
- Prima di un commit che tocca un brano: rigenerare il suo PDF e lanciare i test.

## Codice
- Python 3 senza dipendenze esterne. Test con `unittest`. Nei test i programmi esterni (`chordpro`) vanno simulati: c'è una guardia che fa fallire qualunque `subprocess.Popen` non simulato.
