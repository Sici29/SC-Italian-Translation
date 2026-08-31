# Registro delle versioni

## 4.10 — Revisione 1

- Aggiornata la localizzazione alla LIVE `4.10`, build `4.10.191.2241`, branch
  `sc-alpha-4.10.0`, change `12519617`, tramite estrazione diretta del
  `global.ini` inglese dal `Data.p4k`.
- Portata la copertura a **90.363 chiavi**: 89.437 approvate manualmente, 636
  integrazioni manuali prive di sorgente inglese, 114 non traducibili e 176
  intenzionalmente vuote.
- Rispetto alla 4.9: **287 chiavi aggiunte, 45 rimosse, 156 modificate e 89.920
  invariate**. Tutte le **443 chiavi aggiunte o modificate** sono state
  revisionate.
- Consolidato il glossario vincolante a **4.743 voci**.
- Confermate **2.066 chiavi UI protette**, riesaminate 79 chiavi condivise e
  normalizzati 22 valori con maiuscole accentate.
- Aggiunto il controllo automatico delle nuove release GitHub all'avvio
  dell'installer, con conferma dell'utente, download HTTPS e verifica di nome,
  dimensione e impronta SHA-256 prima dell'avvio.
- I file già scaricati vengono riutilizzati solo se superano nuovamente tutti i
  controlli; download incompleti o alterati vengono rifiutati.
- Il passaggio dalla R4 alla 4.10-R1 richiede un ultimo download manuale;
  l'aggiornamento integrato sarà disponibile dalla 4.10-R1 in avanti.
- SHA-256 sorgente inglese:
  `7DF68893F0EC8564D9E123024CF06C6C731DD7ACC36B528C7CAA06104AD74E11`.
- SHA-256 payload italiano:
  `96CAB8C9053F2B85D2D2AE2F7A8E231EEE8F993392CF680E36A70ED2C9DFCB08`.

## 4.9 — Revisione 4

- Aggiornate 1.212 chiavi del payload rispetto alla R3: 1.190 revisioni
  editoriali e 22 normalizzazioni tecniche confermate visivamente in gioco.
- Rifiniti naturalezza e lessico di testi non dialogici, descrizioni tecniche,
  contratti, equipaggiamento, terminali e interfacce.
- Corretti testi tagliati o sovrapposti in menu, inventario, Gestione flotta,
  mobiGlas, chioschi, Arena Commander e creazione del personaggio.
- Uniformate le scelte `Online`, `Offline`, `Equipaggiamento`, `Multitool`,
  `Hangar`, `Centro Cargo`, `Area di atterraggio` e `Piattaforma di
  atterraggio`.
- Estesa la protezione delle maiuscole accentate a 2.066 chiavi UI, comprese le
  famiglie dinamiche dei suggerimenti comandi, del frontend e dei terminali
  medici.
- Reso sicuro il ripristino: l'installer utilizza soltanto il backup attivo,
  rifiuta stati vecchi o appartenenti a un'altra installazione e richiede una
  conferma esplicita.
- Confermata la compatibilità con la build `4.9.186.58667`, change `12248363`,
  mediante estrazione diretta della sorgente inglese dal `Data.p4k`.

## 4.9 — Revisione 3

- Reso l'installer compatibile con gli aggiornamenti che non modificano la
  localizzazione inglese, senza dipendere dal solo numero di build.
- Aggiunta la verifica SHA-256 del `global.ini` inglese estratto direttamente
  dal `Data.p4k`: contenuto identico significa compatibilità; contenuto diverso
  blocca l'installazione.
- Verificata la nuova build `4.9.186.58667`, change `12248363`, senza variazioni
  rispetto alle 90.121 stringhe della R2.
- Aggiunta un'icona dedicata basata sul simbolo del gioco, con sfondo
  trasparente e badge italiano maggiorato sul modello dell'installer ANIIMO.
- Incorporato StarBreaker 0.3.2, distribuito con licenza MIT, esclusivamente per
  il controllo locale del file inglese.
- Il testo italiano e il relativo hash restano invariati rispetto alla R2.

## 4.9 — Revisione 2

- Aggiornate 546 stringhe rispetto alla R1; 280 appartengono all'audit UI finale.
- Rifinita la creazione del personaggio e corretti i testi del menu principale e delle impostazioni.
- Eliminati troncamenti e sovrapposizioni in inventario, Gestione flotta e mobiGlas.
- Compattate 27 statistiche dei tooltip e 21 categorie tecniche dell'inventario.
- Normalizzate 187 etichette dei comandi con maiuscole accentate corrette.
- Corretto `Cooldown Timer` in `Tempo di attesa` e `Cooler` in `Refrigeratore`.
- Portato il glossario vincolante a 4.733 voci.

## 4.9 — Revisione 1

- Completata la localizzazione manuale della LIVE 4.9.
- Revisionate integralmente 89.193 stringhe traducibili.
- Consolidato il glossario a 4.690 voci.
- Validato il payload sulla change 12232306 estratta dal gioco installato.
- Aggiunto installer Windows in un unico EXE con backup e ripristino.
- Aggiunti test per integrità, compatibilità, configurazione e conservazione
  delle modifiche successive dell'utente.
