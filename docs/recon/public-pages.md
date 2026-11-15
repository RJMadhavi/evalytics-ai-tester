---
id: EVA-DOC-003
title: Public Pages Reconnaissance
story: EVA-S0005
status: Desk review complete. Browser checks pending (section 9)
sut_version: v1.1.0
date: 2026-11-15
---

# Public Pages Reconnaissance

**Scope:** pages anyone can open without logging in. Nothing here needed authentication, and no form was submitted.

**Method and limits:** this document was compiled by reading the text of four public pages (home, pricing, login, create-academy). It has no screenshots, and it cannot show colours, layout, behaviour of sliders and toggles, console errors, cookies or network calls. Two pages (`/register`, `/forgot-password`) could not be read this way. Everything marked **Unconfirmed** needs a quick look in a real browser, listed in section 9. Observations are hypotheses, not confirmed defects.

**Privacy note:** the home page shows names of real students in testimonials. They are deliberately left out of this repo.

## 1. Page inventory

| Route | Purpose | Status | Footer version |
|-------|---------|--------|----------------|
| `/` | Landing page: features, Genie AI, how it works, roles, security claims, testimonials | Read | v1.1.0 |
| `/pricing` | Four plans, seat calculator, AI add-ons, FAQ, plan summary and "Proceed" | Read | v1.1.0 |
| `/login` | Email and password sign-in, 30-day "keep me logged in", invite-code join | Read | v1.1.0 |
| `/create-academy` | Academy and first-teacher sign-up form | Read | v1.1.0 |
| `/register` | Linked from login as "Create an Account" | **Not read** (browser check needed) | |
| `/forgot-password` | Linked from login | **Not read** (browser check needed) | |

**How the pages connect:** every "Create Academy" button on the home page goes to `/pricing`. The pricing page's plan summary has a "Proceed" link that goes to `/create-academy`. So the sign-up path is home → pricing → create-academy → (teacher account, then approval). `/login` is linked from the header and from the Genie and call-to-action sections.

## 2. Page details

### 2.1 Home (`/`)

**What it contains**
- Header: Features, Genie AI, How it Works, Who It's For, Security (all in-page anchors), plus Pricing, Sign In and Create Academy.
- Hero with a demo academy card showing sample figures (628 questions, 94% average, 42 students) and a sample question with options.
- A feature grid of 15 items: Genie, AI question extraction, equation converter, AI explanations, test paper builder, scheduled exam windows, results and analytics, activity log, four languages, enrollment management, difficulty tags, multi-teacher academy and own academy portal.
- A Genie section with example questions and a demo chat showing a score table.
- A four-step "zero to first exam" guide and separate lists for teachers and students.
- A "Your Data is Safe" section with seven claims (section 5).
- A testimonials strip, a closing call to action and a footer.

**Observations**

| ID | Observation | Type | Initial severity | Status |
|----|-------------|------|------------------|--------|
| REC-01 | Every "Create Academy" button goes to `/pricing`, not `/create-academy`. Probably by design, because a plan is chosen first. | Info | n/a | Confirm intent with owner |
| REC-02 | The footer has no Terms, Privacy or Contact links. The home page makes data-handling promises but links no policy. | Content / compliance | S3 | Unconfirmed (check the full footer in a browser) |
| REC-03 | The portal is described as live "instantly" and "in under 2 minutes", but the create-academy page says "Approval within 24 hrs". | Content / claim | S3 | Unconfirmed, test in S0006 |
| REC-08 | The testimonial list repeats (looks like a carousel loop). One author appears more than once per loop with different ratings. | UI / a11y | S4 | Unconfirmed |
| REC-09 | Each testimonial has "Ease of use" and "Helpfulness" labels but the text shows no values. They are probably star icons. Check they have text alternatives. | Accessibility | S3 | Unconfirmed |
| REC-10 | The teacher list says "Separate teacher login page", but `/login` is one page that finds the academy from the email. | Question | n/a | Ask owner or verify after login |
| REC-15 | The stats strip says "∞ Questions", but no question-bank limit is stated for any plan. | Question | n/a | Verify in S0006 |

**Test ideas**
- Every anchor link scrolls to the right section and focus moves with it.
- Header and footer links are the same on every page.
- Keyboard-only use of the header, the carousel and the call-to-action buttons.
- The page works on narrow screens and keeps the demo card readable.

### 2.2 Pricing (`/pricing`)

**What it contains**
- A Monthly / Academic Year (10 months) toggle.
- **Solo:** ₹999 a month, ₹9,990 a year, 1 teacher, up to 50 students.
- **Academy:** ₹1,099 a month, "from 4 teachers · 10 students", marked "Most popular".
- **Pro:** ₹1,999 a month, "from 4 teachers · 10 students".
- **Enterprise:** custom price, contact by email link.
- A seat calculator for Academy and Pro (teachers and students sliders), a list of AI add-ons, a five-question FAQ and a plan summary with "Proceed".

**Arithmetic checked:** ₹9,990 is exactly 10 × ₹999, which matches the claim that the academic year costs 10 months at the monthly rate. June to March is 10 months.

**Observations**

| ID | Observation | Type | Initial severity | Status |
|----|-------------|------|------------------|--------|
| REC-04 | "White-label branding" and "API access" are listed as included under Academy, but marked "Soon" under Pro, which says "Everything in Academy". Pro also lists "Custom domain" as "Soon". | Content | S3 | Unconfirmed |
| REC-05 | Academy and Pro both say "from 4 teachers · 10 students" although they cost ₹1,099 and ₹1,999. The text does not say what differs. | Copy | S4 | Unconfirmed |
| REC-06 | The Solo card lists "AI add-ons" and "Multi-teacher management" while limited to 1 teacher. The add-ons section says they are "Available on Academy and Pro". They may be shown greyed out, which text cannot show. | Content | S3 | Needs visual check |
| REC-07 | Both calculators show range labels that read `420` and `101000`. Likely min and max values (4 to 20 teachers, 10 to 1000 students) with no separator. This could be a real rendering problem or an artefact of reading text only. | UI | S3 | **Needs visual check** |
| REC-11 | The header says "Cancel anytime", but the Academic Year plan is paid upfront. No cancellation or refund rule is visible. | Content / question | S4 | Ask owner |
| REC-12 | Only Solo shows an academic-year price in the default view. Academy and Pro prices for that mode need the toggle to be checked (expected ₹10,990 and ₹19,990 if the rule is 10 × monthly). | Check | n/a | Needs browser |

**Test ideas**
- Toggle monthly and academic year, and check every price and the plan summary update.
- Move both sliders to their minimum, maximum and out-of-range values (typing, keyboard arrows) and check prices and labels.
- Switch plans and check the summary ("Plan, Billing, Teachers, Students, Total") matches the calculator.
- Click "Proceed" and check whether the chosen plan carries over to `/create-academy` (see REC-17).
- Boundary: Solo is capped at 50 students, so test the 51st later (needs a tenant).
- The Enterprise button is an email link. Do not use it for testing.

### 2.3 Login (`/login`)

**What it contains:** email, password, "Keep me logged in for 30 days", a forgot-password link, a "Create an Account" link, and a box for new students to enter an invite code and press "Join". The text says the system takes you to your academy automatically from your email.

**Observations**

| ID | Observation | Type | Status |
|----|-------------|------|--------|
| REC-L1 | The login finds the academy from the email, but a student can belong to several academies with one login. What happens then is unknown. | Question | Test after login (S0007) |
| REC-L2 | "Keep me logged in for 30 days" ties into the session claims (section 5). | Security check | Needs authorization |
| REC-L3 | The invite-code box is on the login page. Valid, invalid, expired and reused codes should be tested. | Test idea | Needs a tenant |

**Test ideas (public, harmless):** empty submit, an invalid email format, a made-up email with a wrong password (watch the error message text, and whether it reveals if the email exists), tab order, and the show/hide password control if present. Do **not** repeat wrong-password attempts here. Lockout testing needs owner approval and your own accounts.

### 2.4 Create academy (`/create-academy`)

**What it contains:** academy name, subdomain (lowercase letters, numbers and hyphens only, shown as `yourname.evalytics.in` live), your name, subject (optional dropdown with 10 choices), email, password, confirm password, a Terms and Privacy line, and a "Create Academy" button. Below it: "Secure & Encrypted", "Approval within 24 hrs", "Free to Start".

**Observations**

| ID | Observation | Type | Initial severity | Status |
|----|-------------|------|------------------|--------|
| REC-02b | The Terms of Service and Privacy Policy links point to `#`, so there is no policy page behind them. | Content / compliance | S3 | Unconfirmed (click them to confirm) |
| REC-03b | "Approval within 24 hrs" suggests someone approves each new academy, which conflicts with "live instantly" on the home page. | Claim | S3 | See REC-03 |
| REC-16 | Password rules are not shown. Only the subdomain rule is stated. | Test idea | n/a | Test in S0006 |
| REC-17 | The page does not show which plan or billing choice was made on `/pricing`. | Question | n/a | Check how it carries over |
| REC-18 | If new academies need manual approval, creating the QA tenant may need the owner's help. | Planning risk | n/a | Ask owner before S0006 |

**Test ideas (for S0006, once the owner confirms scope):** subdomain rules (empty, 1 character, very long, uppercase, spaces, leading or trailing hyphen, reserved words such as `www` or `admin`, a name already taken), password mismatch, weak passwords, duplicate email, invalid email, the live subdomain preview, double-click on the button, and what the confirmation or pending screen says.

### 2.5 Register and forgot password

Not read. Open both in a browser and fill in the table in section 9. For `/forgot-password`, check only the page itself. Don't trigger a reset email to any address you don't own.

## 3. Cross-page findings

| ID | Observation | Severity | Status |
|----|-------------|----------|--------|
| REC-13 | Page titles use different separators (an en dash on home, login and create-academy, an em dash on pricing). Head metadata also varies: pricing, login and create-academy declare mobile web-app and theme-colour tags, while the home page text shows only a viewport tag. | S4 | Unconfirmed |
| REC-14 | Footer wording differs: the home page has its own line, and the other pages share "Empowering learners, one test at a time". | S4 | Cosmetic |
| REC-19 | The version `v1.1.0` appears in the footer of all four pages read. Use it to tag every test run and for change detection later. | n/a | Confirmed |

## 4. Page-flow map

```
Home (/) ──Create Academy──► Pricing (/pricing) ──Proceed──► Create Academy (/create-academy)
   │                              │                                   │
   └──Sign In──► Login (/login) ◄─┴────────── Sign In ────────────────┘
                   ├─ Forgot password ► /forgot-password  (not read)
                   ├─ Create an Account ► /register        (not read)
                   └─ Invite code ► Join
```

## 5. Claims register

Every promise made on the public pages, and when to test it.

| # | Claim | Seen on | How to verify | Story or epic |
|---|-------|---------|---------------|---------------|
| C1 | HTTPS on every page | Home | Browser address bar, and `http://` redirect | S0005 (now) |
| C2 | Zero third-party trackers | Home | DevTools Network tab: list outside domains | S0005 (now) |
| C3 | No ads, no selling of data | Home | Network tab for ad domains. Selling can't be tested from outside. | S0005 / security |
| C4 | Academic year = 10 months at the monthly rate | Pricing | Solo arithmetic checked. Verify Academy and Pro with the toggle. | S0005 (now) |
| C5 | Portal live "instantly" / "under 2 minutes" | Home | Time the sign-up. Compare with "Approval within 24 hrs". | S0006 |
| C6 | Zero to first exam in 15 minutes | Home | Time the whole walkthrough | S0006 / S0007 |
| C7 | 15-day trial, AI limits 5 uploads, 5 generations, 5 Genie questions | Pricing | Check in the trial academy | S0006 |
| C8 | Extraction "in under 10 seconds", including diagrams and formulas | Home | Timed uploads of the golden PDFs | E11 (AI testing) |
| C9 | Instant results after submission | Home | Submit a test exam and time it | E07 |
| C10 | 10-minute warning, auto-save, auto-submit | Home | Short exam windows in the QA tenant | E07 |
| C11 | Four languages (English, Hindi, Marathi, Kannada) | Home | Language switch tests | E11 |
| C12 | Genie answers from live data | Home | Known-answer question set | E11 |
| C13 | Wrong-password lockout | Home | Own accounts only, with owner approval | E10 (security) |
| C14 | Session tied to a device, logged out when used elsewhere | Home | Own accounts only, with owner approval | E10 (security) |
| C15 | Academy data fully isolated | Home | Two tenants you control | E10 (security) |
| C16 | Passwords never stored in plain text | Home | Can't be tested directly. Indirect check: a reset sends a link, never your password. | E10 |
| C17 | A student can join several academies with one login | Pricing | Two tenants you control | S0007 |
| C18 | Solo allows up to 50 students | Pricing | Boundary test with the 51st request | E07 |

## 6. Open questions for the owner

Carry these into story S0011 (some are already in the email you sent).

1. Do new academies need manual approval, and can the QA academy be approved quickly or in advance? (REC-18)
2. Where are the Terms of Service and Privacy Policy? (REC-02)
3. Is "White-label branding" and "API access" meant to be in Academy, in Pro, or both? What differs between Academy and Pro at the same starting seats? (REC-04, REC-05)
4. Is there a separate teacher login page, or does `/login` serve everyone? (REC-10)
5. What are the cancellation and refund rules for the Academic Year plan? (REC-11)
6. Is there a limit on questions in a question bank? (REC-15)
7. Does the plan chosen on `/pricing` carry over to account creation, and how? (REC-17)

## 7. Draft bugs

None are confirmed yet. Confirm the following with a visual check first, then decide whether to log them as `EVA-B####` files. A defect is only worth logging once you have a screenshot or steps that reproduce it.

| Candidate | From | Needs |
|-----------|------|-------|
| Seat calculator range labels merged | REC-07 | Screenshot of the pricing page at desktop and phone widths |
| Plan matrix inconsistency (white-label, API) | REC-04 | Screenshot of the Academy and Pro cards |
| Terms and Privacy links lead nowhere | REC-02b | Click both links and record the address you land on |
| Solo card lists features it does not have | REC-06 | Screenshot showing whether items are greyed out |

## 8. Acceptance criteria for S0005

- [x] Public pages `/`, `/pricing`, `/login`, `/create-academy` documented
- [ ] `/register` and `/forgot-password` documented (browser)
- [ ] Screenshots saved under `docs/recon/screenshots/` (browser)
- [x] Questions for the owner listed
- [x] Anything surprising logged as an unconfirmed observation

## 9. Browser checks still to do

About 45 minutes. Tick them as you go and update the matching IDs above.

- [ ] Take a full-page screenshot of each of the six pages (desktop). Crop out real student names and faces.
- [ ] Take one screenshot of pricing and one of create-academy at phone width
- [ ] Open `/register` and `/forgot-password`. Record fields, buttons, links and the footer version. Do not submit.
- [ ] Pricing: confirm REC-07 (calculator labels), REC-06 (Solo card styling), REC-12 (toggle prices) and REC-04 (white-label and API on Academy and Pro)
- [ ] Click the Terms and Privacy links on create-academy and the home footer (REC-02)
- [ ] Type `http://evalytics.in` and check it redirects to HTTPS (C1)
- [ ] Open a made-up address such as `/does-not-exist` and record the 404 page
- [ ] DevTools, Network tab, reload the home page: list the domains that are not `evalytics.in` (C2, C3)
- [ ] DevTools, Application tab, Cookies, on first visit: record cookie **names** only, never values
- [ ] DevTools, Console: record any red errors on each page
- [ ] Keyboard check: tab through the header, the testimonials and the forms. Note anything that cannot be reached or seen.
- [ ] Update the status column of each observation to Confirmed, Not reproduced or Needs more info
