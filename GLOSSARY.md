# Glossario

Nei progetti Reaper, nei doc su Drive e a voce la stessa cosa ha nomi diversi.
Nei file del songbook si usa **sempre il termine della colonna "Termine"**, in inglese. Il resto del testo (commenti, note) è in italiano.
Anche le etichette che `tools/render.py` scrive nella pagina e nel PDF sono in inglese (ad esempio Key, Tuning, Form, Cue).

La colonna "Sinonimi" serve a riconoscere i nomi che si trovano nelle fonti (tracce e marker Reaper, doc Drive) e a tradurli.
Se nelle fonti compare un nome nuovo, aggiungerlo qui come sinonimo o come termine.

## Strumenti

| Termine | Abbreviazione | Sinonimi | Note |
|---|---|---|---|
| cigar box guitar | CBG | cigar box | quella di Devis, accordata GDG |
| distorted CBG | CBG dist | cigar box distorta | |
| 12-string guitar | 12-string | 12 str, 12 corde | solo nelle registrazioni |
| resonator | – | rezo, dobro, resofonica | solo nelle registrazioni |
| guitar | gtr | chitarra | chitarra generica |
| bass | – | basso, bass guitar | |
| synth | – | synthetizer, sintetizzatore | dal vivo solo in L'Anguana e Sequeri |
| keyboards | keys | tastiera, piano | |
| slide | – | bottleneck | |
| tin can mic | – | can, voice can | microfono autocostruito con una lattina, suona come un megafono ([esempio](https://www.instructables.com/The-New-and-Improved-Tin-Can-Microphone/)) |

## Batteria

| Termine | Sinonimi | Note |
|---|---|---|
| drums | batteria, drum | lo strumento intero |
| kick | cassa, kick - stem | |
| snare | rullante | |
| hi-hat | charleston, hh | |
| crash | piatti (generico) | |
| ride | piatti (generico) | |
| toms | tom, timpano | |
| fill | rullata | |
| claps | battimani, voice clap | |

## Voci

| Termine | Sinonimi | Note |
|---|---|---|
| lead vocal | voce, voice, voice str, voice last try | in E Allora anche le varianti "voce str graff" (graffiata), "voce str suss" (sussurrata), "voce rit urla" (urlata), sovrapposte alla lead vocal |
| double | doppia voce, double track | la stessa voce registrata due volte |
| backing vocals | cori, bv, voice backing | |
| spoken | parlato, voice spoken | |

## Sezioni

L'etichetta è quella usata nei file (vedi [FORMAT.md](FORMAT.md)).

| Termine | Etichetta | Sinonimi |
|---|---|---|
| intro | Intro | |
| verse | V1, V2… | strofa, str, STR |
| pre-chorus | PC | pre chorus |
| chorus | C | ritornello, rit, RIT |
| bridge | B (B1, B2… se più di uno) | ponte, closing |
| break | Brk | stacco |
| instrumental | Inst | strumentale, str no voce |
| solo | Solo | assolo |
| pad | Pad | boogie pad |
| jam | Jam | |
| tag | Tag | |
| outro | Outro | final, finale, coda |
| pause | Pause | pau, [pau], pausa |

## Esecuzione e struttura

| Termine | Sinonimi | Note |
|---|---|---|
| form | struttura, forma | sequenza delle sezioni in ordine di esecuzione, ricavata dalle sezioni, vedi §4 di [FORMAT.md](FORMAT.md) |
| bar | battuta, misura | |
| count-in | conteggio | "un, due, tre, quattro" prima di partire |
| cue | segnale, attacco | segnale tra i musicisti, vedi `x_cue` in [FORMAT.md](FORMAT.md) |
| stop | stacco secco, fermata | |
| riff | giro (quando è un riff) | |
| main riff | riff principale | il riff che caratterizza il brano; nei file si richiama con `{x_riff: Main riff}` |
| tuning | accordatura | es. GDG |
| key | tonalità | |
