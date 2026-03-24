# Video Transcription & Analysis App — Product Requirements Document (PRD)

**Version:** 1.0
**Date:** 2026-03-24
**Author:** Morgan (PM — Synkra AIOX)

---

## Change Log

| Date       | Version | Description   | Author |
|------------|---------|---------------|--------|
| 2026-03-24 | 1.0     | Initial draft | Morgan |

---

## 1. Goals & Background Context

### Goals

- Transcrever automaticamente vídeos longos do YouTube (via URL) e Google Drive (via arquivo) com alta precisão
- Gerar documento estruturado com índice por tópicos e timestamps
- Destacar citações e trechos relevantes identificados automaticamente
- Suportar conteúdos de longa duração (~4h+) sem perda de qualidade
- Disponibilizar o resultado via interface web simples e acessível para uso pessoal

**Métricas de Sucesso:**
- Transcrição de vídeo de 4h com ≥90% de precisão em PT-BR
- Documento gerado com mínimo de 5 tópicos identificados e 3 destaques por tópico
- Pipeline completo concluído em background sem intervenção manual

### Background Context

O usuário frequentemente consome conteúdo longo em formato de live (YouTube/Google Drive) e precisa transformar esse conteúdo em material de referência textual. Transcrever manualmente 4 horas de vídeo é inviável. Esta solução pessoal automatiza o processo completo: ingestão do vídeo, transcrição por IA, segmentação por tópicos e geração de documento rico com destaques e citações.

O foco é praticidade para uso pessoal — interface web limpa, sem necessidade de configuração técnica avançada, entregando um documento final pesquisável e bem organizado.

### Build vs Buy Analysis

Soluções existentes foram avaliadas antes da decisão de construir:

| Solução | Limitação para este caso |
|---------|--------------------------|
| **YouTube auto-captions** | Baixa precisão em PT-BR; sem segmentação por tópicos; sem destaques |
| **Otter.ai** | Custo por minuto de áudio; limite de duração; dados na nuvem (privacidade) |
| **Descript** | Caro para uso pessoal; focado em edição de vídeo, não em análise |
| **AssemblyAI / Deepgram** | Custo por minuto (~$0.006-0.015/min = ~$1.44-$3.60 por vídeo de 4h); dados na nuvem |
| **Whisper API (OpenAI)** | ~$0.006/min = ~$1.44 por vídeo de 4h; dados enviados para OpenAI |

**Decisão: Build com Whisper local**
- ✅ Custo zero por transcrição (após setup)
- ✅ Privacidade total (nada sai da máquina local)
- ✅ Personalização completa do documento de saída
- ✅ Sem limites de duração ou volume
- ⚠️ Trade-off: setup mais complexo; velocidade dependente do hardware

---

## 1.1 Out of Scope (MVP)

Os seguintes itens estão explicitamente fora do escopo do MVP:

- **Múltiplos idiomas simultâneos** — suporte apenas a PT-BR no MVP; outros idiomas via configuração manual em v1.1
- **Autenticação de usuários** — sem login, cadastro ou multi-usuário; aplicação de uso estritamente pessoal e local
- **Histórico de jobs** — sem persistência de jobs anteriores; cada sessão é independente
- **Speaker diarization** — sem identificação de múltiplos falantes ("quem disse o quê")
- **Cloud deploy** — execução exclusivamente local via Docker Compose; sem deploy em servidor remoto no MVP
- **Integração com ferramentas externas** — sem export direto para Notion, Obsidian, Google Docs no MVP
- **Vídeos privados do YouTube** — sem suporte a vídeos com restrição de idade ou acesso privado
- **Processamento simultâneo de múltiplos vídeos** — fila processa um job por vez no MVP

### Future Enhancements (v1.1+)

- Speaker diarization (identificação de múltiplos falantes)
- Suporte a múltiplos idiomas
- Histórico de jobs com busca
- Export direto para Notion/Obsidian
- Interface para upload de arquivo local (além de URL)
- Summarização executiva automática por tópico

---

## 2. Requirements

### Functional Requirements

- **FR1:** O sistema deve aceitar URL de vídeo do YouTube como entrada
- **FR2:** O sistema deve aceitar upload ou link de arquivo de vídeo do Google Drive como entrada
- **FR3:** O sistema deve extrair o áudio do vídeo e transcrever com modelo de speech-to-text
- **FR4:** A transcrição deve preservar timestamps ao longo de todo o conteúdo
- **FR5:** O sistema deve segmentar a transcrição em tópicos identificados automaticamente
- **FR6:** O sistema deve gerar um índice de tópicos com links para os timestamps correspondentes
- **FR7:** O sistema deve identificar e destacar citações e trechos relevantes automaticamente
- **FR8:** O sistema deve gerar um documento final exportável (Markdown e/ou PDF)
- **FR9:** A interface web deve permitir acompanhar o progresso do processamento em tempo real
- **FR10:** O sistema deve suportar vídeos de até 4 horas sem falha ou timeout

### Non-Functional Requirements

- **NFR1:** O processamento de um vídeo de 4h deve concluir sem intervenção manual (tempo real depende do hardware — ver seção Technical Assumptions)
- **NFR2:** A precisão da transcrição deve ser ≥90% para áudio em português claro
- **NFR3:** A interface web deve funcionar em browsers modernos (Chrome, Firefox, Edge)
- **NFR4:** O sistema deve ser executável localmente via Docker Compose sem custos de infra recorrentes
- **NFR5:** Dados do usuário e transcrições não devem ser retidos em servidores externos além do necessário para processamento

---

## 3. User Interface Design Goals

### Overall UX Vision

Interface minimalista e focada em tarefa — o usuário cola uma URL (ou faz upload), clica em processar e aguarda. O resultado aparece como documento navegável diretamente na tela, sem fricção. Sem dashboards complexos, sem cadastro.

### Key Interaction Paradigms

- **Single-page flow:** Entrada → Processamento → Resultado, tudo em uma tela
- **Progress feedback:** Barra/status de progresso durante transcrição
- **Document viewer inline:** Resultado exibido diretamente na interface com navegação por tópicos
- **Copy/Export rápido:** Botões visíveis para copiar ou exportar (Markdown / PDF)

### Core Screens and Views

1. **Home / Input Screen** — Campo de URL (YouTube ou Google Drive) + botão "Processar"
2. **Processing Screen** — Status em tempo real (etapas: download → extração de áudio → transcrição → análise → geração de doc)
3. **Result Screen** — Documento completo com índice de tópicos clicável, transcrição com timestamps, destaques e citações em destaque visual
4. **Export Panel** — Opções de download: Markdown, PDF

### Accessibility

WCAG AA — contraste adequado, navegação por teclado

### Branding

Uso pessoal — design limpo, tipografia legível, suporte a dark mode simples

### Target Device and Platforms

Web Responsive — desktop-first, responsivo para tablet

---

## 4. Technical Assumptions

### Repository Structure

Monorepo — frontend + backend + worker no mesmo repositório

### Service Architecture

Monolith com workers assíncronos:

```
Frontend (React + Vite) → Backend API (Python/FastAPI) → Queue (Redis/Celery) → Worker (Whisper + LLM)
```

### Stack Técnica

| Camada        | Tecnologia                        | Justificativa                                      |
|---------------|-----------------------------------|----------------------------------------------------|
| Frontend      | React + Vite                      | Simples, rápido, amplo ecossistema                 |
| Backend       | Python + FastAPI                  | Ecossistema nativo para IA/ML, assíncrono          |
| Transcrição   | OpenAI Whisper (local)            | Gratuito, alta precisão em PT-BR, roda localmente  |
| Análise       | OpenAI GPT-4o ou Ollama (local)   | Segmentação de tópicos e extração de destaques     |
| Download YT   | yt-dlp                            | Padrão de mercado, robusto para lives longas       |
| Google Drive  | Google Drive API v3               | Download direto do arquivo                         |
| Queue/Jobs    | Celery + Redis                    | Processamento assíncrono de jobs longos            |
| Export        | Markdown + WeasyPrint (PDF)       | Geração nativa, PDF via lib Python                 |
| Deploy        | Docker Compose (local)            | Uso pessoal — roda na máquina do usuário           |

### Whisper Model Selection (Hardware-Dependent)

| Modelo     | RAM/VRAM Necessária | Precisão | Velocidade (CPU)       |
|------------|---------------------|----------|------------------------|
| `large-v3` | ~10 GB              | Máxima   | ~8-12x tempo real      |
| `medium`   | ~5 GB               | Alta     | ~4-6x tempo real       |
| `small`    | ~2 GB               | Boa      | ~2x tempo real         |

- **Recomendação MVP:** `medium` como default (melhor custo-benefício em CPU)
- Para 4h de áudio com modelo `medium` em CPU: estimativa de 16-24h de processamento
- **Com GPU (CUDA):** `large-v3` processa 4h em ~30-40min
- Modelo configurável via `WHISPER_MODEL` (default: `medium`)

> ⚠️ **Risco:** O NFR1 original (30min) é atingível apenas com GPU. Para CPU, o processamento ocorre em background (overnight). Recomenda-se validar hardware disponível antes de iniciar o desenvolvimento.

### Testing Requirements

Unit + Integration básico:
- Unit: parsers de transcrição, segmentação de tópicos
- Integration: pipeline completo (URL → documento)

### Additional Technical Assumptions

- Whisper roda localmente para preservar privacidade e evitar custos de API
- Vídeos privados do Google Drive requerem autenticação OAuth2
- Vídeos do YouTube privados ou com restrição de idade não são suportados no MVP
- Processamento em chunks de 10 minutos com overlap de 5s para evitar estouro de memória
- Resultados armazenados localmente em `outputs/` — sem banco de dados no MVP
- LLM para análise configurável: OpenAI GPT-4o (requer API key) ou Ollama local (gratuito, mais lento)

---

## 5. Epic List

| Epic   | Título                                    | Objetivo                                                    |
|--------|-------------------------------------------|-------------------------------------------------------------|
| Epic 1 | Foundation & Project Setup                | Infraestrutura base, Docker Compose, scaffolding completo   |
| Epic 2 | Video Ingestion Pipeline                  | Download YouTube/Drive, extração de áudio, chunking         |
| Epic 3 | Transcription Engine                      | Whisper por chunks, consolidação com timestamps             |
| Epic 4 | Analysis, Document Generation & Export    | LLM analysis, documento final, viewer, exportação           |

---

## 6. Epic Details

### Epic 1 — Foundation & Project Setup

**Goal:** Estabelecer toda a infraestrutura base do projeto em Docker Compose (FastAPI + React + Redis + Celery), com monorepo organizado, entregando uma interface web funcional onde o usuário já consegue visualizar o formulário de input e o backend responde com health-check — garantindo que o ambiente completo está operacional antes de qualquer feature real.

---

#### Story 1.1 — Monorepo Structure & Docker Compose Setup

> As a developer, I want a working monorepo with Docker Compose, so that all services start with a single command.

**Acceptance Criteria:**
1. Repositório criado com estrutura `frontend/`, `backend/`, `worker/`, `docker-compose.yml`
2. `docker-compose up` sobe todos os serviços (frontend, backend, redis, worker) sem erros
3. Cada serviço possui Dockerfile funcional com hot-reload em desenvolvimento
4. `README.md` documenta como iniciar o projeto localmente

---

#### Story 1.2 — FastAPI Backend Scaffold

> As a developer, I want a FastAPI backend running, so that I can add endpoints progressively.

**Acceptance Criteria:**
1. FastAPI rodando na porta 8000 com estrutura de pastas (`routers/`, `services/`, `models/`)
2. Endpoint `GET /health` retorna `{"status": "ok"}`
3. CORS configurado para aceitar requisições do frontend
4. Logging estruturado configurado (JSON logs)

---

#### Story 1.3 — Celery + Redis Async Queue

> As a developer, I want an async job queue, so that long-running tasks don't block the HTTP server.

**Acceptance Criteria:**
1. Celery worker conectado ao Redis e processando tarefas assíncronas
2. Endpoint `POST /jobs` cria um job e retorna `job_id` imediatamente
3. Endpoint `GET /jobs/{job_id}` retorna status (`pending`, `processing`, `completed`, `failed`)
4. Job de teste (sleep 5s) executado com sucesso via queue

---

#### Story 1.4 — React Frontend Scaffold + Input Form

> As a user, I want a web page where I can submit a video URL, so that I can start the transcription process.

**Acceptance Criteria:**
1. React + Vite rodando na porta 3000, servido via Docker
2. Página inicial exibe formulário com campo de URL e botão "Processar"
3. Formulário valida se o campo não está vazio antes de submeter
4. Submissão chama `POST /jobs` no backend e exibe o `job_id` retornado
5. Estado de loading exibido durante a chamada à API

---

#### Story 1.5 — Job Progress Polling UI

> As a user, I want to see the real-time status of my job, so that I know the processing is progressing.

**Acceptance Criteria:**
1. Após submissão, UI faz polling em `GET /jobs/{job_id}` a cada 3 segundos
2. Barra de progresso ou indicador de status exibido com a etapa atual
3. Mensagem de erro amigável exibida se o job falhar
4. Polling encerrado automaticamente quando status for `completed` ou `failed`

---

### Epic 2 — Video Ingestion Pipeline

**Goal:** Implementar a capacidade de receber uma URL do YouTube ou link do Google Drive, baixar o vídeo, extrair o áudio em formato otimizado para transcrição e armazená-lo localmente — com feedback visual de progresso em cada etapa e tratamento robusto de erros para os casos mais comuns.

---

#### Story 2.1 — YouTube Download via yt-dlp

> As a user, I want to submit a YouTube URL and have the audio downloaded automatically, so that I don't need to manually extract it.

**Acceptance Criteria:**
1. Backend aceita URL do YouTube via `POST /jobs` com campo `source_type: "youtube"`
2. yt-dlp instalado no worker e executa download do áudio (formato `.wav`, 16kHz mono)
3. Arquivo de áudio salvo em `outputs/{job_id}/audio.wav`
4. Status do job atualizado para `downloading` durante o processo
5. Erro tratado e registrado se URL for inválida, vídeo privado ou indisponível
6. Suporte a vídeos de até 4 horas sem timeout (timeout configurado para 30min)

---

#### Story 2.2 — Google Drive File Download

> As a user, I want to submit a Google Drive link and have the video downloaded automatically, so that I can use files I already have saved.

**Acceptance Criteria:**
1. Backend aceita link do Google Drive via `POST /jobs` com campo `source_type: "gdrive"`
2. Download via Google Drive API v3 com autenticação por Service Account ou OAuth2
3. Arquivo baixado e áudio extraído com `ffmpeg` para `.wav` 16kHz mono
4. Credenciais do Google Drive configuráveis via variável de ambiente (`GOOGLE_CREDENTIALS_PATH`)
5. Erro tratado se arquivo não encontrado, sem permissão ou link inválido
6. Arquivo de vídeo removido após extração do áudio (economizar espaço)

---

#### Story 2.3 — Audio Chunking for Long Videos

> As a developer, I want the audio split into chunks, so that Whisper can process long videos without memory overflow.

**Acceptance Criteria:**
1. Áudio dividido em chunks de 10 minutos com overlap de 5 segundos entre chunks
2. Chunks salvos em `outputs/{job_id}/chunks/chunk_{n}.wav`
3. Metadados de cada chunk registrados em `outputs/{job_id}/chunks_meta.json` (início, fim, índice)
4. Processo funciona corretamente para áudios de até 4 horas (≥24 chunks)
5. Status do job atualizado para `chunking` durante o processo

---

#### Story 2.4 — Ingestion Progress Feedback on UI

> As a user, I want to see detailed progress during video ingestion, so that I know exactly what is happening.

**Acceptance Criteria:**
1. UI exibe etapas distintas: `Baixando vídeo...`, `Extraindo áudio...`, `Dividindo em partes...`
2. Percentual de progresso exibido quando disponível (ex: download do yt-dlp)
3. Mensagens de erro específicas exibidas por tipo de falha (ex: "Vídeo privado — não foi possível baixar")
4. Botão "Cancelar" disponível durante o processamento, cancelando o job no backend

---

### Epic 3 — Transcription Engine

**Goal:** Integrar OpenAI Whisper para transcrever cada chunk de áudio preservando timestamps precisos, processar todos os chunks de forma assíncrona e sequencial, consolidar os resultados em uma transcrição completa e coesa — entregando ao usuário feedback em tempo real do progresso chunk a chunk durante todo o processo.

---

#### Story 3.1 — Whisper Integration & Single Chunk Transcription

> As a developer, I want Whisper transcribing a single audio chunk, so that I can validate accuracy and output format before scaling.

**Acceptance Criteria:**
1. OpenAI Whisper instalado no worker com modelo configurável via `WHISPER_MODEL` (default: `medium`)
2. Função `transcribe_chunk(chunk_path)` retorna lista de segmentos `[{start, end, text}]`
3. Idioma configurável via `WHISPER_LANGUAGE` (default: `pt`)
4. Transcrição de chunk de 10min concluída sem erros; tempo registrado no log para benchmarking
5. Output salvo em `outputs/{job_id}/transcripts/chunk_{n}.json`

---

#### Story 3.2 — Full Pipeline: All Chunks Transcribed Sequentially

> As a user, I want all chunks transcribed automatically in sequence, so that the entire video is covered.

**Acceptance Criteria:**
1. Worker processa todos os chunks sequencialmente após etapa de chunking
2. Status do job atualizado com progresso: `transcribing (chunk 3/24)`
3. Falha em chunk individual registrada sem interromper os demais (chunk marcado como `failed`, processamento continua)
4. Todos os arquivos `chunk_{n}.json` gerados ao final do processamento
5. Job marcado como `failed` somente se mais de 20% dos chunks falharem

---

#### Story 3.3 — Transcript Consolidation with Timestamps

> As a developer, I want all chunk transcripts merged into a single document, so that the full video has one continuous timeline.

**Acceptance Criteria:**
1. Função `consolidate_transcripts(job_id)` lê todos os `chunk_{n}.json` e consolida em ordem cronológica
2. Timestamps ajustados para refletir posição absoluta no vídeo (não relativa ao chunk)
3. Output consolidado salvo em `outputs/{job_id}/transcript_full.json` com formato `[{start, end, text}]`
4. Gaps entre chunks (overlap) resolvidos sem duplicação de texto
5. Transcrição consolidada de 4h contém timestamps precisos do início ao fim

---

#### Story 3.4 — Transcription Progress on UI

> As a user, I want to see chunk-by-chunk transcription progress, so that I know the process is running and can estimate remaining time.

**Acceptance Criteria:**
1. UI exibe progresso detalhado: `Transcrevendo... (parte 5 de 24 — 21% concluído)`
2. Tempo estimado restante calculado e exibido com base na velocidade média dos chunks anteriores
3. UI atualiza a cada polling (3s) sem flickering ou perda de estado
4. Ao completar todas as transcrições, status muda automaticamente para `Analisando conteúdo...`

---

### Epic 4 — Analysis, Document Generation & Export

**Goal:** Processar a transcrição consolidada com LLM para identificar tópicos, extrair destaques e citações relevantes, gerar documento final rico e navegável na interface web — com exportação em Markdown e PDF — completando o ciclo completo da aplicação.

---

#### Story 4.1 — Topic Segmentation via LLM

> As a user, I want the transcription automatically divided into topics, so that I can navigate the content without reading everything.

**Acceptance Criteria:**
1. Função `segment_topics(transcript_full)` envia transcrição ao LLM (GPT-4o ou Ollama) em batches
2. LLM retorna lista de tópicos `[{title, start_time, end_time, summary}]`
3. Mínimo de 5 tópicos identificados para vídeos de 4h (média esperada: 10-20 tópicos)
4. Timestamps de início/fim de cada tópico mapeados para a transcrição original
5. Output salvo em `outputs/{job_id}/topics.json`
6. LLM configurável via `LLM_PROVIDER` (`openai` ou `ollama`)

---

#### Story 4.2 — Highlights & Key Quotes Extraction

> As a user, I want key highlights and notable quotes identified automatically, so that I can quickly find the most important moments.

**Acceptance Criteria:**
1. Função `extract_highlights(transcript_full, topics)` identifica trechos de alto valor por tópico
2. Mínimo de 3 destaques por tópico identificado
3. Cada destaque contém `{text, timestamp, topic, type}` onde `type` é `quote` ou `highlight`
4. Critérios de seleção: definições importantes, afirmações fortes, momentos-chave da live
5. Output salvo em `outputs/{job_id}/highlights.json`

---

#### Story 4.3 — Structured Document Generation

> As a user, I want a complete structured document generated from the analysis, so that I have a single reference artifact.

**Acceptance Criteria:**
1. Função `generate_document(job_id)` combina transcrição + tópicos + destaques em documento Markdown
2. Documento contém: cabeçalho com metadados (título, duração, data), índice de tópicos com links âncora e timestamps, seção por tópico com resumo + transcrição do trecho + destaques/citações em `> blockquote`
3. Documento salvo em `outputs/{job_id}/document.md`
4. Documento de 4h de conteúdo gerado em menos de 2 minutos
5. Status do job atualizado para `completed` após geração

---

#### Story 4.4 — Document Viewer on UI

> As a user, I want to read the generated document directly in the browser, so that I don't need to download anything to consume the result.

**Acceptance Criteria:**
1. Ao completar o job, UI transiciona automaticamente para Result Screen
2. Documento Markdown renderizado com formatação visual (headings, blockquotes, timestamps)
3. Índice de tópicos fixo na sidebar com links âncora para cada seção
4. Timestamps clicáveis abrem YouTube no tempo correspondente (se fonte for YouTube)
5. Barra de busca permite pesquisar termos dentro do documento

---

#### Story 4.5 — Export to Markdown & PDF

> As a user, I want to download the document as Markdown or PDF, so that I can save and share the result.

**Acceptance Criteria:**
1. Botão "Exportar Markdown" faz download de `document.md` diretamente
2. Botão "Exportar PDF" gera PDF via WeasyPrint no backend e faz download
3. PDF preserva formatação: índice, headings, blockquotes de citações
4. Nome do arquivo exportado inclui título do vídeo e data: `{titulo}_{data}.md` / `.pdf`
5. Ambas as exportações disponíveis em menos de 10 segundos após solicitação

---

## 7. Checklist Results Report

| Categoria | Status | Issues Críticos |
|-----------|--------|-----------------|
| 1. Problem Definition & Context | ⚠️ PARTIAL (75%) | Corrigido: build vs buy adicionado |
| 2. MVP Scope Definition | ✅ PASS (85%) | Corrigido: Out of Scope + Future Enhancements adicionados |
| 3. User Experience Requirements | ⚠️ PARTIAL (70%) | Fluxo de erros parcialmente coberto |
| 4. Functional Requirements | ✅ PASS (85%) | — |
| 5. Non-Functional Requirements | ✅ PASS (80%) | Corrigido: RAM constraints do Whisper documentados |
| 6. Epic & Story Structure | ✅ PASS (92%) | — |
| 7. Technical Guidance | ✅ PASS (80%) | — |
| 8. Cross-Functional Requirements | ⚠️ PARTIAL (60%) | Data entities e integration testing não formalizados |
| 9. Clarity & Communication | ✅ PASS (75%) | — |

**Completude geral:** ~80% | **Escopo MVP:** Just Right | **Pronto para arquitetura:** ✅ Ready

---

## 8. Next Steps

### UX Expert Prompt

> Revisar o `docs/prd.md` do **Video Transcription & Analysis App** e criar a especificação de UI/UX. Foco em: single-page flow (Input → Processing → Result), sidebar de navegação de tópicos, progress screen com etapas detalhadas, e document viewer com timestamps clicáveis. Stack: React + Vite, desktop-first, WCAG AA.

### Architect Prompt

> Revisar o `docs/prd.md` do **Video Transcription & Analysis App** e criar a arquitetura técnica. Stack definida: Python/FastAPI + React/Vite + Celery/Redis + Whisper (local) + GPT-4o ou Ollama + yt-dlp + Google Drive API + Docker Compose. Atenção especial a: (1) constraints de RAM do modelo Whisper vs hardware disponível, (2) estratégia de chunking e consolidação de timestamps, (3) pipeline assíncrono para jobs de ~4h, (4) complexidade de auth OAuth2 Google Drive vs alternativas mais simples.
