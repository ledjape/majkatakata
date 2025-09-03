# majkatakata.com

Live site: https://majkatakata.com

A minimal one-page site built for speed and easy growth.

## Tech
- **Hosting**: GitHub Pages
- **CSS**: Pico.css (CDN)
- **Sections**: Hero, About, Instagram embeds, Subscribe, Contact

## Update content
- **Instagram**: Edit `index.html` and replace the three `https://www.instagram.com/p/POST_ID_*` links with real public post URLs. Keep the Instagram embed script at the bottom.
- **Subscribe**: Swap the Buttondown form `YOUR_LIST_ID` with your provider (Mailchimp/Beehiiv/Buttondown/Brevo).
- **Contact**: Replace the Formspree `YOUR_FORM_ID` or use a `mailto:` link.

## Deploy
Push to `main`; GitHub Pages auto-deploys.  
Custom domain managed via Route 53:
- A @ → 185.199.108.153 / .109.153 / .110.153 / .111.153
- CNAME www → ledjape.github.io.

## Next
- Add favicon (`/favicon.ico` or SVG).
- Add Open Graph meta tags for rich shares.
- (Optional) Analytics (Plausible/GA4).

