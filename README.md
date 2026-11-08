# Oldenburger Stucadoors

Website van Oldenburger Stucadoors: *strak in afwerking, sterk in detail.*

Een statische website van zes pagina's, zonder build-stap:

| Pagina | Bestand |
|---|---|
| Home | `index.html` |
| Diensten | `diensten.html` |
| Werkwijze (laag voor laag) | `werkwijze.html` |
| Projecten (met filter) | `projecten.html` |
| Over Frank | `over-frank.html` |
| Contact | `contact.html` |

Foto's en video's staan in `assets/`.

## Online zetten met GitHub Pages

1. Ga in deze repository naar **Settings → Pages**.
2. Kies bij *Source* voor **Deploy from a branch**, branch `main`, map `/ (root)`.
3. Na een minuut staat de site op `https://<gebruikersnaam>.github.io/<repository>/`.

## Nog aan te vullen

Zoek in de HTML-bestanden op `[` om alle placeholders te vinden, zoals:

- telefoonnummer, e-mailadres en WhatsApp-nummer
- KvK-nummer, adres en privacyverklaring
- echte reviews van klanten
- tekst over Frank (ervaring, achtergrond)
- plaats en toelichting bij het gewelfproject

Het offerteformulier op `contact.html` verstuurt nog niets. Koppel het aan een formulierdienst (bijvoorbeeld Formspree of Netlify Forms) of aan een eigen offertesysteem.
