# Utilizare în ChatGPT Cloud Projects

1. Creează sau deschide un Project în ChatGPT.
2. Copiază conținutul PROJECT_INSTRUCTIONS.md în instrucțiunile proiectului. Simpla încărcare a acestui fișier nu configurează instrucțiunile.
3. Adaugă COMMANDS.md în Sources/fișierele proiectului.
4. Deschide un chat nou în proiect și încearcă `/IG-REEL Scrie un Reel de 30 de secunde despre feedback, fără experiențe personale inventate.`.
5. Cere un rezultat cu date reale. Dacă biblioteca nu poate fi recuperată, atașează direct secțiunea necesară.

Poți folosi și un chat obișnuit: lipește instrucțiunile și atașează biblioteca pentru conversația respectivă. Pachetul nu instalează un plugin, nu înregistrează slash commands și nu modifică personalizarea globală. Nu rula instalatorul Python pentru adaptarea cloud. Capabilitățile contului și politicile workspace-ului determină accesul la web, analiză și crearea fișierelor. Workflow-urile nu oferă instrumente ori permisiuni noi.

Nu sunt incluse corpus personal sau credențiale. Păstrează și reconciliază instrucțiunile relevante deja existente ale proiectului. Alege o singură ediție lingvistică pentru același proiect.

Bază oficială de configurare, verificată la 2026-11-02: [ChatGPT Projects](https://learn.chatgpt.com/docs/projects). Instrucțiunile proiectului configurează comportamentul; biblioteca încărcată oferă workflow-urile. Adaptarea a fost instalată și testată într-un Project ChatGPT real la 2 noiembrie 2026. Accesul la bibliotecă și scenariile reprezentative au fost verificate în cont. Testele automate ale pachetului nu demonstrează calitatea generală a raționamentului sau funcționarea fiecărui workflow.

## Resurse și helper-e

Încarcă și REFERENCE.md (formule, rubrică, lexicon), plus helpers.zip dacă dorești rulări reale în instrumentul de analiză/execuție Python disponibil în sesiune. Nu este arhiva întregului repository. helpers.zip conține doar helper-ele Python, JSON-urile necesare și licențele, în structura lor originală. Exemple după extragere:

```text
python skills/ig-reel/hookscore.py --hook "Nu mai aștepta promovarea ca să fii lider." --json
python skills/ig-reel/beats.py script.txt --target 30 --wpm 165 --json
python skills/ig-caption/caption.py caption.txt --json
python skills/ig-audit/audit.py posts.csv --json
```

Execuția depinde de instrumentele sesiunii; nu afirma că un helper a rulat doar pentru că arhiva a fost încărcată. Dacă execuția sau extragerea arhivei nu sunt disponibile, folosește biblioteca și REFERENCE.md pentru o evaluare calitativă. Metricile Instagram necesită surse reale; lipsa accesului rămâne lipsă de dovezi. Voice template opțional: folosește informațiile cunoscute ori un profil provizoriu explicit. Caruselele și videoclipurile necesită un instrument real de randare pentru exporturi finale.

## Test live — 2 noiembrie 2026

COMMANDS și REFERENCE au fost accesate; cele 26 de formule și rubrica de 100 de puncte au fost confirmate. helpers.zip a fost extras în sesiune și hookscore.py/beats.py au rulat efectiv în Python 3.13.5. Pentru inputurile de test, scorul 44,4 și durata estimată 6,55 secunde au coincis cu rularea locală. Metricile lipsă au rămas N/A. Au fost testate scenarii reprezentative; nu toate cele 13 comenzi, randarea sau publicarea. Fișierele extrase nu au persistență garantată între sesiuni.
