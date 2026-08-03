# Ogden Decks DNS Cutover Procedure

## Approved staging release

- Cloudflare Pages project: `ogden-decks-preview`
- Branch: `ogden-decks-staging`
- Root directory: `ogden-decks-preview`
- Approved commit: `93bbbd611d09e4b3966617cde7fe10223273d7f9`
- Approved deployment: `498b7400-af39-46a6-874e-35235a9f0c9f`
- Preview: `https://498b7400.ogden-decks-preview.pages.dev`
- Final sitemap: `https://www.ogdendecks.com/sitemap.xml`

## Known deferred item

The public contact-form submission workflow is intentionally deferred. Phone, email and estimate information remain available. Employee Jotforms are preserved and noindexed.

## Before changing DNS

1. Export or screenshot all current DNS records for `ogdendecks.com`.
2. Keep the existing hosting account active as a rollback source.
3. Confirm access to the Cloudflare zone for `ogdendecks.com` with permission to read and edit DNS records and attach Pages custom domains.
4. Do not alter email-related MX, TXT, SPF, DKIM or DMARC records.
5. Confirm the approved deployment above is still the current successful production deployment for the Pages project.

## Cutover sequence

1. In Cloudflare Pages, add `ogdendecks.com` as a custom domain for `ogden-decks-preview`.
2. Add `www.ogdendecks.com` as a custom domain for the same project.
3. Allow Cloudflare to create or update only the web-host records required for the apex and `www` hostnames.
4. Keep all mail and unrelated verification records unchanged.
5. Wait for both custom domains to show active and for SSL certificates to be issued.
6. Set one preferred hostname and use a single 301 redirect from the alternate hostname. Recommended: `www.ogdendecks.com` as canonical because all page canonicals and the sitemap use `www`.
7. Confirm SSL mode is Full (strict) where compatible and Always Use HTTPS is enabled.

## Immediate production validation

Test all of the following on the real domain:

- `/`
- `/services-we-offer.html`
- `/deck-building.html`
- `/deck-repair-services.html`
- `/trex.html`
- `/pergola-installation.html`
- `/ogden-decks-railing-options.html`
- `/deck-project-gallery.html`
- `/contact-us.html`
- `/blog`
- `/sitemap.xml`
- `/robots.txt`
- `/leave-request.html`
- A legacy redirect such as `/deck-builder-layton-ut.html`
- An archive redirect such as `/blog/archives/05-2023`
- A nonexistent URL to confirm the custom noindex 404 page
- Several `/uploads/...` image URLs to confirm local fallback delivery

Confirm:

- HTTPS loads without certificate warnings.
- Apex and `www` use one-hop redirects only.
- Core pages return 200.
- Legacy URLs redirect to the intended destination.
- Employee Jotforms load and remain noindexed.
- The sitemap contains 366 unique production URLs.
- Robots references only `https://www.ogdendecks.com/sitemap.xml`.

## Search and analytics follow-up

1. Submit the final sitemap in Google Search Console.
2. Inspect the homepage, services, blog and key city pages in Search Console.
3. Confirm Google Analytics, Google Ads and call tracking separately if they are required. Cloudflare Web Analytics is not currently configured on the Pages project.
4. Monitor 404s, redirects, traffic and leads daily during the first week.

## Rollback

If the production site has a critical issue:

1. Restore the previous apex and `www` DNS records from the saved DNS backup.
2. Keep the Cloudflare Pages project and custom domains intact for troubleshooting unless they cause the issue.
3. Purge Cloudflare cache after restoring records if stale content persists.
4. Verify the old host loads over HTTPS before declaring rollback complete.

Do not cancel or delete the previous hosting account until the Cloudflare site has been stable and verified in production.
