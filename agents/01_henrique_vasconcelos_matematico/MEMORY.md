# 💾 MEMORY.md — Memória Persistente (Henrique Vasconcelos - Matemático)

## 📐 1. Biblioteca de Modelos Matemáticos Padrão da Equipe
1. **Difusão e Adoção de Produtos (Modelo de Bass Discreto/Contínuo):**
   $$\frac{dN(t)}{dt} = \left(p + q \frac{N(t)}{M}\right)(M - N(t))$$
   Onde $M$ é o potencial máximo de mercado, $p$ o coeficiente de inovação (aquisição direta) e $q$ o coeficiente de imitação (efeito de rede / boca-a-boca).
2. **Demanda com Elasticidade-Preço Constant/Log-Linear ou Logística:**
   $$D(P) = D_0 \cdot \exp(-\epsilon \cdot (P - P_0) / P_0)$$
3. **Otimização de Margem de Contribuição Esperada:**
   $$\Pi(P) = (P - c_v) \cdot D(P) - C_{fixo}$$
   Com preço ótimo estacionário satisfazendo $\frac{\partial \Pi}{\partial P} = 0 \implies P^* = c_v + \frac{P_0}{\epsilon}$.

## 📜 2. Log de Entregas e Handoffs
- **[2026-11-01]:** Estrutura matemática inicializada e integrada ao `core/argon_engine.py`.
