# Backlog de workflows

Temas para virar workflow (passo a passo). Marque `[x]` quando estiver pronto em `workflows/`.
⭐ = prioridade (tem um fluxo claro de etapas).

## Primeira leva (pronta)
- [x] ⭐ RAG: busca + geração (embeddings, banco vetorial)
- [x] ⭐ Agentes com ferramentas (ReAct, tool use / function calling)
- [x] ⭐ RLHF / DPO (pré-treino → SFT → preferências)
- [x] ⭐ Fine-tuning com LoRA
- [x] ⭐ Stable Diffusion completo (VAE + texto + U-Net)

## Fundamentos de machine learning
- [x] ⭐ Pipeline de ML: dados → treino → validação → deploy
- [x] ⭐ Overfitting, regularização e validação cruzada
- [x] Regressão linear e logística
- [x] Árvores de decisão, Random Forest e gradient boosting (XGBoost)
- [x] k-means, k-NN, SVM e PCA
- [x] Viés e variância

## Como as redes aprendem
- [ ] ⭐ Gradiente descendente e otimizadores (SGD, Adam)
- [ ] Funções de ativação
- [ ] Normalização (batch e layer norm), dropout
- [ ] ⭐ Transfer learning e fine-tuning
- [ ] ⭐ Quantização
- [ ] Destilação de conhecimento e pruning
- [ ] Treino distribuído em várias GPUs (data/model parallelism)

## Arquiteturas de redes neurais
- [ ] Perceptron e MLP
- [ ] ⭐ ResNet (conexões residuais)
- [ ] ⭐ U-Net
- [ ] ⭐ Vision Transformer (ViT)
- [ ] BERT contra GPT (encoder, decoder, encoder-decoder)
- [ ] ⭐ Mixture of Experts (MoE)
- [ ] Mamba / modelos de espaço de estados
- [ ] Redes em grafos (GNN)
- [ ] Flow matching e consistency models

## LLMs por dentro
- [ ] ⭐ KV cache e FlashAttention
- [ ] Multi-head attention, RoPE e janela de contexto
- [ ] Temperatura, top-k e top-p
- [ ] Chain-of-thought e modelos de raciocínio
- [ ] Alucinação e como mitigar
- [ ] Avaliação: benchmarks e LLM-as-judge

## Aplicações com LLMs
- [ ] ⭐ MCP (Model Context Protocol)
- [ ] Memória de agentes e multiagentes
- [ ] Prompt engineering e structured output
- [ ] Guardrails e segurança (prompt injection, jailbreak)

## Aprendizado por reforço
- [ ] ⭐ Agente, ambiente, recompensa
- [ ] Q-learning e DQN
- [ ] Policy gradient e PPO
- [ ] AlphaGo / MCTS

## Visão, imagem e vídeo
- [ ] ControlNet e LoRA de imagem
- [ ] ⭐ CLIP e modelos multimodais
- [ ] Detecção de objetos (YOLO) e segmentação
- [ ] OCR e NeRF / Gaussian splatting
- [ ] Geração de vídeo

## Áudio e fala
- [ ] Reconhecimento de fala (Whisper)
- [ ] Síntese de voz (TTS) e clonagem
- [ ] Geração de música
- [ ] Narração dos workflows com ElevenLabs (áudio por passo, gerado antes; Live espera o áudio terminar)

## Engenharia e ferramentas
- [ ] ⭐ MLOps: treino → deploy → monitoramento (drift)
- [ ] ⭐ Servir modelos (vLLM, batching, GPU / CUDA / TPU)
- [ ] PyTorch, TensorFlow e JAX
- [ ] Hugging Face, Ollama e llama.cpp, LangChain e LlamaIndex
- [ ] ONNX, Docker e Kubernetes para IA
- [x] Experimentos: MLflow
- [ ] Experimentos: Weights & Biases

## Dados, ética e segurança
- [ ] Coleta, limpeza e rotulagem; dados sintéticos
- [ ] Viés e fairness
- [ ] Explicabilidade (SHAP, LIME, Grad-CAM)
- [ ] Exemplos adversariais e deepfakes
- [ ] Privacidade (federated learning, differential privacy)
- [ ] Regulação (AI Act) e direitos autorais
