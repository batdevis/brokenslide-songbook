# BrokenSlide Songbook: istruzioni per Claude

I brani di BrokenSlide in ChordPro esteso. Si lavora in italiano.
Il contesto sulla band e sulle fonti (Reaper, Google Drive con `gws`) è nel `CLAUDE.md` della cartella madre `BrokenSlide/`.
Lo stato del lavoro e i prossimi passi sono in [ROADMAP.md](ROADMAP.md): leggerlo a inizio sessione e aggiornarlo a fine sessione.

## File
```
FORMAT.md                  # specifica del formato: riferimento principale, aggiornarlo se il formato cambia
GLOSSARY.md                # termini da usare (in inglese) e sinonimi trovati nelle fonti
README.md                  # per chi legge il repo: brani, stampa, strumenti, test
ROADMAP.md                 # stato dei brani, domande aperte, prossimi passi
songs/<brano>/             # una cartella per brano (file piccoli; audio e video restano fuori da git)
  <brano>.demo.cho         # versione demo (registrata in casa da Devis)
  <brano>.live.cho         # versione live (come il trio lo suona dal vivo)
  <brano>.disco.cho        # versione disco, registrata in studio (futura)
tools/rpp_arrangement.py   # .RPP → tempo, sezioni (marker) e tracce attive per sezione
tools/render.py            # .cho (o una cartella, es. songs/) → out/html/<brano>.html via chordpro, poi out/pdf/<brano>.pdf stampando la pagina con Chromium headless
tools/html/*.css           # stile della pagina (chordpro.css) e della stampa/PDF (chordpro_print.css), copiati da render.py accanto alla pagina
tests/                     # python3 -m unittest discover tests
out/pdf/                   # PDF generati, versionati
out/html/                  # HTML generati, con i CSS copiati, versionati
```

## Decisioni prese
- **Formato**: ChordPro standard più direttive `x_` (ignorate dagli altri programmi ChordPro). Righe `#` per fonti, TODO e nome del marker Reaper (`# Reaper: str 01`).
- **Tre versioni per brano**, che seguono la vita del brano: **demo** (Devis la registra da solo in casa; oggettiva, ricavata dal progetto Reaper), **live** (il trio sviluppa il brano in sala prove partendo dalla demo; la struttura può cambiare), **disco** (registrazione in studio, futura).
- **Parti degli strumenti** (`x_cbg`, `x_gtr`, `x_bass`, `x_drums`…): servono nella demo e nella disco. Nella live non si mettono, salvo che non servano a chi suona.
- **Versione demo = solo fatti**: niente interpretazioni (ad esempio sulla dinamica) che non si leggano nel progetto o che Devis non abbia confermato.
- **Etichette delle sezioni**: Intro, V1…, PC, C, B (B1…), Solo, Inst, Brk, Pad, Jam, Tag, Outro. Il ritornello si scrive una volta, come frase, e si richiama con `{chorus: C}`. Le ripetizioni stanno in `{x_times: N}`, non nell'etichetta.
- **Struttura**: non si scrive a mano (niente `x_form`): `tools/render.py` la ricava dalle sezioni con etichetta e dai richiami, nell'ordine del file.
- **Termini**: strumenti, voci e sezioni si scrivono con i termini inglesi di `GLOSSARY.md`, il resto in italiano. Le etichette che `render.py` scrive nella pagina e nel PDF (Key, Tuning, Form, Cue, bars, Page…) sono in inglese; il contenuto del `.cho` (testo, note, cue) resta com'è scritto. Niente i18n finché non serve davvero. Un nome nuovo trovato nelle fonti va aggiunto al glossario.
- **Testo**: in dialetto veneto, va riportato **così com'è**. Non correggere l'ortografia senza chiedere.
- **Accordi fuori tonalità**: possono essere voluti (ad esempio il pre-chorus di El Boogie). Segnalarli con un commento, non correggerli.
- **HTML e PDF**: la pagina HTML la scrive ChordPro, il PDF è quella pagina stampata da Chromium headless (Chrome come ripiego). Lo stile sta solo nei CSS di `tools/html/`: scuro per lo schermo (palco, telefono e tablet), chiaro per la stampa. Diagrammi degli accordi disattivati (quelli di ChordPro sono per chitarra a 6 corde). Le parti degli strumenti stanno in una riga compatta per sezione, i cue in un riquadro.
- **Deploy futuro**: il progetto potrebbe finire su un server, magari con un editor. Scegliere strumenti che girano anche headless su Linux (ad esempio il pacchetto Debian `chromium`).

## Procedura: versione demo di un brano
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
6. **Scrittura**: `songs/<brano>/<brano>.demo.cho`, seguendo `FORMAT.md` e usando `songs/el-boogie-del-barbastrejo/el-boogie-del-barbastrejo.demo.cho` come esempio.
7. **Chiusura**: `python3 tools/render.py songs/<brano>/<brano>.demo.cho`, controllo della pagina e del PDF (con `pdftoppm -r 70 -png` si può guardare il PDF), tabella dei brani in `README.md`, aggiornamento di `ROADMAP.md`.

## Git
- Remote `git@github.com:batdevis/brokenslide-songbook.git`, branch `main`.
- `user.email batdevis@gmail.com` impostato **in locale** nel repo (l'email globale è quella di lavoro).
- Commit e push **solo su richiesta esplicita** di Devis. Va bene proporre quando è il momento.
- Prima di un commit che tocca un brano: rigenerare il suo PDF e il suo HTML e lanciare i test. Se cambia un CSS o `render.py`: `python3 tools/render.py songs/`.

## Codice
- Python 3 senza dipendenze esterne. Test con `unittest`. Nei test i programmi esterni (`chordpro`) vanno simulati: c'è una guardia che fa fallire qualunque `subprocess.Popen` non simulato.
