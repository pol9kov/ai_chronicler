FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN pip install --no-cache-dir poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi
COPY . /app/
ENV HF_HUB_ENABLE_HF_TRANSFER=1
RUN python - <<PY
from huggingface_hub import hf_hub_download
hf_hub_download(repo_id="NousResearch/TinyLlama-1.1B-Chat-v1.0-GGUF",
                filename="tinyllama-1.1b-chat-v1.0.Q8_0.gguf",
                local_dir="models", local_dir_use_symlinks=False,
                resume_download=True)
PY
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
