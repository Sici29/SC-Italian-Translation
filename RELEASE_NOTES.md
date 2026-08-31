# Traduzione italiana Star Citizen 4.10 — Revisione 1

Prima revisione della localizzazione italiana non ufficiale per Star Citizen
LIVE 4.10.

## Novità della 4.10-R1

La 4.10-R1 aggiorna integralmente la base della traduzione alla nuova LIVE e
introduce l'aggiornamento automatico e verificato dell'installer.

- Controllo delle nuove revisioni GitHub eseguito automaticamente all'avvio.
- Download diretto del nuovo EXE, senza aprire il browser.
- Conferma esplicita dell'utente prima del download e dell'avvio.
- Selezione vincolata all'unico installer Windows della release stabile.
- Verifica di provenienza HTTPS, dimensione dichiarata e impronta SHA-256
  pubblicata da GitHub.
- Blocco e cancellazione dei download incompleti o alterati.
- Riutilizzo di un file già scaricato solo dopo una nuova verifica completa.

La R4 non contiene questa funzione: il passaggio alla 4.10-R1 richiede quindi
un ultimo download manuale. Dalla 4.10-R1 in avanti le revisioni successive
potranno essere rilevate, scaricate e avviate direttamente dall'installer,
sempre dopo conferma dell'utente.

## Compatibilità verificata

- Ramo: `sc-alpha-4.10.0`
- Build verificata: `4.10.191.2241`, change `12519617`
- Chiavi inglesi: `90.363`
- Delta rispetto alla 4.9: `287` aggiunte, `45` rimosse, `156` modificate e
  `89.920` invariate
- Chiavi aggiunte o modificate revisionate: `443 / 443`
- SHA-256 sorgente inglese:
  `7DF68893F0EC8564D9E123024CF06C6C731DD7ACC36B528C7CAA06104AD74E11`

Il `global.ini` inglese è stato estratto direttamente dalla LIVE installata. Le
chiavi nuove e modificate sono state revisionate prima della generazione del
payload; le `89.920` chiavi invariate conservano il lavoro già approvato.

## Integrità

- Righe italiane: `90.363`
- Traduzioni approvate manualmente: `89.437`
- Integrazioni manuali prive di sorgente inglese: `636`
- Stringhe non traducibili: `114`
- Stringhe intenzionalmente vuote: `176`
- Glossario vincolante: `4.743` voci
- Chiavi UI protette per le maiuscole accentate: `2.066`
- Chiavi condivise sottoposte a controllo conservativo: `79`
- Valori con accenti normalizzati: `22`
- SHA-256 payload italiano:
  `96CAB8C9053F2B85D2D2AE2F7A8E231EEE8F993392CF680E36A70ED2C9DFCB08`
- SHA-256 installer:
  `D53244B9284B372D89B361F538B987AD9C54BCAA65A629AC76AD013CD52DB4C5`

## Installer unico

La release contiene un solo file:

```text
StarCitizen_Traduzione_Italiana_4.10_R1.exe
```

L'installer rileva la cartella del gioco, controlla la compatibilità della
build, verifica il payload, crea un backup, configura testo italiano e audio
inglese e verifica nuovamente l'installazione al termine.

## Installazione

1. Chiudi Star Citizen e RSI Launcher.
2. Scarica l'EXE della release.
3. Aprilo e premi Invio.
4. Avvia il gioco.

L'eseguibile non dispone di una firma digitale commerciale. Se SmartScreen
mostra un avviso, confronta l'hash SHA-256 con quello pubblicato nella release
prima di scegliere `Ulteriori informazioni` e `Esegui comunque`.

## Componente incluso

Per leggere il `Data.p4k`, l'installer incorpora StarBreaker 0.3.2, progetto
indipendente distribuito con licenza MIT:
https://github.com/diogotr7/StarBreaker

## Nota legale

Questa è una traduzione fan non ufficiale, gratuita e non commerciale. Il
progetto non è approvato, sponsorizzato o affiliato a Cloud Imperium Games o
Roberts Space Industries. Per utilizzarla è necessaria una copia legittima e
installata di Star Citizen.
