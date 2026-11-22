# Phase 2: worker image running EU-Flex from its official conda lock file.
FROM mambaorg/micromamba:1.5-jammy

ARG EUFLEX_REPO=https://github.com/EU-ACER/eu-flex-model.git
# Pin a specific commit; record it in every exported run.
ARG EUFLEX_COMMIT=main

USER root
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
USER $MAMBA_USER

WORKDIR /opt/eu-flex-model
RUN git clone ${EUFLEX_REPO} . && git checkout ${EUFLEX_COMMIT}

RUN micromamba create -y -n eu-flex -f envs/linux-64.lock.yaml && micromamba clean -a -y
ENV ENV_NAME=eu-flex
RUN micromamba run -n eu-flex pip install --no-deps -e .

COPY --chown=$MAMBA_USER:$MAMBA_USER adapter /opt/adapter
RUN micromamba run -n eu-flex pip install -e /opt/adapter

ENV EUFLEX_COMMIT=${EUFLEX_COMMIT}
WORKDIR /runs
# TODO: replace with the Arq worker entrypoint
CMD ["micromamba", "run", "-n", "eu-flex", "snakemake", "--version"]
