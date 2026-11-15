---
id: EVA-DOC-003
title: Public Pages Reconnaissance
story: EVA-S0005
status: In progress
sut_version: v1.1.0
date: <2026-11-15>
---

# Public Pages Reconnaissance

Scope: pages anyone can open without logging in. Nothing here needs authentication. Write what you **see**, not what you assume. Anything odd goes in the Observations column as a question, not as a confirmed bug.

Use the browser's normal view for this, plus DevTools (right-click, Inspect) only to read, never to change anything.

## 1. Page inventory

| Route | Page purpose | Seen by me? | Screenshot | Observations / questions |
|-------|--------------|-------------|------------|--------------------------|
| `/` | Landing page: features, testimonials, call to action | Yes (pre-filled from first look) | `screenshots/home.png` | Testimonials look duplicated on the page. Check whether it is a carousel loop. |
| `/pricing` | Plans (Solo, Academy, Pro, Enterprise), seat calculator, monthly vs academic-year billing | Yes (pre-filled) | `screenshots/pricing.png` | "White-label" and "API access" differ between Academy and Pro. Calculator labels look merged (`420`, `101000`). Academy and Pro both say "from 4 teachers · 10 students". |
| `/login` | Email and password login, "keep me logged in for 30 days", forgot-password link, invite-code join box | Yes (pre-filled) | `screenshots/login.png` | Login finds the academy from the email. Footer shows `v1.1.0`. |
| `/register` | | | `screenshots/register.png` | |
| `/forgot-password` | | | `screenshots/forgot-password.png` | |
| `/create-academy` | | | `screenshots/create-academy.png` | Look, but **do not submit** the form until the owner confirms scope. Creating an academy is covered by story S0006. |

Add any other page you find through links (terms, privacy, contact, help, blog).

## 2. Checklist for each page

Tick these as you go. Copy this block under each page if you want notes per page.

- [ ] Page title in the browser tab makes sense
- [ ] One clear main heading
- [ ] Every link goes somewhere (no dead links, no wrong pages)
- [ ] Forms: labels, placeholders, required fields, what happens on an empty submit (public forms only, and only harmless ones like a wrong login with a made-up email)
- [ ] Error messages are readable
- [ ] Layout works on a narrow window (drag the window thinner) and on your phone
- [ ] Text is readable: size, contrast
- [ ] Footer shows the version number
- [ ] Browser console (DevTools, Console tab): note any red errors

## 3. Cross-page items

| Item | What to check | Result |
|------|---------------|--------|
| Header and navigation | Same on every page? Logo link goes home? | |
| Footer | Links, copyright year, version string | |
| Favicon and tab titles | Present and sensible | |
| HTTPS | `http://evalytics.in` redirects to `https://` | |
| Unknown page | Type a nonsense address (for example `/does-not-exist`). Is there a friendly 404? | |
| `robots.txt` and `sitemap.xml` | Open `https://evalytics.in/robots.txt` and `/sitemap.xml`. Do they exist? | |
| Third-party requests | DevTools, Network tab, reload the home page. List domains other than evalytics.in. The site claims zero third-party trackers. | |
| Cookies | DevTools, Application tab, Cookies. List names on first visit, before logging in. Do not copy values. | |

## 4. Claims to check on public pages

From the test plan, section 3.3. Mark each as Confirmed, Not confirmed or Needs login to check.

| Claim | Result | Notes |
|-------|--------|-------|
| "Zero third-party trackers" | | |
| Plan matrix is consistent across plans | | |
| Seat calculator shows correct ranges and prices | | |
| 15-day trial is described the same way everywhere | | |
| Pricing for monthly and academic-year (10 months) matches the calculator | | |

## 5. New questions for the owner

Add anything that needs the owner's answer here, then carry it to story S0011.

1. 
2. 

## 6. Draft bugs

List anything that looks like a real defect. Do not create bug files yet. Collect them here and review once recon is done.

| # | Page | What I saw | Expected | Evidence |
|---|------|------------|----------|----------|
| 1 | | | | |
