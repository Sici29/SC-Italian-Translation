# Traduzione italiana Star Citizen 4.10 — Revisione 3

Terza revisione della localizzazione italiana non ufficiale per Star Citizen
LIVE 4.10.2 (build `4.10.197.2878`, branch `sc-alpha-4.10.2`, change `12913470`, aggiornamento del 18 ottobre 2026).

## Novità della 4.10-R3

- **Copertura 100% manuale umana:** Tutte le 577 chiavi aggiunte o modificate dalla patch CIG sono state tradotte e revisionate professionalmente in 4 lotti dedicati.
- **Nuovi contenuti inclusi:**
  - Evento IASI (Intergalactic Aerospace Science Institute), missioni scientifiche, incarichi di rifornimento, ricompense e distintivi.
  - Nuove armi ed equipaggiamenti (fucile S71 Infrared, mitra P8-SC Echo, fucili a pompa R97 Runic e Ravager-212 Infrared, fucile di precisione Atzkav Starwalker, mitragliatrice leggera F55 Shadowflux, modulo Cambio-II Glacier SRT, raggio traente MaxLift-II Keelback).
  - Nuove armature e tute (serie Zeus Exploration Keelback/Echo/Glacier, completi Venture Starwalker/Infrared, elmo BUL-H4 Stronghold Nine Tails, corazze e zaini Morozov-SH-I / Morozov-CH Kalahari/Galvanic/Headstone, linea completa Monolith Heavy Armor Liquidator/Tsunami/Sandhawk/Serpentine/Runic/Blackheart/Shadowflux/Silver Strike/Oubliette).
  - Flight Blade Broad & Rabiee per Aurora Mk II, Mantis, Meteor, Zeus Mk II CL ed ES.
  - Nuovi veicoli RSI Skylark e rinnovata serie Constellation Mk5 (Andromeda, Aquila, Taurus) con relative livree e descrizioni.
  - Nuove ricette di fabbricazione Banu del Collezionista Wikelo e decorazioni per hangar.
- **Installer potenziato:**
  - **Confronto patch automatico:** rileva e riconosce nativamente `sc-alpha-4.10.2` (change `12913470`) mantenendo la retrocompatibilità con tutte le build del ciclo 4.10 (`12519617`, `12572603`, `12660092`).
  - **Fallback dinamico all'inglese (Zero blocchi):** se CIG rilascia una nuova build non ancora convalidata, l'installer estrae automaticamente il catalogo inglese dal `Data.p4k` locale e compone al volo un payload ibrido funzionante (testi noti in italiano, testi inediti in inglese) senza bloccare il giocatore.
  - **Rilevamento intelligente:** auto-rilevamento della cartella LIVE tramite registro Windows, percorsi standard o variabile d'ambiente.
  - **Preservazione differenziale:** conserva intatte le impostazioni video e comandi personalizzate in `user.cfg`.
  - **Backup & Ripristino atomico:** salvataggio automatico prima di qualsiasi modifica e ripristino sicuro vincolato allo stato attivo.
  - **Aggiornamento automatico integrato:** verifica della presenza di nuove release GitHub all'avvio con download sicuro HTTPS e controllo dell'impronta SHA-256 prima dell'esecuzione.

## Compatibilità verificata

- Ramo: `sc-alpha-4.10.2`
- Build verificata: `4.10.197.2878`, change `12913470`
- Build precedentemente verificate: `12519617`, `12572603`, `12660092`
- Chiavi inglesi: `90.946`
- Delta rispetto alla 4.10-R2: `521` aggiunte, `12` rimosse, `56` modificate e `90.369` invariate
- Chiavi aggiunte o modificate revisionate: `577 / 577` (100%)
- SHA-256 sorgente inglese:
  `80D0DF503C47CC0E31FE5F841880C03D0FC0A261912169E3482988412FF7E9B1`

## Integrità

- Righe italiane: `90.946`
- Traduzioni approvate manualmente: `90.020`
- Integrazioni manuali prive di sorgente inglese: `636`
- Stringhe non traducibili: `114`
- Stringhe intenzionalmente vuote: `176`
- Glossario vincolante: `4.743` voci
- Chiavi UI protette per le maiuscole accentate: `2.066`
- SHA-256 payload italiano:
  `525833E0DA46E7D279867F211C84CD74862D5C658547DDFFC1C268E6FFC62450`
- SHA-256 installer:
  `CB5DBF05B2D0A241824FDEAB43D805F279A82CF3A4A491FDBCC011903194F596`

## Installer unico

La release contiene un solo file:

```text
StarCitizen_Traduzione_Italiana_4.10_R3.exe
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
