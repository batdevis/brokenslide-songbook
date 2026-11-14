# Formato dei brani BrokenSlide

Specifica per scrivere la struttura dei brani in testo semplice.

## Versioni

Ogni brano può avere due versioni, in due file distinti:

| Versione | File | Fonte |
|---|---|---|
| **disco** | `<brano>.disco.cho` | il progetto Reaper: forma, tempo, testo e arrangiamento registrato |
| **live** | `<brano>.live.cho` | parte dalla versione disco e la adatta a come il trio suona il brano dal vivo |

Si scrive prima la versione disco, che è oggettiva. La versione live si deriva da quella.
La versione si dichiara anche nell'intestazione con `{meta: version disco}` o `{meta: version live}`.

È **ChordPro standard** ([chordpro.org](https://www.chordpro.org)) con alcune **estensioni `x_`**.
Le direttive `x_` sono il meccanismo di estensione previsto da ChordPro: i programmi che non le conoscono le ignorano, quindi ogni file resta un ChordPro valido e si può stampare con `chordpro <file>.cho`.

---

## 1. File

- Un brano per file, estensione `.cho`, codifica UTF-8.
- Nome del file in kebab-case, senza accenti, con la versione prima dell'estensione: `el-boogie-del-barbastrejo.disco.cho`, `l-anguana.live.cho`.

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
| `{meta: version ...}` | sì | `disco` o `live` | `{meta: version disco}` |
| `{x_form: ...}` | sì | forma sintetica del brano (vedi §4) | `{x_form: Intro V1 C V2 C Jam C Outro}` |

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

Altre etichette sono ammesse se sono brevi e senza spazi.

Se una sezione torna identica, non riscriverla: richiamala con `{chorus}` (per il ritornello) o lasciala solo in `x_form`.

## 4. `x_form`: la forma del brano

È una sequenza di etichette separate da spazi, in ordine di esecuzione.
Il suffisso `xN` indica che la sezione si ripete N volte di fila.

```
{x_form: Intro V1 C V2 C Jam C x2 Outro}
```

Ogni etichetta usata in `x_form` deve corrispondere a una sezione del file.

## 5. Direttive dentro le sezioni

Messe dentro una sezione, valgono per quella sezione. Il testo è libero, salvo dove indicato.

| Direttiva | Significato | Esempio |
|---|---|---|
| `{x_bars: N}` | durata in battute (totale, ripetizioni comprese) | `{x_bars: 16}` |
| `{x_bars: open}` | durata aperta, si chiude con un cue | `{x_bars: open}` |
| `{x_riff: <nome>}` | riff da suonare, definito in un blocco `tab` | `{x_riff: Riff A}` |
| `{x_cue: ...}` | segnale tra i musicisti. Forma consigliata: `chi: segnale → cosa succede` | `{x_cue: Devis: alza la cigar box → stop sul 4, poi C}` |
| `{x_dyn: ...}` | dinamica: `pp p mp mf f ff`, `→` per crescendo/diminuendo | `{x_dyn: p → ff}` |
| `{x_vox: ...}` | voce principale: tipo e trattamento (cantato, parlato, doppiata…) | `{x_vox: parlato + backing}` |
| `{x_cbg: ...}` | parte della cigar box | `{x_cbg: riff x2, poi slide libero}` |
| `{x_gtr: ...}` | altre chitarre (12 corde, resonator…), di solito solo nella versione disco | `{x_gtr: 12 corde + resonator}` |
| `{x_drums: ...}` | parte della batteria | `{x_drums: solo tom, niente piatti}` |
| `{x_bass: ...}` | parte del basso | `{x_bass: pedale su G}` |
| `{x_synth: ...}` | parte del synth | `{x_synth: drone, filtro che si apre}` |
| `{x_bv: ...}` | cori | `{x_bv: Daniele sulle ultime due parole}` |

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
{x_drums: entra alla battuta 5, cassa e charleston}
{end_of_verse}

{start_of_verse: V1}
{x_bars: 16}
{x_bass: pedale su G}
[G]Testo della strofa qui...
{end_of_verse}

{start_of_chorus: C}
{x_bars: 8}
{x_bv: cori sulle ultime due parole}
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
