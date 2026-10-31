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
- [x] ⭐ Gradiente descendente e otimizadores (SGD, Adam)
- [ ] Funções de ativação
- [ ] Normalização (batch e layer norm), dropout
- [x] ⭐ Transfer learning e fine-tuning
- [x] ⭐ Quantização
- [ ] Destilação de conhecimento e pruning
- [ ] Treino distribuído em várias GPUs (data/model parallelism)

## Arquiteturas de redes neurais
- [ ] Perceptron e MLP
- [x] ⭐ ResNet (conexões residuais)
- [x] ⭐ U-Net
- [x] ⭐ Vision Transformer (ViT)
- [ ] BERT contra GPT (encoder, decoder, encoder-decoder)
- [x] ⭐ Mixture of Experts (MoE)
- [ ] Mamba / modelos de espaço de estados
- [ ] Redes em grafos (GNN)
- [ ] Flow matching e consistency models

## LLMs por dentro
- [x] ⭐ KV cache e FlashAttention
- [x] Multi-head attention, RoPE e janela de contexto
- [x] Temperatura, top-k e top-p
- [x] Chain-of-thought e modelos de raciocínio
- [x] Alucinação e como mitigar
- [x] Avaliação: benchmarks e LLM-as-judge

## Aplicações com LLMs
- [x] ⭐ MCP (Model Context Protocol)
- [ ] Memória de agentes e multiagentes
- [ ] Prompt engineering e structured output
- [ ] Guardrails e segurança (prompt injection, jailbreak)

## Aprendizado por reforço
- [x] ⭐ Agente, ambiente, recompensa
- [x] Q-learning e DQN
- [x] Policy gradient e PPO
- [x] AlphaGo / MCTS

## Visão, imagem e vídeo
- [ ] ControlNet e LoRA de imagem
- [x] ⭐ CLIP e modelos multimodais
- [ ] Detecção de objetos (YOLO) e segmentação
- [ ] OCR e NeRF / Gaussian splatting
- [ ] Geração de vídeo

## Áudio e fala
- [ ] Reconhecimento de fala (Whisper)
- [ ] Síntese de voz (TTS) e clonagem
- [ ] Geração de música
- [ ] Narração dos workflows com ElevenLabs (áudio por passo, gerado antes; Live espera o áudio terminar)

## Engenharia e ferramentas
- [x] ⭐ MLOps: treino → deploy → monitoramento (drift)
- [x] ⭐ Servir modelos (vLLM, batching, GPU / CUDA / TPU)
- [ ] PyTorch, TensorFlow e JAX
- [ ] Hugging Face, Ollama e llama.cpp, LangChain e LlamaIndex
- [ ] ONNX, Docker e Kubernetes para IA
- [x] Experimentos: MLflow
- [ ] Experimentos: Weights & Biases

## IA simbólica
- [x] ⭐ Sistemas especialistas e regras (motor de inferência, base de conhecimento)
- [ ] Lógica, busca e planejamento (A*, resolução de problemas)
- [ ] IA neuro-simbólica (redes neurais + regras)

## Dados, ética e segurança
- [ ] Coleta, limpeza e rotulagem; dados sintéticos
- [ ] Viés e fairness
- [ ] Explicabilidade (SHAP, LIME, Grad-CAM)
- [ ] Exemplos adversariais e deepfakes
- [ ] Privacidade (federated learning, differential privacy)
- [ ] Regulação (AI Act) e direitos autorais
