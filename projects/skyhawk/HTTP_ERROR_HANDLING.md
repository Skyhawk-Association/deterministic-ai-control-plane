# Skyhawk HTTP Error Handling and Alerting Design

**Status:** APPROVED DESIGN / 5xx FRONT-LAYER FALLBACK IMPLEMENTED 2026-10-09 / EXTERNAL UPTIME WATCH PARTIAL (HOURLY, BELOW DESIGN CADENCE) / 400-403-429 STATIC PAGES AND LOCAL MONITORING NOT YET IMPLEMENTED
**Decision date:** 2026-10-08
**Owner:** Skyhawk front web/security layer for infrastructure errors; Drupal for application-level errors when Drupal is healthy.

## Objective

Provide useful, branded, low-information error responses without depending on PHP, Drupal, or the database when the failure itself may make those services unavailable. Pair the visitor experience with monitoring that detects real outages without turning routine bot traffic into an email cannon.

## Verified current state

- Public traffic reaches nginx first, then Apache, then PHP-FPM/Drupal.
- Normal nonexistent URLs reach Drupal and render the branded Bolter! 404 page.
- nginx/security-layer denials can return the stock nginx 403 page before Drupal.
- Current Skyhawk nginx vhosts contain error_page 500 = @custom but no active 503 handler.
- Current Skyhawk Apache vhosts contain no site-specific 4xx/5xx ErrorDocument directives.
- Apache's packaged multilingual 503 document exists, but its config include is disabled.
- Drupal maintenance mode depends on Drupal/PHP remaining available and therefore cannot cover backend/socket failures.
- In a recent 5,000-line access-log sample, 404 and 403 responses were frequent enough that per-hit email would be noisy.

## Ownership map

| HTTP class | Primary owner | Visitor handling |
| --- | --- | --- |
| 400 | nginx/security layer | Small static generic page |
| 401 | nginx/security layer when generated there | Small static generic page |
| 403 | nginx/ModSecurity when blocked before Drupal; Drupal when application-owned | Static front-layer page or Drupal page, preserving the actual owner |
| 404 | Drupal for normal site routes | Keep existing branded Bolter! page |
| 429 | nginx/security/rate-limit layer | Small static generic page with retry language |
| 500 | Front layer must have static fallback; Drupal may render an application error when healthy | Branded static fallback if backend cannot respond |
| 502 | nginx/front layer | Branded static fallback |
| 503 | nginx/front layer | Branded static fallback |
| 504 | nginx/front layer | Branded static fallback |

Do not force all errors through one layer. The response must remain available when the lower layer is the thing that failed.

## Static page set

Create one lightweight static HTML asset family outside Drupal execution:

- 400.html - We could not understand that request.
- 403.html - That request is not permitted.
- 429.html - Too many requests. Please wait a moment and try again.
- 500.html - The Skyhawk Association site encountered a problem.
- 502.html - The site is temporarily unable to reach part of its service.
- 503.html - The Skyhawk Association site is temporarily unavailable. Please try again shortly.
- 504.html - The site did not receive a response in time. Please try again shortly.

The pages should:

- identify The Skyhawk Association;
- use restrained Skyhawk branding;
- avoid PHP, JavaScript, database calls, Drupal bootstrap, remote fonts, analytics, or third-party assets;
- avoid publishing technical details, server identities, paths, versions, or security rules;
- return the original HTTP status rather than converting failures to HTTP 200;
- include a link to / where appropriate;
- be usable with CSS embedded directly in the HTML or from a static local asset that nginx can serve independently;
- stay small enough to serve reliably during degraded conditions.

404 remains Drupal-owned because the current branded page already works and can provide useful site navigation.

## Front-layer routing design

### nginx

nginx is the required hard-failure owner because it is public-facing and can serve a static file without PHP/Drupal.

The intended behavior is equivalent to:

- map 500, 502, 503, and 504 to static internal locations;
- map front-layer 400, 403, and 429 to static internal locations where practical;
- use internal locations so visitors cannot misuse the error assets as alternate application endpoints;
- preserve the triggering status code.

Do not edit generated skyhawk.org.conf / skyhawk.org.ssl.conf directly as the durable solution. CWP is known to rebuild vhost files. CWP documentation/community guidance indicates custom vhost templates should be created and assigned per domain rather than editing generated vhosts in place.

Resolved 2026-10-09: templates live in /usr/local/cwpsrv/htdocs/resources/conf/web_servers/vhosts/nginx/ (custom pair skyhawk-errors.tpl / skyhawk-errors.stpl). The per-domain owner is /home/n790725/.conf/webservers/skyhawk.org.conf, set through CWP admin WebServer Settings -> WebServers Domain Conf with "Rebuild WebServers conf for domain on save". Do not use /scripts/cwp_api webservers rebuild_all for Skyhawk changes.

### Apache

Apache does not need to become the primary hard-failure page owner if nginx intercepts backend failures correctly.

Application-generated 403/404 responses should normally pass through so Drupal can continue owning those cases.

Do not enable the global Apache multilingual error-doc config merely to solve Skyhawk. That would broaden scope beyond the domain and would still not cover nginx-level/backend-unreachable failures cleanly.

## Monitoring and alerting design

### Primary availability detector: external

Whole-site availability must be checked from outside the VPS. An internal script cannot reliably report that its own server, network path, or public TLS endpoint is dead.

**Primary external monitor 2026-10-08:** UptimeRobot monitor "skyhawk.org" checks https://skyhawk.org from North America; test DOWN and UP email notifications were delivered to saweba4master1 on 2026-10-08. Check interval, real-incident detection and account timezone remain to be verified. See LOST-D.

**Secondary watch 2026-10-08:** an enabled ChatGPT condition-watch automation named `Skyhawk Uptime Watch` runs hourly and checks `https://skyhawk.org` externally. Its configured action is to diagnose a detected outage, notify in ChatGPT, and send outage/recovery email through connected Gmail. This is PARTIAL relative to the approved design: the automation platform cadence is hourly, so it cannot perform the required second check about one minute later or require two good checks on recovery. The prompt also does not measure response time or explicitly check certificate expiry. Automation configuration and latest-run timestamp are verified; the available automation interface does not expose a multi-run result history. Actual outage-triggered Gmail delivery and recovery delivery remain unverified.

External checks should cover:

- HTTPS reachability;
- expected HTTP 200 on /;
- TLS validity;
- response time;
- 5xx status detection.

Recommended alert policy:

- 502/503/504: alert after 2 consecutive failed checks separated by about 1 minute.
- 500: alert after 3 occurrences/check failures within 5 minutes.
- Complete timeout/TLS/DNS failure: alert after 2 consecutive checks.
- Recovery: send one recovery notification after 2 consecutive successful checks.

This avoids one transient blip generating drama while still catching a genuine outage within a few minutes.

### Secondary diagnostic detector: local

Local monitoring should summarize nginx/Apache/ModSecurity/PHP-FPM evidence and report only when thresholds are crossed.

Recommended policy:

- 403: no per-hit email. Log normally. Daily digest only if useful, or alert when a protected/important route shows an unusual spike.
- 404: no per-hit email. Optional daily digest of top missing URLs; separately alert only for known important URLs expected to exist.
- 429: threshold alert if sustained, because it may indicate abuse or an overly aggressive rule.
- 500/502/503/504: immediate local event capture, with email only when the rate threshold is crossed.
- Rate-limit duplicate alerts so one incident creates one opening alert, periodic reminders only if materially useful, and one recovery message.

Local alert messages should include:

- timestamp;
- affected host;
- status class;
- count/window;
- top failing URLs where safe;
- nginx/Apache/PHP-FPM service state;
- PHP-FPM socket presence when relevant;
- whether the public external check is also failing.

Do not include secrets, tokens, private member information, full request bodies, or unnecessary attacker-controlled strings.

## Email / event behavior

Email is appropriate for actionable incidents, not raw events.

Preferred hierarchy:

1. External monitor creates the primary outage event.
2. Local monitor enriches the event with server evidence.
3. One notification is sent for the incident.
4. Duplicate events are coalesced during the incident window.
5. One recovery notification closes the incident.

If email transport from the VPS itself is impaired, the external monitor remains independent and still reports the outage.

## Implementation sequence

1. Obtain root-capable inspection of the active CWP nginx template mechanism.
2. Identify the exact per-domain template pair that generates the HTTP and HTTPS Skyhawk nginx vhosts.
3. Copy to a Skyhawk-specific custom template pair rather than editing CWP defaults.
4. Create the static error assets in a user-owned, nginx-readable location outside Drupal execution.
5. Add only the necessary Skyhawk-domain error mappings to the custom templates.
6. Validate nginx configuration syntax before reload.
7. Rebuild/apply the Skyhawk domain configuration through the CWP-supported mechanism.
8. Reload nginx only after syntax passes.
9. Verify ordinary / remains HTTP 200 and the current Drupal Bolter! 404 remains unchanged.
10. Test each static error page through a non-disruptive dedicated test location or temporary test hostname/path that intentionally returns the status without breaking production.
11. Regenerate the Skyhawk vhost through CWP once more and verify the custom behavior survives regeneration.
12. Only then classify the error-page path as regeneration-safe.
13. External monitoring: UptimeRobot is primary (monitor exists, test alert delivery verified); verify interval and a real or controlled incident. The hourly ChatGPT `Skyhawk Uptime Watch` is a secondary backup below design cadence.
14. Add local threshold/digest monitoring.
15. Test alert opening, duplicate suppression, and recovery notification end to end.

## Success evidence

Implementation is complete only when all of the following are verified:

- normal Skyhawk homepage remains 200;
- Drupal 404 remains the branded Bolter! response;
- front-layer 403 presents the approved static response where nginx/security owns the denial;
- 500/502/503/504 static pages return their original status and do not require PHP/Drupal;
- configuration survives an actual CWP domain-vhost regeneration;
- external monitor detects a controlled test failure and sends one alert;
- local diagnostic monitor records/enriches the same test without mail flooding;
- recovery generates one recovery notification;
- production configuration and static assets are backed by a documented rollback path.

## Rollback

Rollback consists of:

- restore the previously assigned CWP Skyhawk vhost templates/configuration;
- rebuild the Skyhawk vhost through CWP;
- validate nginx syntax;
- reload nginx;
- verify homepage 200 and Drupal 404 behavior.

Static error files may remain harmlessly on disk after rollback because they are inert without active mappings.

## Current implementation boundary

IMPLEMENTED AND VERIFIED (2026-10-09, see projects/skyhawk/LOST-D.md "HTTP ERROR HANDLING ACTIVATED 2026-10-09"):

- nginx static fallback for 500/502/503/504 on skyhawk.org via the CWP-assigned skyhawk-errors template pair, with proxy_intercept_errors on and an internal /_skyhawk_errors/ location aliased to /var/www/skyhawk-errors/.
- Drupal-owned 403/404 verified unchanged in production; 5xx status preservation verified on an isolated nginx instance with identical directives.
- Configuration produced by a CWP domain rebuild from template + per-domain JSON (PHP-FPM 8.4 preserved).

Accepted side effect: a Drupal application 500 or maintenance-mode 503 also shows the static page, with the correct status.

NOT IMPLEMENTED:

- Static front-layer 400/403/429. A 403 mapping combined with proxy_intercept_errors would replace Drupal-owned 403 pages, so it needs a scoped design (for example, mappings only inside the deny locations) before adding.
- External uptime monitoring: UptimeRobot primary monitor exists with test alert delivery verified; interval and real-incident detection unverified. The hourly ChatGPT watch is secondary. Local threshold/digest monitoring and end-to-end outage/recovery notification verification also remain open.
