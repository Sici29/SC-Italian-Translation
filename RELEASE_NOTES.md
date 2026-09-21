# Traduzione italiana Star Citizen 4.10 — Revisione 2

Seconda revisione della localizzazione italiana non ufficiale per Star Citizen
LIVE 4.10 (build `4.10.193.11644`, change `12660092`, aggiornamento del 17 settembre 2026).

## Novità della 4.10-R2

- **Copertura 100% manuale umana:** Tutte le 87 chiavi aggiunte o modificate dalla patch CIG sono state tradotte e revisionate professionalmente.
- **Nuovi contenuti inclusi:**
  - Distintivi e titoli evento *Orison Relief* (Tier 1-6).
  - Schede informative e parametri comparativi dei processi di raffinazione (resa, tempo, costo).
  - Nuovi veicoli, armature e armi (*Sabre Raven EX*, *ATLS IKTI Akuma*, livree esclusive).
  - Testi aggiornati per missioni di costruzione e ascensori di Orison.
- **Installer potenziato:**
  - **Confronto patch automatico:** rileva e confronta la build installata con quelle convalidate.
  - **Fallback dinamico all'inglese (Zero blocchi):** se CIG rilascia una nuova build non ancora convalidata, l'installer estrae automaticamente il catalogo inglese dal `Data.p4k` locale e compone al volo un payload ibrido funzionante (testi noti in italiano, testi inediti in inglese) senza bloccare il giocatore.
  - **Rilevamento intelligente:** auto-rilevamento della cartella LIVE tramite registro Windows, percorsi standard o variabile d'ambiente.
  - **Preservazione differenziale:** conserva intatte le impostazioni video e comandi personalizzate in `user.cfg`.
  - **Backup & Ripristino atomico:** salvataggio automatico prima di qualsiasi modifica e ripristino sicuro vincolato allo stato attivo.
  - **Aggiornamento automatico integrato:** verifica della presenza di nuove release GitHub all'avvio con download sicuro HTTPS e controllo dell'impronta SHA-256 prima dell'esecuzione.

## Compatibilità verificata

- Ramo: `sc-alpha-4.10.0`
- Build verificata: `4.10.193.11644`, change `12660092`
- Build precedentemente verificate: `12519617`, `12572603`
- Chiavi inglesi: `90.437`
- Delta rispetto alla 4.10-R1: `83` aggiunte, `9` rimosse, `4` modificate e `90.350` invariate
- Chiavi aggiunte o modificate revisionate: `87 / 87` (100%)
- SHA-256 sorgente inglese:
  `037071E9FC8F402FEE87E76B5CA175F4AE7BEF5CF443A3A89727DB9B139AE2F3`

## Integrità

- Righe italiane: `90.437`
- Traduzioni approvate manualmente: `89.511`
- Integrazioni manuali prive di sorgente inglese: `636`
- Stringhe non traducibili: `114`
- Stringhe intenzionalmente vuote: `176`
- Glossario vincolante: `4.743` voci
- Chiavi UI protette per le maiuscole accentate: `2.066`
- SHA-256 payload italiano:
  `CE0FBEA65B404B7E17293E76F1F1DD28344753239EAA7FDA37B9E2A1F58B492F`
- SHA-256 installer:
  `282F1ADA8BE89631C81018C5C155F8CADF4406308F6CFB3D3840C6E9EA30B521`

## Installer unico

La release contiene un solo file:

```text
StarCitizen_Traduzione_Italiana_4.10_R2.exe
```

## Installazione

1. Chiudi Star Citizen e RSI Launcher.
2. Scarica l'EXE della release (oppure avvia la versione precedente che lo aggiornerà automaticamente).
3. Aprilo e premi Invio.
4. Avvia il gioco.

L'eseguibile non dispone di una firma digitale commerciale. Se SmartScreen mostra un avviso, confronta l'hash SHA-256 con quello pubblicato nella release prima di scegliere `Ulteriori informazioni` e `Esegui comunque`.

## Componente incluso

Per leggere il `Data.p4k`, l'installer incorpora StarBreaker 0.3.2, progetto indipendente distribuito con licenza MIT:
https://github.com/diogotr7/StarBreaker

## Nota legale

Questa è una traduzione fan non ufficiale, gratuita e non commerciale. Il progetto non è approvato, sponsorizzato o affiliato a Cloud Imperium Games o Roberts Space Industries. Per utilizzarla è necessaria una copia legittima e installata di Star Citizen.
