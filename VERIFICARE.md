# Verificare — 1 noiembrie 2026

- 13/13 skill-uri acceptate de validatorul oficial `quick_validate.py`.
- Metadatele UI, invocarea `$ig-*`, referințele comune și licențele au fost verificate pentru fiecare skill.
- Sintaxa Python și toate fișierele JSON sunt valide.
- Cele 26 de ID-uri originale au fost păstrate. Rubrica de profil are 12 criterii și ponderi cu total 100.
- 28/28 teste automate trecute: 24 pentru scripturi și 4 pentru instalator.
- Scripturile au fost executate și dintr-un director de lucru diferit de cel al skill-ului.
- Testele acoperă diacritice, cuvinte cu cratimă, vocabular românesc, CTA-uri RO/EN, preview configurabil, păstrarea URL-urilor și emoji-urilor compuse, raportarea textelor prea scurte, mediane absente/zero, vizualizări zero, proveniența surselor, indicatori lipsă, separarea shares/sends și cohorte cont+format.
- Instalatorul a fost verificat pentru preflight fără scriere, instalare repetabilă, refuzul conflictelor fără modificări parțiale și refuzul surselor modificate.

## Limite

Verificarea validează structura și comportamentul local al instrumentelor. Nu demonstrează predicția viralității sau calibrarea scorurilor pentru română. Nu a fost accesat ori modificat un cont Instagram. Nu s-au creat sau publicat postări în timpul instalării. Nu s-a verificat activarea skill-urilor într-un mesaj viitor sau autocomplete pentru aliasurile slash; invocarea nativă documentată este `$ig-*`.

Pentru carusele și materiale video, workflow-urile descriu producția și verificarea fișierelor cu instrumentele disponibile în sesiunea de utilizare; această adaptare nu include un nou renderer video și nu conectează servicii externe.

Comandă de retestare:

```bash
python3 -B -m unittest discover -s tests -v
```
