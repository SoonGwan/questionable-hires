# Build only from an explicitly staged, credential-free context.
ARG BASE_IMAGE
FROM ${BASE_IMAGE}
ARG PROJECT
ENV PATH=/opt/miniconda3/envs/testbed/bin:/usr/local/bin:/usr/bin:/bin
COPY wheels/ /opt/qh-wheels/
COPY ca.pem /opt/qh-ca.pem
COPY prepare.py /opt/qh-prepare.py
RUN python /opt/qh-prepare.py ${PROJECT}
# Same CLI release as the preceding model experiments; no auth is copied here.
RUN curl -fsSL https://chatgpt.com/codex/install.sh -o /tmp/qh-codex-install.sh \
    && env CODEX_RELEASE=0.153.4 CODEX_NON_INTERACTIVE=true \
       CODEX_INSTALL_DIR=/usr/local/bin CODEX_HOME=/opt/qh-codex-install \
       sh /tmp/qh-codex-install.sh \
    && test "$(codex --version)" = "codex-cli 0.153.4"
ENV PIP_NO_INDEX=1 PIP_FIND_LINKS=/opt/qh-wheels PYTHONDONTWRITEBYTECODE=1
WORKDIR /testbed
