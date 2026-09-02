# CARE Codespaces / Dev Container base image.
#
# Built on the upstream devcontainers Python image, with two Codespaces build
# blockers fixed at the image layer -- before any dev container *feature* runs.
# A feature that fails to install fails the whole container build, which is what
# drops freshly created Codespaces into recovery mode (Error 1302).
#
#  1. Broken Yarn apt repo:
#     The upstream image ships /etc/apt/sources.list.d/yarn.list, whose signing
#     key is no longer resolvable (apt reports "NO_PUBKEY 62D54FD4003F6525").
#     That makes `apt-get update` exit 100 and breaks every feature that installs
#     apt packages (e.g. apt-get-packages). CARE's backend is Python-only and
#     never uses Yarn, so the repo is removed here.
#
#  2. GitHub API rate limits:
#     The devcontainers-extra "direnv" feature resolves its binary through the
#     GitHub Releases API, and "apt-get-packages" installs via nanolayer too.
#     Unauthenticated GitHub API requests from the Codespaces build network are
#     rate-limited (HTTP 403: rate limit exceeded), which intermittently fails
#     the build. Installing these tools directly from apt avoids the API
#     entirely and is fully deterministic.
FROM mcr.microsoft.com/devcontainers/python:1-3.13-bookworm

RUN set -eux; \
    # Drop the unusable Yarn source, plus any other apt source still pointing at
    # dl.yarnpkg.com, then refresh apt metadata so it resolves cleanly.
    rm -f /etc/apt/sources.list.d/yarn.list; \
    grep -rlE 'dl\.yarnpkg\.com' /etc/apt/ 2>/dev/null | xargs -r rm -f; \
    apt-get update; \
    # OS build/runtime dependencies (native psycopg / Pillow builds, gettext for
    # translations, etc.) plus direnv -- previously provided by the
    # apt-get-packages and direnv features.
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        libjpeg-dev \
        zlib1g-dev \
        libpq-dev \
        gettext \
        wget \
        curl \
        gnupg \
        direnv; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*
