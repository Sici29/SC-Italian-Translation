# Traduzione italiana Star Citizen 4.9 — Revisione 4

Quarta revisione pubblica della localizzazione italiana non ufficiale per
Star Citizen.

## Novità della R4

La R4 raccoglie il grande ciclo di verifica visiva svolto direttamente in
gioco dopo la R3. Il payload differisce su 1.212 chiavi: 1.190 revisioni
editoriali e 22 normalizzazioni tecniche mirate.

- Testi compatti e pulsanti rivisti per evitare troncamenti, sovrapposizioni e
  ritorni a capo innaturali.
- Correzioni estese a creazione del personaggio, menu principale, impostazioni,
  inventario, Gestione flotta, mobiGlas, terminali, chioschi e Arena Commander.
- Terminologia resa più naturale e coerente, senza tradurre nomi propri,
  località o riferimenti utili per mappe e guide.
- Nomi canonici di navi, aziende, avamposti, città, pubblicazioni ed elementi di
  lore mantenuti nella forma originale.
- Revisione delle categorie degli incarichi e delle etichette operative.
- Uniformazione di `Online`, `Offline`, `Equipaggiamento`, `Multitool`,
  `Hangar`, `Centro Cargo`, `Area di atterraggio` e `Piattaforma di
  atterraggio`.

## Maiuscole accentate

Il client trasforma dinamicamente in maiuscolo alcune etichette senza
segnalarlo nel file di localizzazione. La R4 estende la protezione tecnica a
2.066 chiavi UI confermate.

- Inclusi suggerimenti comandi, frontend, creazione del personaggio, Arena
  Commander, mobiGlas, terminali medici e avvisi HUD.
- Riesaminate 79 chiavi condivise fra campi maiuscoli e normali.
- Nessun caso condiviso lasciato senza decisione.
- Nessuna forma residua confermata come `MODALITà`, `LOCALITà` o `QUANTITà`.
- Descrizioni e frasi normali non vengono modificate indiscriminatamente.

## Ripristino più sicuro

L'installer non cerca più semplicemente il backup più recente presente su
disco. Usa soltanto quello registrato come attivo per la cartella LIVE
selezionata.

- I backup vecchi non vengono applicati automaticamente.
- Stati riferiti a un'altra installazione o a una revisione incoerente vengono
  rifiutati.
- Dal menu è richiesta una conferma esplicita prima del ripristino.
- Le impostazioni aggiunte in seguito dall'utente continuano a essere
  preservate.

## Installer unico

La release contiene un solo file:

```text
StarCitizen_Traduzione_Italiana_4.9_R4.exe
```

L'installer rileva la cartella del gioco, verifica la sorgente inglese,
controlla il payload italiano, crea un backup, configura testo italiano e audio
inglese e verifica nuovamente l'installazione al termine.

## Compatibilità verificata

- Ramo di riferimento: `sc-alpha-4.9.0`
- Build verificata: `4.9.186.58667`, change `12248363`
- Chiavi inglesi: `90.121`
- Stringhe inglesi aggiunte, rimosse o modificate rispetto alla base
  revisionata: `0`
- SHA-256 sorgente inglese:
  `E5574DF1178A980C4B8CFA1FB812D813B527CBC65BC613631EB0ABBFECBDD1A5`
- SHA-256 payload italiano:
  `9C8FC68AF677D84FB490852D359BCBF417B39699E61F14EEAEB0699FFD7E5E68`
- SHA-256 installer:
  `509E7438435A482050E9D09CE8272014E8FA16F1507AED6AD84A0B506529E009`

## Installazione

1. Chiudi Star Citizen e RSI Launcher.
2. Scarica l'EXE della release.
3. Aprilo e premi Invio.
4. Avvia il gioco.

Non servono Python, programmi separati, archivi da estrarre o configurazioni
manuali.

L'eseguibile non dispone di una firma digitale commerciale. Se SmartScreen
mostra un avviso, confronta l'hash SHA-256 con quello pubblicato nella release
prima di scegliere `Ulteriori informazioni` e `Esegui comunque`.

## Componente incluso

Per leggere il `Data.p4k`, l'installer incorpora StarBreaker 0.3.2, progetto
indipendente distribuito con licenza MIT:
https://github.com/diogotr7/StarBreaker
