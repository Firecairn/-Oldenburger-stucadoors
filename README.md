# Oldenburger Stucadoors

Website van Oldenburger Stucadoors: *strak in afwerking, sterk in detail.*

De site staat op Vercel en wordt bij elke wijziging in deze repository automatisch bijgewerkt.

## Gegevens invullen

Alle contactgegevens staan in één bestand: **`gegevens.js`**. Vul daar telefoonnummer, WhatsApp, e-mail, adres, KvK en reviews in. Wat is ingevuld verschijnt vanzelf op alle pagina's; wat leeg blijft wordt nergens getoond.

Het offerteformulier werkt zodra in `gegevens.js` een e-mailadres of een formulierdienst is ingevuld:

- met `formulier` (bijvoorbeeld een Formspree-adres) wordt de aanvraag direct verstuurd;
- met alleen `email` opent het e-mailprogramma van de bezoeker met de ingevulde aanvraag.

## Opbouw

| Onderdeel | Bestand |
|---|---|
| Pagina's | `index.html`, `diensten.html`, `werkwijze.html`, `projecten.html`, `over-frank.html`, `contact.html`, `privacy.html`, `404.html` |
| Opmaak | `assets/site.css` |
| Gedrag (menu, filter, vergroting, formulier) | `assets/site.js` |
| Foto's, video's, lettertypes | `assets/` |
| Teksten en paginaopbouw | `tools/build.py` |

De pagina's worden gemaakt door `python3 tools/build.py` (vereist Pillow). Pas teksten daar aan en draai het script opnieuw; wijzig de `.html`-bestanden niet met de hand, want die worden overschreven. Zet in `tools/build.py` bij `SITE_URL` het domein zodra dat bekend is: dan komen er ook een sitemap, `robots.txt` en deel-afbeelding voor sociale media bij.

Lettertypes: Cormorant Garamond en Inter (SIL Open Font License), lokaal meegeleverd.
