# Traduzione italiana Star Citizen 4.9 — Revisione 3

Terza revisione pubblica della localizzazione italiana non ufficiale per
Star Citizen.

## Novità della R3

La traduzione non cambia rispetto alla R2: il payload italiano resta completo,
revisionato e identico. Questa revisione rende invece l'installer più autonomo
e sicuro dopo gli aggiornamenti del gioco.

- Non blocca più automaticamente una build soltanto perché il numero di change
  è nuovo.
- Estrae esclusivamente il `global.ini` inglese dal `Data.p4k` installato.
- Confronta dimensione e SHA-256 con la sorgente usata per la traduzione.
- Se il contenuto è identico, considera compatibile anche una nuova build o una
  nuova versione del gioco.
- Se cambia anche una sola parte del file inglese, interrompe l'installazione e
  richiede una revisione aggiornata.
- Usa una nuova icona trasparente con badge della bandiera italiana più grande
  e leggibile.

Il controllo non carica file del gioco in rete: avviene interamente sul computer
dell'utente e il file temporaneo viene eliminato al termine.

## Installer unico

La release contiene un solo file:

```text
StarCitizen_Traduzione_Italiana_4.9_R3.exe
```

L'installer rileva la cartella del gioco, controlla la sorgente inglese, verifica
il payload italiano, crea un backup, configura testo italiano e audio inglese e
offre il ripristino.

## Compatibilità verificata

- Ramo di riferimento: `sc-alpha-4.9.0`
- Versione precedente: `4.9.186.42610`, change `12232306`
- Nuova versione verificata: `4.9.186.58667`, change `12248363`
- Stringhe inglesi aggiunte, rimosse o modificate: `0`
- Chiavi: `90.121`
- SHA-256 sorgente inglese:
  `E5574DF1178A980C4B8CFA1FB812D813B527CBC65BC613631EB0ABBFECBDD1A5`
- SHA-256 payload italiano:
  `6F482EE99E1692128EEC8F13CFD0F335237789D00E7D75C2147B9CBEC2D19B42`
- SHA-256 installer:
  `0EBEA17BAF25400B1715DE3F13ED54BC7533D0927A8C1BBB196173CE33B40390`

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
