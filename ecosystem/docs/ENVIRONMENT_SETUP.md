# Cloud environment configuration

The running instance has Python 3.12, Git and C11 cc. All seven clean independent
checkouts are present at the tested lock. No Python dependency installation or
persistent service is needed. The feature branch must be present in the checkout
(or subsequently merged) before these scripts can run; no script switches branches.

Saved draft fields for environment settings:

- install_script: validate checkout/cc, clone missing dependencies with
  `sync --require-lock`, check lock, run offline ecosystem tests.
- start_skill: use existing isolated checkout, preserve refs/work, run doctor,
  baseline and integration/protocol/demo checks; demo manages its own loopback server.
- network: add only api.github.com to custom allowed domains; existing package
  manager presets are preserved. Git transport already works; the GitHub API
  CONNECT request was refused by the proxy before authentication could be tested.

Saving a draft does not apply settings to this instance or publish a snapshot.
Review and save changes in environment settings, then publish the environment
when the reviewed feature checkout should become its prepared snapshot. After
network settings take effect, retry draft-PR creation; no new credential has been
requested because Git already authenticates and API authentication is untested.
