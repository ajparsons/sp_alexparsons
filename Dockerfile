FROM ghcr.io/mysociety/stringprint2:sha-5b5dccd

COPY pyproject.toml poetry.lock /setup/ 
COPY stringprint2/pyproject.toml stringprint2/poetry.lock /setup/stringprint2/
RUN mkdir /setup/stringprint_document_source \
    && touch /setup/stringprint_document_source/__init__.py \
    && mkdir --parents /setup/stringprint2/stringprint2/ \
    && touch /setup/stringprint2/stringprint2/__init__.py \
    && export PATH="/root/.local/bin:$PATH" \
    && cd /setup/ && poetry install \
    && echo "/workspaces/stringprint_document_source/stringprint2" > /usr/local/lib/python3.8/site-packages/stringprint2.pth