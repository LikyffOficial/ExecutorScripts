cat > README.md << 'EOF'
# 🤖 Executor de Scripts

Aplicativo Android para execução de scripts Python com automação.

## 📱 Instalação

1. Vá em [Actions](../../actions)
2. Clique no último workflow bem-sucedido (✅)
3. Baixe o artifact `executorscripts-apk`
4. Instale o APK no seu Android

## 🚀 Como Usar

1. Abra o app
2. Cole um script Python
3. Clique em **▶️ EXECUTAR**

### Exemplo de Script

```python
# Contador simples
for i in range(10):
    output(f"Contagem: {i}")
    sleep(1)
