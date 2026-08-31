# Star Citizen — Traduzione italiana non ufficiale

Localizzazione italiana completa per **Star Citizen LIVE 4.10**, con installer
Windows in un unico file, backup automatico e ripristino.

> **Traduzione fan non ufficiale e non commerciale.** Il progetto non è
> approvato, sponsorizzato o affiliato a Cloud Imperium Games o Roberts Space
> Industries.

## Scarica e installa

### 1. Scarica un solo file

[**Scarica l'ultima versione da GitHub Releases**](https://github.com/Sici29/SC-Italian-Translation/releases/latest)

Il file da scaricare è:

```text
StarCitizen_Traduzione_Italiana_4.10_R1.exe
```

### 2. Chiudi gioco e launcher

Chiudi completamente **Star Citizen** e **RSI Launcher**.

### 3. Apri l'installer

Fai doppio clic sull'EXE e premi **Invio**. L'installer:

- trova automaticamente la cartella `LIVE`;
- verifica il contenuto della localizzazione inglese installata;
- controlla l'integrità delle 90.363 stringhe italiane incorporate;
- crea un backup prima di modificare qualsiasi file;
- installa la lingua italiana mantenendo l'audio inglese;
- verifica nuovamente file e configurazione al termine;
- controlla all'avvio se su GitHub esiste una revisione più recente;
- se la trova, può scaricarla, verificarne dimensione e SHA-256 e avviarla
  direttamente, senza aprire il browser.

Non servono Python, archivi da estrarre o modifiche manuali.

> **Passaggio dalla R4 alla 4.10-R1:** la R4 non contiene ancora il sistema di
> aggiornamento automatico, quindi la 4.10-R1 va scaricata manualmente
> un'ultima volta. Dalla 4.10-R1 in avanti l'installer potrà rilevare, scaricare
> e avviare le nuove revisioni, sempre dopo conferma dell'utente e verifica
> dell'integrità del file.

> **Nota Windows:** l'eseguibile non dispone di una firma digitale commerciale.
> Al primo avvio Microsoft Defender SmartScreen potrebbe mostrare un avviso.
> Verifica che il nome del file e l'hash SHA-256 coincidano con quelli pubblicati
> nella release, quindi scegli `Ulteriori informazioni` e `Esegui comunque`.

### 4. Avvia Star Citizen

La lingua viene configurata automaticamente. Se un aggiornamento del launcher
rimuove i file locali, basta riaprire l'installer: non installa mai alla cieca
su una build con stringhe inglesi diverse da quelle già revisionate.

## Se l'installer non trova il gioco

Seleziona la cartella `LIVE` che contiene `Data.p4k` e `Bin64`.

Esempio:

```text
D:\Robert Space Industries\StarCitizen\LIVE
```

Il percorso verificato viene salvato e riutilizzato. Per cambiarlo, riapri
l'installer e scegli l'opzione `4`.

## Ripristina i file precedenti

1. Chiudi Star Citizen e RSI Launcher.
2. Apri nuovamente l'installer.
3. Digita `2` e premi **Invio**.

L'installer chiede una seconda conferma e usa esclusivamente il backup attivo
registrato durante l'ultima installazione. I vecchi backup non vengono mai
applicati alla cieca. Se `user.cfg` è stato modificato dopo l'installazione, le
nuove impostazioni vengono conservate e sono rimosse soltanto le righe
linguistiche aggiunte dal progetto.

I backup si trovano in:

```text
Documenti\StarCitizenItalianTranslation\backups
```

## Perché questa traduzione è diversa

L'obiettivo non è sostituire parole inglesi una dopo l'altra, ma ricreare in
italiano tono, atmosfera e intenzione di ogni scena.

- **Revisione manuale stringa per stringa:** 89.437 stringhe traducibili
  approvate, senza traduzione automatica in massa.
- **Voci riconoscibili:** dialoghi riscritti nel registro del singolo NPC,
  preservando ironia, aggressività, formalità, gergo e ritmo della battuta.
- **Glossario vincolante:** 4.743 decisioni terminologiche per UI, volo,
  equipaggiamento, missioni, organizzazioni e lore.
- **Compatibilità con mappe e guide:** pianeti, città, avamposti, fazioni,
  modelli, pubblicazioni e nomi utili a orientarsi restano nella forma canonica.
- **Italiano naturale:** niente calchi meccanici; genere dinamico gestito con
  formulazioni credibili e senza grafie artificiali.
- **Controlli tecnici:** tag, variabili, maiuscole funzionali, ritorni a capo,
  codifica, apostrofi e virgolette sono verificati automaticamente.

Scelte come `Hangar`, `Multitool`, `Centro Cargo`, `Area di atterraggio` e
`Piattaforma di atterraggio` non sono casuali: sono registrate nel glossario e
applicate in modo coerente.

## Stato della 4.10-R1

- Copertura: **90.363 / 90.363 chiavi**.
- Stringhe traducibili approvate manualmente: **89.437**.
- Integrazioni manuali prive di sorgente inglese: **636**.
- Stringhe classificate come non traducibili: **114**.
- Stringhe intenzionalmente vuote: **176**.
- Build verificata: **4.10.191.2241**, branch `sc-alpha-4.10.0`, change
  **12519617**.
- Delta rispetto alla 4.9: **287 chiavi aggiunte, 45 rimosse, 156 modificate e
  89.920 invariate**.
- Tutte le **443 chiavi aggiunte o modificate** presenti nella 4.10 sono state
  revisionate.
- Chiavi mancanti, extra, duplicate o malformate: **0**.
- Caratteri corrotti o mojibake: **0**.
- Versione: **Traduzione italiana Star Citizen 4.10 — Revisione 1**.
- Novità dell'installer: aggiornamento automatico con download HTTPS dal
  repository ufficiale, controllo del nome, della dimensione e dell'impronta
  SHA-256 prima dell'avvio.
- Protezione delle maiuscole accentate applicata a **2.066 chiavi UI**; altre
  **79 chiavi condivise** restano sottoposte a controllo conservativo e **22
  valori** sono stati normalizzati.
- Ripristino dell'installer vincolato al backup attivo, con conferma esplicita e
  rifiuto automatico degli stati vecchi o non associati all'installazione.
- SHA-256 sorgente inglese: `7DF68893F0EC8564D9E123024CF06C6C731DD7ACC36B528C7CAA06104AD74E11`.
- SHA-256 payload: `96CAB8C9053F2B85D2D2AE2F7A8E231EEE8F993392CF680E36A70ED2C9DFCB08`.
- SHA-256 installer: `D53244B9284B372D89B361F538B987AD9C54BCAA65A629AC76AD013CD52DB4C5`.

La base inglese è stata estratta direttamente dalla LIVE installata e confrontata
byte per byte con quella usata per generare il payload pubblico. Dopo un
aggiornamento, l'installer ripete questo controllo sul computer dell'utente:
se l'hash inglese è identico prosegue, altrimenti si ferma.

## Cosa resta in inglese

Soltanto ciò che è utile o necessario mantenere:

- nomi propri, località e riferimenti per mappe e guide;
- nomi canonici di aziende, organizzazioni, modelli, livree ed edizioni;
- titoli ufficiali, pubblicazioni e slogan del lore;
- comandi digitabili, tasti, codice e parametri interpretati dal gioco.

Un termine inglese non protetto da una di queste ragioni è considerato un errore
e può essere segnalato.

## Sostieni il progetto

La traduzione è gratuita, non commerciale e senza paywall. Puoi sostenerla in
modo semplice:

- metti una **stella** al repository;
- condividi la release con la comunità italiana;
- segnala errori con uno screenshot e il punto esatto in cui compaiono;
- aiuta a verificare rapidamente la compatibilità dopo gli aggiornamenti LIVE.

## Segnala un problema

Apri una [Issue](https://github.com/Sici29/SC-Italian-Translation/issues) per
segnalare:

- una frase poco naturale o rimasta in inglese;
- un tono non adatto al personaggio;
- un errore di genere, concordanza o maiuscole;
- un testo tagliato nell'interfaccia;
- un problema con installazione, aggiornamento o ripristino.

Non pubblicare file originali del gioco, dati dell'account o informazioni
personali.

<details>
<summary><strong>Informazioni per traduttori e sviluppatori</strong></summary>

Il repository pubblico contiene:

- `translation/`: solo il payload italiano installabile;
- `glossary/`: dizionario editoriale vincolante;
- `docs/`: guida stilistica e criteri di localizzazione;
- `tools/`: sorgente dell'installer;
- `tools/vendor/`: componente StarBreaker usato per la sola verifica locale del
  `Data.p4k`, con avviso di licenza;
- `tests/`: test di installazione, ripristino e integrità.

Non contiene il `global.ini` inglese, traduzioni esterne di confronto, estrazioni
private o il master interno che incorpora il testo originale. Gli strumenti non
generano traduzioni: organizzano, installano e verificano materiale già
revisionato manualmente.

Per compilare l'EXE:

```powershell
python -m pip install -r requirements-build.txt
.\tools\build_installer.ps1
```

</details>

## Componente di verifica

L'installer incorpora
[StarBreaker 0.3.2](https://github.com/diogotr7/StarBreaker), distribuito con
licenza MIT, per estrarre esclusivamente il file inglese necessario al controllo
di compatibilità. L'operazione resta locale e il file temporaneo viene eliminato
automaticamente.

## Nota legale

Questa è una traduzione fan non ufficiale e non commerciale. Star Citizen,
Squadron 42 e tutti i marchi, personaggi, luoghi, veicoli e contenuti correlati
appartengono ai rispettivi titolari di Cloud Imperium. Il progetto non è
approvato, sponsorizzato o affiliato a Cloud Imperium Group.

Per utilizzarla è necessaria una copia legittima e installata di Star Citizen.
Sito ufficiale: [Roberts Space Industries](https://robertsspaceindustries.com/).
Consulta la [policy ufficiale su fan translation e localizzazione](https://support.robertsspaceindustries.com/hc/en-us/articles/360006895793-Star-Citizen-Fankit-and-Fandom-FAQ).
