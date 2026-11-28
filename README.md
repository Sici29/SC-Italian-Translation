# Star Citizen — Traduzione Italiana Non Ufficiale

Localizzazione italiana per **Star Citizen LIVE 4.10.3**, build **13220821**.

Include un installer Windows standalone in un unico file con backup automatico, ripristino e gestione intelligente degli aggiornamenti.

> [!NOTE]
> **Traduzione fan non ufficiale e non commerciale.** Il progetto non è approvato, sponsorizzato o affiliato a Cloud Imperium Games o Roberts Space Industries.

---

## 🚀 Guida Rapida all'Installazione

### 1. Scarica l'installer
Scarica l'eseguibile verificato più recente:  
👉 [**Download Diretto (GitHub Releases)**](https://github.com/Sici29/SC-Italian-Translation/releases/latest)

File: `StarCitizen_Traduzione_Italiana_4.10_R5.exe`

### 2. Chiudi gioco e launcher
Assicurati che **Star Citizen** e **RSI Launcher** siano completamente chiusi.

### 3. Avvia e installa
Fai doppio clic su `StarCitizen_Traduzione_Italiana_4.10_R5.exe` e premi **Invio**.

L'installer si occuperà di tutto:
- Rileva automaticamente la cartella `LIVE` del gioco;
- Crea un backup di sicurezza dei file originali;
- Installa il testo in italiano mantenendo l'audio originale in inglese;
- Preserva le tue impostazioni grafiche e comandi in `user.cfg`.

Avvia normalmente il gioco da **RSI Launcher**!

---

## ✨ Caratteristiche Principali

- **Catalogo completo:** 91.358 chiavi nella LIVE verificata, con dialoghi, missioni, interfaccia e descrizioni in italiano.
- **Glossario Vincolante:** Più di 4.700 voci codificate per garantire coerenza terminologica assoluta tra veicoli, armi, equipaggiamento e interfacce.
- **Nomi riconoscibili nelle guide:** Le denominazioni inglesi di stazioni, luoghi, modelli, livree, equipaggiamenti ed eventi facilitano la ricerca nelle mappe e nelle guide.
- **Verifica della build:** La R5 è verificata sulla LIVE 13220821. Per altre build l'installer confronta l'impronta del catalogo inglese. Se il catalogo differisce, il menu può proporre una modalità provvisoria con le chiavi note in italiano e quelle nuove in inglese.
- **Ripristino Sicuro (Rollback Atomico):** Puoi tornare alla lingua originale in qualsiasi momento tramite il menu dell'installer (opzione `2`), ripristinando fedelmente i file precedenti.
- **Aggiornamento Automatico Integrato:** All'avvio, l'installer verifica su GitHub se esiste una nuova revisione e può aggiornarsi in un clic con convalida SHA-256 integrata.

---

## ❓ Risoluzione Problemi e Domande Frequenti

<details>
<summary><strong>L'installer non trova automaticamente la cartella del gioco</strong></summary>

Se Star Citizen è installato su un'unità secondaria o un percorso personalizzato, scegli l'opzione `4` nel menu dell'installer oppure seleziona la cartella `LIVE` contenente `Data.p4k` e `Bin64`.

Percorso standard di riferimento:
```text
C:\Program Files\Roberts Space Industries\StarCitizen\LIVE
```
Il percorso verificato viene memorizzato per gli aggiornamenti futuri.
</details>

<details>
<summary><strong>Avviso di Microsoft Defender SmartScreen</strong></summary>

Essendo un software fan non commerciale distribuito gratuitamente, l'eseguibile non dispone di un certificato a pagamento.  
Se Windows visualizza l'avviso SmartScreen:
1. Clicca su **Ulteriori informazioni**;
2. Verifica che l'impronta SHA-256 corrisponda a quella pubblicata nella release;
3. Clicca su **Esegui comunque**.
</details>

<details>
<summary><strong>Come ripristinare i file di gioco originali</strong></summary>

1. Chiudi Star Citizen e RSI Launcher;
2. Riapri l'installer;
3. Digita `2` e premi **Invio**.  
L'installer rimuoverà la traduzione ripristinando il backup originale attivo. I tuoi parametri grafici e di sistema in `user.cfg` rimarranno intatti.
</details>

<details>
<summary><strong>Cosa rimane intenzionalmente in inglese?</strong></summary>

Per preservare l'immersione, la compatibilità con le guide online e il corretto funzionamento del motore di gioco:
- Nomi propri di corpi celesti, città, stazioni spaziali e cosmoporti (es. *August Dunlow Spaceport*, *Area18*, *Orison*);
- Nomi canonici di aziende, fazioni e organizzazioni (*Crusader Industries*, *Drake Interplanetary*, *Nine Tails*);
- Modelli di navi, livree ed edizioni (*Cutlass Black*, *Sabre Raven EX*);
- Comandi della console di gioco e comandi chat preceduti da barra (es. `/partyinvite`, `r_displayinfo`).
</details>

---

## 🔍 Dettagli Tecnici e Stato Release

<details>
<summary><strong>Stato e Impronte SHA-256 (Release 4.10-R5)</strong></summary>

- **Versione Client LIVE verificata:** `4.10.201.48085` (branch `sc-alpha-4.10.0`, change `13220821`)
- **Copertura del catalogo:** `91.358 / 91.358` chiavi
- **Delta dalla R4:** 989 voci aggiornate per ripristinare i nomi inglesi. La build LIVE è la stessa.
- **Stato editoriale:** 90.432 approvate, 636 integrazioni, 114 tecniche e 176 vuote
- **Verifiche e QA:** 7 suite di test di localizzazione + 15 controlli installer superati

| File | Dimensione | SHA-256 |
| :--- | :--- | :--- |
| **Sorgente LIVE inglese** | 10.700.162 B | `99113D762AAABEB1519458E6FDCA7B45610BCCE3C5E3ADFB795C79A96FCB7CEA` |
| **Payload italiano** | 11.423.953 B | `243E2AF83A3D473F1492703B22F62ECD6ECE5251C7BDE0D70AA39CECA0D2613A` |
| **Installer EXE (4.10-R5)** | 18.297.205 B | `51F77D5DED67E1EF36834DA3ECA21B65F8CE144B3431C49514BE11273014A7D3` |

</details>

<details>
<summary><strong>Informazioni per Traduttori e Sviluppatori</strong></summary>

La struttura pubblica del repository comprende:
- `translation/`: payload italiano installabile e configurazione `user.cfg`;
- `glossary/`: database terminologico vincolante (`glossario.csv`);
- `docs/`: linee guida editoriali e convenzioni stilistiche;
- `tools/`: codice sorgente Python dell'installer e modulo [StarBreaker 0.3.2](https://github.com/diogotr7/StarBreaker) (licenza MIT);
- `tests/`: test automatici di installazione, regressione e integrità.

Per compilare autonomamente l'eseguibile:
```powershell
python -m pip install -r requirements-build.txt
.\tools\build_installer.ps1
```
</details>

---

## 🤝 Contribuire e Segnalare Errori

Hai notato un refuso, una frase poco naturale o un testo fuori posto?
- Apri una [**Issue su GitHub**](https://github.com/Sici29/SC-Italian-Translation/issues) includendo uno screenshot e il luogo in cui compare il testo.
- Consulta [CONTRIBUTING.md](CONTRIBUTING.md) per i criteri di segnalazione.
- Metti una **stella ⭐ al repository** per supportare il progetto e condividerlo con la community italiana!

---

## ⚖️ Note Legali

Questo è un progetto fan non ufficiale, gratuito e non commerciale.  
Star Citizen, Squadron 42 e tutti i relativi loghi, marchi, personaggi, navi e contenuti appartengono a Cloud Imperium Games e Roberts Space Industries.  
Per l'utilizzo è richiesta una copia legittima di Star Citizen. Visita il sito ufficiale: [robertsspaceindustries.com](https://robertsspaceindustries.com/).
