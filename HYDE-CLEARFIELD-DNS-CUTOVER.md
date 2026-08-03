# Hyde Beauty & Wellness Clearfield — DNS Cutover Plan

## Approved staging release

- Cloudflare Pages project: `hyde-clearfield-preview`
- Branch: `hyde-clearfield-staging`
- Latest gated commit at preparation: `d6981abc2af876d1434eb51a4668caa82a9815e7`
- Quality gate: 71 HTML documents, 70 sitemap URLs, 348 redirect rules, zero redirect chains
- Live DNS must not be changed until the Cloudflare zone becomes Active.

## Current DNS state

Cloudflare zone ID: `3717d412a3903753626fad5c05d260c2`

The zone is currently **pending** because the registrar still delegates to Namecheap:

- Current observed nameservers: `dns1.registrar-servers.com`, `dns2.registrar-servers.com`
- Cloudflare-assigned nameservers: `gordon.ns.cloudflare.com`, `isla.ns.cloudflare.com`

Current web records:

- Apex A: `hydemedspaclearfield.com` → `199.34.228.77`
- WWW A: `www.hydemedspaclearfield.com` → `199.34.228.77`

These point to the existing Weebly site and must remain until the Pages custom domains are ready.

## Records that must be preserved

### Email forwarding MX records

- `eforward1.registrar-servers.com`
- `eforward2.registrar-servers.com`
- `eforward3.registrar-servers.com`
- `eforward4.registrar-servers.com`
- `eforward5.registrar-servers.com`

### TXT records

- Google Search Console verification: `google-site-verification=8DjC25__6OnqDpg-FlgD5abWFOYI-oR3jAlZyR2BFVM`
- SPF: `v=spf1 include:spf.efwd.registrar-servers.com ~all`

Do not delete or modify the MX/TXT records during website cutover.

## Cutover sequence

1. At Namecheap, replace the current nameservers with:
   - `gordon.ns.cloudflare.com`
   - `isla.ns.cloudflare.com`
2. Wait until the Cloudflare zone status changes from `pending` to `active`.
3. In the Pages project, add both custom domains:
   - `hydemedspaclearfield.com`
   - `www.hydemedspaclearfield.com`
4. Wait for both custom domains and SSL certificates to become active.
5. Make `www.hydemedspaclearfield.com` the preferred public hostname.
6. Configure a one-hop apex-to-WWW redirect.
7. Replace the old Weebly A records only through the Pages custom-domain process. Do not manually guess a Pages IP address.
8. Change `robots.txt` from staging blocking to production crawling:
   ```
   User-agent: *
   Allow: /

   Sitemap: https://www.hydemedspaclearfield.com/sitemap.xml
   ```
9. Deploy the approved commit after the production robots change.
10. Validate on the real domain:
    - Homepage
    - Services, About and Contact
    - Laser Hair Removal, Botox, Facials, Waxing, Lashes and Massage
    - Boulevard booking links
    - Phone and email links
    - Local hero image
    - Blog hub and preserved articles
    - Sitemap and robots
    - Representative legacy redirects
    - Custom 404
11. Submit `https://www.hydemedspaclearfield.com/sitemap.xml` in Google Search Console.
12. Keep the old Weebly account/site available temporarily as rollback protection.

## Rollback

If production validation fails:

1. Restore the apex and WWW records to `199.34.228.77`.
2. Keep all MX and TXT records unchanged.
3. Remove or pause the Pages custom domains if necessary.
4. Confirm the old Weebly site loads on apex and WWW.
5. Repair staging, pass the quality gate again, and retry cutover.

## Launch acceptance criteria

- Cloudflare zone Active
- Both custom domains Active
- Universal SSL active on apex and WWW
- One-hop preferred-host redirect
- No broken core pages or assets
- Boulevard booking opens correctly
- 70 sitemap URLs are valid, unique and self-canonical
- 348 legacy redirect rules have valid final targets
- Zero redirect chains
- Production robots allows crawling
- MX, SPF and Google verification records preserved
