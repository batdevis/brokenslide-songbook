# Formato dei brani BrokenSlide

Specifica per scrivere i brani in testo semplice.
I nomi di strumenti, voci e sezioni sono quelli del [glossario](GLOSSARY.md).

## Versioni

Ogni brano può avere tre versioni, in file distinti, che seguono la vita del brano:

| Versione | File | Fonte |
|---|---|---|
| **demo** | `<brano>.demo.cho` | la demo registrata in casa da Devis (progetto Reaper): struttura, tempo, testo e arrangiamento registrato |
| **live** | `<brano>.live.cho` | parte dalla demo e la adatta a come il trio ha sviluppato il brano in sala prove e lo suona dal vivo |
| **disco** | `<brano>.disco.cho` | la registrazione in studio (futura). Serve ai musicisti in studio: contiene le parti degli strumenti |

Si scrive prima la demo, che è oggettiva. La live si deriva dalla demo, la disco dalla live.
La versione si dichiara anche nell'intestazione con `{meta: version demo}`, `{meta: version live}` o `{meta: version disco}`.

È **ChordPro standard** ([chordpro.org](https://www.chordpro.org)) con alcune **estensioni `x_`**.
Le direttive `x_` sono il meccanismo di estensione previsto da ChordPro: i programmi che non le conoscono le ignorano, quindi ogni file resta un ChordPro valido e si può stampare con `chordpro <file>.cho`.

---

## 1. File

- Un brano per file, estensione `.cho`, codifica UTF-8.
- Nome del file in kebab-case, senza accenti, con la versione prima dell'estensione: `el-boogie-del-barbastrejo.demo.cho`, `l-anguana.live.cho`.

## 2. Intestazione

In testa al file vanno le direttive che valgono per tutto il brano.

| Direttiva | Obbl. | Significato | Esempio |
|---|---|---|---|
| `{title: ...}` | sì | titolo | `{title: L'Anguana}` |
| `{key: ...}` | no | tonalità | `{key: G}` |
| `{tempo: ...}` | no | BPM | `{tempo: 96}` |
| `{time: ...}` | no | metro | `{time: 4/4}` |
| `{duration: ...}` | no | durata indicativa (m:ss) | `{duration: 3:45}` |
| `{meta: tuning ...}` | sì | accordatura della cigar box, dalla corda più grave alla più acuta | `{meta: tuning GDG}` |
| `{meta: slide ...}` | no | uso dello slide: `yes`, `no`, `mixed` | `{meta: slide yes}` |
| `{meta: version ...}` | sì | `demo`, `live` o `disco` | `{meta: version demo}` |
| `{x_form: ...}` | sì | struttura sintetica del brano (vedi §4) | `{x_form: Intro V1 C V2 C Jam C Outro}` |

## 3. Sezioni

Ogni sezione si apre con `{start_of_<tipo>: <etichetta>}` e si chiude con `{end_of_<tipo>}`.

| Tipo | Uso |
|---|---|
| `verse` | strofa, ma anche intro, outro e break: è il contenitore generico |
| `chorus` | ritornello |
| `bridge` | ponte |
| `jam` | parte improvvisata o di durata aperta (sezione personalizzata) |
| `tab` | riff scritto in tablatura (vedi §6) |
| `grid` | griglia di accordi per battute (standard ChordPro) |

Le sezioni senza testo con accordi (intro, parti strumentali, outro) si scrivono come `grid`: una cella per battuta, un simbolo per tempo, `.` dove l'accordo continua.
Etichetta e dimensioni della griglia vanno come attributi: `shape="4x4"` vuol dire 4 battute da 4 tempi per riga.

```
{start_of_grid: label="Intro" shape="4x4"}
{x_bars: 4}
| G . . . | G . . . | G . . . | G . . . |
{end_of_grid}
```

Una riga può avere meno battute di quelle indicate in `shape`: 6 battute si scrivono come una riga da 4 più una da 2.

**Sezione con testo e griglia.** Se una sezione con testo ha bisogno anche della griglia (ad esempio per mostrare come gli accordi si distribuiscono sulle battute), la griglia va **dopo** la chiusura della sezione, senza `label`.
I blocchi non si possono annidare: una griglia dentro `start_of_chorus` … `end_of_chorus` dà errore in ChordPro e si stampa come testo.

```
{start_of_chorus: C}
{x_bars: 4}
[C]Aaaah
[Bb]ahhhh
[G]el boogie del barbastrejo
{end_of_chorus}
{start_of_grid: shape="4x4"}
| C . . . | Bb . . . | G . . . | G . . . |
{end_of_grid}
```

**Pausa.** Un silenzio di tutti che aggiunge tempo al brano è una sezione `Pau`: una griglia di una battuta da un tempo con `N.C.` (nessun accordo), più un `x_cue`. Va nel punto esatto della pausa, quindi anche in `x_form`.
Per una pausa di 2 tempi: `shape="1x2"` e `| N.C. . |`.

```
{start_of_grid: label="Pau" shape="1x1"}
{x_cue: tutti: 1 tempo di silenzio → C x4}
| N.C. |
{end_of_grid}
```

### Etichette

L'etichetta dà il nome alla sezione ed è lo stesso nome usato in `x_form`.

| Etichetta | Sezione |
|---|---|
| `Intro`, `Outro` | apertura, chiusura |
| `V1`, `V2`, … | strofe |
| `PC` | pre-ritornello |
| `C` | ritornello |
| `B` | ponte |
| `Solo` | assolo |
| `Jam` (`Jam1`, `Jam2`, …) | jam |
| `Brk` | break / stop / stacco |
| `Inst` | strofa o parte strumentale, senza voce |
| `Pad` | tappeto / groove senza voce, di solito prima di una ripresa |
| `Tag` | ripetizione finale di una frase |
| `Pau` | pausa: silenzio di tutti che aggiunge tempo al brano |

Altre etichette sono ammesse se sono brevi e senza spazi.
Unica eccezione: il suffisso di ripetizione `xN`, come in `x_form`. Ad esempio il ritornello alla prima comparsa si apre con `{start_of_chorus: C x2}` se lì si suona due volte.

Se una sezione torna identica, non riscriverla. Il ritornello si scrive una volta, alla sua prima comparsa, e nei punti in cui torna si richiama con `{chorus: <etichetta>}`.
L'etichetta del richiamo è libera e si usa per le ripetizioni, così il file e il PDF seguono l'ordine del brano:

```
{chorus: C x4}
# Reaper: rit 02
```

Le altre sezioni che tornano identiche restano solo in `x_form`.

## 4. `x_form`: la struttura del brano

È una sequenza di etichette separate da spazi, in ordine di esecuzione.
Il nome della direttiva viene dall'inglese *song form*; in italiano si dice struttura.
Il suffisso `xN` indica che la sezione si ripete N volte di fila.

```
{x_form: Intro V1 C V2 C Jam C x2 Outro}
```

Ogni etichetta usata in `x_form` deve corrispondere a una sezione del file.

## 5. Direttive dentro le sezioni

Messe dentro una sezione, valgono per quella sezione. Il testo è libero, salvo dove indicato.

| Direttiva | Significato | Esempio |
|---|---|---|
| `{x_bars: N}` | durata in battute di un passaggio della sezione. Le ripetizioni (`C x4`) stanno in `x_form` e nei richiami | `{x_bars: 16}` |
| `{x_bars: open}` | durata aperta, si chiude con un cue | `{x_bars: open}` |
| `{x_riff: <nome>}` | riff da suonare, definito in un blocco `tab` | `{x_riff: Riff A}` |
| `{x_cue: ...}` | segnale tra i musicisti. Forma consigliata: `chi: segnale → cosa succede` | `{x_cue: Devis: alza la cigar box → stop sul 4, poi C}` |
| `{x_dyn: ...}` | dinamica: `pp p mp mf f ff`, `→` per crescendo/diminuendo | `{x_dyn: p → ff}` |
| `{x_vox: ...}` | voce principale: tipo e trattamento (cantato, parlato, doppiata…) | `{x_vox: spoken + double}` |
| `{x_cbg: ...}` | parte della cigar box | `{x_cbg: riff x2, poi slide libero}` |
| `{x_gtr: ...}` | altre chitarre (12 corde, resonator…), di solito solo nelle versioni demo e disco | `{x_gtr: 12 corde + resonator}` |
| `{x_drums: ...}` | parte della batteria | `{x_drums: solo toms, niente crash e ride}` |
| `{x_bass: ...}` | parte del basso | `{x_bass: pedale su G}` |
| `{x_synth: ...}` | parte del synth | `{x_synth: drone, filtro che si apre}` |
| `{x_bv: ...}` | backing vocals | `{x_bv: Daniele sulle ultime due parole}` |

Per le note che non rientrano in nessuna direttiva si usa lo standard `{comment: ...}`, che viene anche stampato.

Le righe che iniziano con `#` sono commenti ChordPro e non vengono stampate. Si usano per:
- la fonte delle informazioni e i `TODO`;
- il nome del marker nella DAW che corrisponde alla sezione (`# Reaper: str 01`), così il file e il progetto restano allineati.

## 6. Riff in tablatura

I riff si scrivono in blocchi `tab` con un nome, definiti una volta sola (di solito subito dopo l'intestazione) e richiamati con `x_riff`.

- Una riga per corda, con l'**acuta in alto** (convenzione standard delle tablature).
- Ogni riga inizia con il nome della corda secondo `tuning`.
- `/` e `\` indicano lo slide verso l'alto o verso il basso.

```
{start_of_tab: Riff A}
G|0--3/5--3-0------|
D|-----------------|
G|-----------------|
{end_of_tab}
```

## 7. Accordi e testo

Standard ChordPro: l'accordo va tra parentesi quadre, subito prima della sillaba su cui cade.

```
[G]Testo della strofa che [C]va avanti
```

---

## Esempio completo

```chordpro
{title: Esempio}
{key: G}
{tempo: 96}
{time: 4/4}
{meta: tuning GDG}
{meta: slide yes}
{x_form: Intro V1 C V2 C Jam C x2 Outro}

{start_of_tab: Riff A}
G|0--3/5--3-0------|
D|-----------------|
G|-----------------|
{end_of_tab}

{start_of_verse: Intro}
{x_bars: 8}
{x_riff: Riff A}
{x_cbg: da sola per 4 battute}
{x_drums: entra alla battuta 5, kick e hi-hat}
{end_of_verse}

{start_of_verse: V1}
{x_bars: 16}
{x_bass: pedale su G}
[G]Testo della strofa qui...
{end_of_verse}

{start_of_chorus: C}
{x_bars: 8}
{x_bv: backing vocals sulle ultime due parole}
[C]Testo del rit[G]ornello
{end_of_chorus}

{start_of_verse: V2}
{x_bars: 16}
[G]Seconda strofa...
{end_of_verse}

{start_of_jam: Jam}
{x_bars: open}
{x_synth: drone, filtro che si apre}
{x_dyn: p → ff}
{x_cue: Devis: alza la cigar box → stop sul 4, poi C}
{end_of_jam}

{start_of_verse: Outro}
{x_bars: 4}
{x_riff: Riff A}
{x_cue: Daniele: rullata → accordo finale tenuto}
{end_of_verse}
```
