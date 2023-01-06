# Dummy comment
ARG BASE_IMAGE=jupyter/base-notebook

FROM ${BASE_IMAGE} as base

COPY software-engineer-technical-test /home/jovyan/work/software-engineer-technical-test
