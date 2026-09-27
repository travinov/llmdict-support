# LLM Dict — Support & Privacy

Static Russian and English support and privacy pages for the LLM Dict iOS app.

## Public pages

- Russian support: https://travinov.github.io/llmdict-support/
- English support: https://travinov.github.io/llmdict-support/en/
- Russian privacy: https://travinov.github.io/llmdict-support/privacy/
- English privacy: https://travinov.github.io/llmdict-support/en/privacy/

Contact: **llmdict.support@gmail.com**

## Edit and preview

Page content is in `content/ru.json` and `content/en.json`. The developer identity, contact and canonical URL are in `content/site.json`. The developer name is taken from the app's Apple development team profile.

After changing content, run:

```sh
python3 scripts/build.py
python3 -m http.server 8769 --bind 127.0.0.1 --directory docs
```

Open `http://127.0.0.1:8769/`. CSS and the email-copy enhancement live in `docs/assets/`. All content, language navigation and email links work without JavaScript. Copying uses the browser clipboard API, with a manual-copy fallback.

Commit both content and generated HTML. GitHub Pages publishes **main → /docs**. The custom domain field stays empty; the built-in `github.io` address is used with HTTPS. There is no package installation or framework build.

## Data and scope

The website uses no third-party scripts, external fonts, analytics, cookies or localStorage. GitHub Pages may log IP addresses for security, as disclosed in the policy. Email is handled by the user's email client and Gmail. There is no web form, upload endpoint or app backend in this repository.

The privacy text describes version 1.0, including explicit per-service consent and withdrawal, provider-managed retention, OpenAI Responses storage behavior, and deletion of the Live cache together with its recording. Publishing this site does not constitute App Store approval.

The app icon is reused as the website's brand mark. This repository contains website files and a demonstration recording for TestFlight review. No application source, API keys or signing assets are included.

## TestFlight demonstration

The supplied screen recording is available from `docs/review/1.0-17-45eb614f/`. Its landing page is not linked from the support navigation and requests no indexing; this is not access control, and the public repository and video remain accessible. The original local recording is preserved; the hosted H.264 copy keeps the complete timeline.
