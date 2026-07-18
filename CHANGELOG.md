# Registro delle versioni

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
