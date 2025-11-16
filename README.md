
# J.A.R.V.I.S — A Personal Desktop Assistant

> **Note:** triggers are matched by substring checks in `execute_query(query)`. That means partial matches will fire (e.g. any query containing the word `search` will trigger "search"). Keep that in mind when adding new commands.

---
## How to download and install the agent

* Install the complete zip file

```
pip install -r requirements.txt
```

> _ To install PyAudio on windows head over to https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio and download the .whl for your machine and run the installation as shown below, then install the remaining dependencies from the requirements.txt file. You may remove pyAduio from the requirements file if it interrupts your installation (its there for unix users)
```bash
pip install PyAudio‑0.2.11‑cp<version>‑cp<version>m‑win_amd<architecture>.whl
```

### On Ubuntu based Linux distribution you need to install the following packages, so that the code works:

```
sudo apt-get update && sudo apt-get install espeak

```
This section lists all voice commands and what each command triggers in your `jarvis.py`. Use this as a quick reference for testing, extending, or documenting your JARVIS assistant.

## Boot / authentication

* **Optical Face Recognition (startup)**

  * **What triggers it:** The face-recognition block runs immediately when `jarvis.py` is launched (the bottom of the file).
  * **What it does:** Uses `cv2.face.LBPHFaceRecognizer` + Haar cascade to detect a face. If `accuracy < 100` it announces success (`"Optical Face Recognition Done. Welcome"`) and calls `wakeUpJARVIS()` to start the assistant. Otherwise it speaks `"Optical Face Recognition Failed"` and stops.
  * **Files used:** `trainer/trainer.yml`, `haarcascade_frontalface_default.xml` (in `./Face-Recognition/` in your repo).

---

## High-level assistant flow

* **wakeUpJARVIS()**

  * Starts the Jarvis class, calls `wishMe()` (greeting + weather), then continuously captures voice input with `takeCommand()` and forwards it to `execute_query(query)`.

* **Jarvis.wishMe()**

  * Greets based on the current hour (morning/afternoon/evening), calls `weather()`, then says a prompt: "I am JARVIS. Please tell me how can I help you SIR?"

---

## Main voice commands (execute_query)

**Note:** checks are substring-based and not mutually exclusive. Order matters. I list them in the same order they appear in your code.

1. **`wikipedia`**

   * **Trigger:** any query containing the word `wikipedia`.
   * **Action:** strips `wikipedia` from the query, calls `wikipedia.summary(query, sentences=2)`, prints and speaks the short summary.

2. **`youtube downloader`**

   * **Trigger:** contains `youtube downloader`.
   * **Action:** executes the script `youtube_downloader.py` (using `exec(open(...).read())`).

3. **`voice`**

   * **Trigger:** contains `voice` and optionally `female`.
   * **Action:** switches `pyttsx3` voice to `voices[1]` if `female` present; else `voices[0]`. Then speaks confirmation.
   * **Note:** later in file there's another `elif 'voice'` block — duplicate checks exist; the second one sets voices reversed (voices[0] vs voices[1]). This is a bug/duplication to fix.

4. **`jarvis are you there`**

   * **Trigger:** exact substring.
   * **Action:** speaks "Yes Sir, at your service".

5. **`jarvis who made you` / `who made you`**

   * **Trigger:** queries containing those phrases.
   * **Action:** speaks lines about the master/creator.

6. **`open youtube` / `open amazon` / `open google` / `open stackoverflow`**

   * **Trigger:** `open youtube` / `open amazon` / `open google` / `open stackoverflow`.
   * **Action:** opens the specified site in Chrome via the registered Chrome browser.

7. **`cpu`**

   * **Trigger:** contains `cpu` (note: appears twice in code).
   * **Action:** calls `cpu()` imported from `helpers` (presumably reads CPU usage info and speaks it).

8. **`joke`**

   * **Trigger:** contains `joke` (appears twice).
   * **Action:** calls `joke()` from `helpers` (speaks a joke).

9. **`screenshot`**

   * **Trigger:** contains `screenshot` (appears twice).
   * **Action:** calls `screenshot()` from `helpers()` and speaks `taking screenshot`.

10. **`play music`**

    * **Trigger:** contains `play music`.
    * **Action:** `os.startfile("D:\\RoiNa.mp3")` — plays a hardcoded MP3. Replace with a configurable path or folder scan.

11. **`search youtube`**

    * **Trigger:** contains `search youtube`.
    * **Action:** asks follow-up question and calls `youtube(takeCommand())` (function from `youtube` module) to search/play.

12. **`the time`**

    * **Trigger:** contains `the time`.
    * **Action:** speaks current time (HH:MM:SS format).

13. **`search` (general)**

    * **Trigger:** contains `search` (this is broad and will match many things).
    * **Action:** asks what to search for, captures voice, opens Google search results in Chrome, speaks a confirmation.
    * **IMPORTANT:** this will also match `search youtube` and other longer phrases unless order prevents it.

14. **`location`**

    * **Trigger:** contains `location`.
    * **Action:** asks for location, opens Google Maps URL for that place.

15. **`your master`**

    * **Trigger:** contains `your master`.
    * **Action:** speaks the master name. Contains an OS-check bug: the `if platform == "win32" or "darwin"` condition is always truthy because of how `or` is used — fix it.

16. **`your name`**

    * **Trigger:** contains `your name`.
    * **Action:** speaks "My name is JARVIS".

17. **`who made you`**

    * **Trigger:** contains `who made you`.
    * **Action:** speaks creation message (duplicate of earlier maker messages).

18. **`stands for`**

    * **Trigger:** contains `stands for`.
    * **Action:** explains J.A.R.V.I.S acronym.

19. **`open code`**

    * **Trigger:** contains `open code`.
    * **Action:** opens VS Code using a hardcoded path on Windows or runs `code .` on other OSes.

20. **`shutdown`**

    * **Trigger:** contains `shutdown`.
    * **Action:** calls OS shutdown commands (Windows: `shutdown /p /f`, others: `poweroff`). Dangerous — use with caution.

21. **`your friend`**

    * **Trigger:** contains `your friend`.
    * **Action:** speaks list of assistant "friends" (Google Assistant, Alexa, Siri).

22. **`github`**

    * **Trigger:** contains `github`.
    * **Action:** opens your GitHub profile in Chrome.

23. **`remember that`**

    * **Trigger:** contains `remember that`.
    * **Action:** asks follow-up, records spoken phrase to `data.txt` (overwrites file), and confirms.

24. **`do you remember anything`**

    * **Trigger:** contains that exact phrase.
    * **Action:** reads `data.txt` and speaks it.

25. **`sleep`**

    * **Trigger:** contains `sleep`.
    * **Action:** calls `sys.exit()` to terminate the program.

26. **`dictionary`**

    * **Trigger:** contains `dictionary`.
    * **Action:** asks what to look up and calls `translate(takeCommand())` (from `diction` module).

27. **`news`**

    * **Trigger:** contains `news`.
    * **Action:** calls `speak_news()` (speaks headlines) then asks if user wants full article and opens `getNewsUrl()` in browser if user says `yes`.

28. **`email to gaurav`**

    * **Trigger:** contains `email to gaurav`.
    * **Action:** asks what to say, then calls `self.sendEmail(to, content)` using a hardcoded `to` (placeholder 'email'). Wraps call in try/except and speaks success/failure.

---

## Helper functions / imported modules your commands rely on

* **helpers.py** — contains `takeCommand()`, `speak()`, `cpu()`, `joke()`, `screenshot()`, `weather()`, and other utilities. Many `execute_query()` cases call these. Make sure `helpers` is correct and robust (I previously provided a safer `weather()` replacement).

* **youtube (module)** — a helper that performs Youtube searches/plays using your custom `youtube()` function.

* **diction (module)** — `translate()` function that probably uses an API to look up words or translate language.

* **news (module)** — exposes `speak_news()` and `getNewsUrl()` used for news reading & opening full article.

* **OCR (module)** — `OCR()` imported but never used inside `execute_query()` — check if you want a command to trigger OCR.

---

## Problems & suggested fixes (actionable)

1. **Duplicate/overlapping `if` branches** — `voice`, `cpu`, `joke`, `screenshot` appear more than once. Consolidate to avoid unpredictable branching.
2. **Substring-based matching is brittle** — use tokenization or exact commands, or prefer `query.startswith()`/regex to reduce false positives.
3. **OS checks are incorrect** — conditions like `if platform == "win32" or "darwin"` always evaluate True. Use `if platform in ("win32","darwin")`.
4. **Hardcoded paths & values** — e.g. MP3 path, VS Code path, Chrome path, email credentials. Make these configurable through a `config.py` or environment variables.
5. **Email credentials are plaintext** — don't hardcode credentials in code. Use environment variables or a secure vault.
6. **Shutdown command is dangerous** — consider requiring a confirmation phrase before executing.
7. **Face recognition runs on import / at bottom of file** — better structure: separate face-authentication into a function and call it explicitly from a guarded `if __name__ == '__main__'` flow (you already do, but the bottom of the file runs a blocking while-loop before main app logic; consider refactoring to avoid duplicate logic).

---

## Quick mapping (compact)

```
"wikipedia"         -> wikipedia.summary(query)
"youtube downloader"-> runs youtube_downloader.py
"voice [female]"    -> switch TTS voice
"jarvis are you there" -> reply ready
"open youtube"      -> open youtube in chrome
"open amazon"       -> open amazon in chrome
"cpu"               -> cpu() helper
"joke"              -> joke() helper
"screenshot"        -> screenshot() helper
"open google"       -> open google
"open stackoverflow"-> open stackoverflow
"play music"        -> play hardcoded mp3
"search youtube"    -> youtube(takeCommand())
"the time"          -> speak time
"search"            -> open google search for provided phrase
"location"          -> open google maps for provided location
"your master"       -> speak master name (buggy OS logic)
"your name"         -> speak JARVIS
"who made you"      -> speak creator
"stands for"        -> speak acronym
"open code"         -> open VS Code
"shutdown"          -> system shutdown
"remember that"     -> write data.txt
"do you remember"   -> read data.txt
"sleep"             -> exit program
"dictionary"        -> translate(takeCommand())
"news"              -> speak_news() and optionally open getNewsUrl()
"email to gaurav"   -> sendEmail()
```

---
This project is open-source and available under the MIT License.

If you have any questions or suggestions, feel free to contact me.

Become Tony Stark with this! 
