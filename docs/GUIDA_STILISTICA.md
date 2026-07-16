# Guida stilistica della localizzazione italiana

## Principio editoriale

Ogni stringa è tradotta e revisionata manualmente partendo dall'inglese della
build di riferimento. Le traduzioni comunitarie possono essere consultate, ma
non sono mai considerate corrette o approvate per il solo fatto di esistere.
Nessuno strumento può generare, parafrasare o approvare automaticamente testo
italiano.

Gli automatismi ammessi si limitano a inventario, confronto tra build,
classificazione, individuazione dei duplicati e controlli tecnici.

## Italiano e compatibilità con mappe e guide

I termini comuni inglesi vanno tradotti. Devono invece rimanere nella grafia e
con le maiuscole originali tutti i nomi canonici utili a riconoscere il lore o a
cercare informazioni nelle mappe, nelle guide e nella comunità anglofona:

- persone, pianeti, lune, sistemi, insediamenti e località con nome proprio;
- aziende, organizzazioni, fazioni, reparti e istituzioni;
- eventi, iniziative, pubblicazioni, opere narrative, programmi e slogan
  diegetici quando funzionano come titoli ufficiali;
- marchi e nomi canonici di veicoli, armi, armature, modelli, prodotti ed
  edizioni quando identificano una voce specifica;
- sigle canoniche dell'universo narrativo, come UEE, CDF, SCU e aUEC;
- codice, variabili, unità di misura e marcatori richiesti dal gioco.

I nomi ufficiali di città, avamposti, stazioni, cosmoporti e zone di interesse
restano integralmente originali anche quando contengono sostantivi comuni, per
esempio `August Dunlow Spaceport`, `Security Post Kareah` e `Ruin Station`.

Il descrittore funzionale che accompagna il nome resta italiano: per esempio
`Elmo Horizon`, `Sottotuta Beacon "Rust Society"` e `Livrea Foundation Fest`.
Colori e qualifiche puramente descrittive seguono invece la grammatica italiana
e rimangono minuscoli, come `Elmo Strata microTech nero`.

Prestiti ormai naturali per un giocatore italiano, come `Hangar` e `Multitool`, possono essere
mantenuti quando risultano più chiari e riconoscibili della traduzione. La scelta
si compie caso per caso e viene registrata nel glossario.

Nei menu di assegnazione dei comandi restano riconoscibili le legende fisiche
standard dei tasti e le relative forme brevi usate da hardware e guide, come
`Backspace`, `Delete`, `Home`, `End`, `Shift`, `Ctrl`, `Alt`, `Page Up`,
`Page Down`, `L-Shift` e `R-Shift`. Si traducono invece i descrittori funzionali,
le direzioni e i nomi estesi che non identificano una legenda, per esempio
`Freccia giù`, `Tastierino numerico`, `Barra spaziatrice` e `Rotella del mouse`.

I comandi digitabili, i sottocomandi e i nomi delle azioni richiamate dalla
barra obliqua restano identici alla sorgente, anche quando la chiave non mostra
esplicitamente `/`: per esempio `/partyinvite`, `addfriend`, `partyleave` e
`tell`. Tradurli ne impedirebbe l'esecuzione e renderebbe errate le guide. Si
traducono invece titoli, istruzioni, messaggi di esito e nomi descrittivi degli
argomenti, purché questi ultimi non siano marcatori interpretati dal gioco.

Un nome canonico o un prestito approvato non è considerato un residuo inglese.
Un termine tecnico comune o una voce d'interfaccia lasciati in inglese senza una
decisione esplicita, invece, costituiscono un errore.

## Registro

- Interfaccia: italiano sintetico, naturale e immediatamente comprensibile.
- Pulsanti: forma d'azione diretta, per esempio Accetta, Annulla, Conferma.
- Obiettivi: infinito presente, per esempio Raggiungere o Recuperare.
- Istruzioni: seconda persona singolare sottintesa, senza formule burocratiche.
- Comunicazioni diegetiche: tono coerente con mittente, fazione e situazione.
- Testi militari o istituzionali: autorevoli e concisi, senza calchi inglesi.
- Descrizioni commerciali: persuasive ma credibili, senza superlativi meccanici.

## Forma

- Usare la maiuscola solo dove richiesta dall'italiano; evitare il maiuscolo
  sistematico dei titoli inglesi.
- Conservare numeri, unità, simboli e spazi funzionali.
- Usare esclusivamente apostrofo e virgolette ASCII (`'` e `"`). Non usare
  caporali o virgolette tipografiche, per evitare caratteri non supportati dal
  font del gioco.
- Non aggiungere punteggiatura a etichette che nell'originale ne sono prive,
  salvo necessità grammaticale evidente.
- Preferire frasi italiane naturali ai calchi della sintassi inglese.

## Vincoli tecnici

Devono rimanere identici, inclusi maiuscole e argomenti:

- variabili come ~mission(Location|Address);
- marcatori come %s, %d e %ls;
- tag come <EM4> e </EM4>;
- sequenze come \n;
- identificatori tra parentesi graffe.

La traduzione può spostare un marcatore nella frase quando la grammatica lo
richiede, ma non può modificarlo, eliminarlo o duplicarlo.

## Segnaposto della sorgente

I segnaposto di sviluppo non autorizzano a inventare descrizioni mancanti.
Vanno revisionati singolarmente distinguendo due casi:

- i marcatori diagnostici o editoriali opachi, come `<-=MISSING=->`, `(PH)`,
  `[PH]`, `*WIP*`, `WIP`, `PH -` e `[PU]`, restano identici alla sorgente per
  conservarne la funzione tecnica e la riconoscibilità;
- il testo provvisorio potenzialmente visibile, come `DESCRIBE ME!` o
  `PLACEHOLDER TO BE FILLED IN`, può essere tradotto in modo letterale e
  conservativo, mantenendo invariati prefissi opachi, codici, numeri e nomi propri.

Non si introducono marcatori interni come `[PROV]` o `(PROV)` se non sono presenti
nella sorgente.

Una stringa provvisoria può essere approvata soltanto come segnaposto revisionato,
mai come sostituto di un contenuto definitivo non ancora fornito da CIG. Il
confronto tra build deve segnalarne ogni futura sostituzione.

## Contesto e duplicati

Le stringhe uguali non vengono approvate in blocco. Ogni chiave è controllata nel
proprio contesto: Power, per esempio, può significare Alimentazione, Potenza o
Energia. Una traduzione può essere propagata soltanto dopo aver verificato che
tutti i contesti siano equivalenti.

## Revisione

Una stringa passa allo stato approvato soltanto dopo:

1. confronto con la sorgente inglese;
2. applicazione del glossario;
3. controllo del contesto indicato dalla chiave;
4. verifica di marcatori, spazi e interruzioni di riga;
5. rilettura autonoma in italiano;
6. controllo dell'assenza di termini inglesi non protetti e della conservazione
   dei nomi canonici necessari alla compatibilità con mappe e guide.
