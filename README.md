# Star Citizen — Traduzione Italiana Non Ufficiale

Localizzazione italiana completa, curata e professionale per **Star Citizen LIVE 4.10**.  
Include un installer Windows standalone in un unico file con backup automatico, ripristino e gestione intelligente degli aggiornamenti.

> [!NOTE]
> **Traduzione fan non ufficiale e non commerciale.** Il progetto non è approvato, sponsorizzato o affiliato a Cloud Imperium Games o Roberts Space Industries.

---

## 🚀 Guida Rapida all'Installazione

### 1. Scarica l'installer
Scarica l'eseguibile verificato più recente:  
👉 [**Download Diretto (GitHub Releases)**](https://github.com/Sici29/SC-Italian-Translation/releases/latest)

File: `StarCitizen_Traduzione_Italiana_4.10_R2.exe`

### 2. Chiudi gioco e launcher
Assicurati che **Star Citizen** e **RSI Launcher** siano completamente chiusi.

### 3. Avvia e installa
Fai doppio clic su `StarCitizen_Traduzione_Italiana_4.10_R2.exe` e premi **Invio**.  
L'installer si occuperà di tutto:
- Rileva automaticamente la cartella `LIVE` del gioco;
- Crea un backup di sicurezza dei file originali;
- Installa il testo in italiano mantenendo l'audio originale in inglese;
- Preserva le tue impostazioni grafiche e comandi in `user.cfg`.

Avvia normalmente il gioco da **RSI Launcher**!

---

## ✨ Caratteristiche Principali

- **Traduzione 100% Umana e Professionale:** Oltre 90.400 stringhe revisionate manualmente senza traduzioni automatiche approssimative, con adattamento naturale di dialoghi, missioni e lore.
- **Glossario Vincolante:** Più di 4.700 voci codificate per garantire coerenza terminologica assoluta tra veicoli, armi, equipaggiamento e interfacce.
- **Compatibilità Totale con Guide e Mappe:** Nomi propri di sistemi, pianeti, stazioni, modelli di navi e comandi rimangono conformi agli standard della community internazionale per non disorientare i piloti.
- **Zero Blocchi (Fallback Dinamico):** Se CIG pubblica una nuova micro-patch non ancora verificata, l'installer genera al volo un catalogo ibrido funzionante (testi noti in italiano, testi nuovi provvisoriamente in inglese), garantendo che il gioco parta sempre senza crash o blocchi.
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
<summary><strong>Stato e Impronte SHA-256 (Release 4.10-R2)</strong></summary>

- **Versione Client LIVE supportata:** `4.10.193.11644` (branch `sc-alpha-4.10.0`, change `12660092`)
- **Copertura traduzione:** `90.437 / 90.437` stringhe (**100,00% manuale**)
- **Chiavi approvate:** 89.511 manuali | 636 integrazioni | 114 non traducibili | 176 vuote
- **Verifiche e QA:** 7 suite di test di localizzazione + 15 controlli installer superati

| File | Dimensione | SHA-256 |
| :--- | :--- | :--- |
| **Sorgente LIVE inglese** | 10.491.521 B | `037071E9FC8F402FEE87E76B5CA175F4AE7BEF5CF443A3A89727DB9B139AE2F3` |
| **Payload italiano** | 11.201.218 B | `CE0FBEA65B404B7E17293E76F1F1DD28344753239EAA7FDA37B9E2A1F58B492F` |
| **Installer EXE (4.10-R2)** | 17.229.751 B | `282F1ADA8BE89631C81018C5C155F8CADF4406308F6CFB3D3840C6E9EA30B521` |

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
