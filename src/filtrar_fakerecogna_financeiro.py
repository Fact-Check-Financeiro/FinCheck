
"""
Filtra notícias do dataset FakeRecogna2 por palavras-chave
relacionadas a mercado financeiro
Salva em CSV e em pastas fake/true para treinamento
"""
import os
import pandas as pd
from pathlib import Path

# PALAVRAS-CHAVE
palavras_chave = [
    'mercado financeiro', 'bolsa de valores', 'ações', 'investimento',
    'economia', 'dólar', 'real', 'inflação', 'juros', 'banco central',
    'bovespa', 'ibovespa', 'renda fixa', 'pib', 'taxa selic',
    'câmbio', 'recessão', 'crescimento econômico', 'empregos',
    'desemprego', 'crise econômica', 'mercado de ações', 'investidores'
]

def contem_palavra_financeira(texto):
    """Verifica se o texto contém alguma palavra-chave"""
    if not isinstance(texto, str):
        return False
    texto_lower = texto.lower()
    return any(palavra in texto_lower for palavra in palavras_chave)

def main():
    # 1. Carregar dataset
    print(" Baixando dataset do Hugging Face ")
    df = pd.read_csv("hf://datasets/recogna-nlp/fakerecogna2-abstrativa/fakerecogna_abstrativo.csv")
    
    print(f" Dataset carregado: {len(df)} registros.")
    print(f" Colunas disponíveis: {df.columns.tolist()}")

    # 2. Definir colunas corretas
    coluna_texto = 'Noticia'    # corpo da notícia
    coluna_titulo = 'Titulo'    # título
    coluna_label = 'Label'      # rótulo (0=fake, 1=true)

    # 3. Aplicar filtro
    print("🔍 Filtrando notícias sobre mercado financeiro...")
    df['contem_financeiro'] = df[coluna_texto].apply(contem_palavra_financeira)
    df_filtrado = df[df['contem_financeiro']].copy()
    df_filtrado.drop(columns=['contem_financeiro'], inplace=True)

    print(f" Encontradas {len(df_filtrado)} notícias financeiras.")

    # 4. Salvar CSV completo
    csv_saida = "fakerecogna_financeiro.csv"
    df_filtrado.to_csv(csv_saida, index=False, encoding='utf-8-sig')
    print(f" CSV salvo: {csv_saida}")

    # 5. Salvar em pastas fake/true
    pasta_base = "./noticias_fakerecogna_financeiro"
    Path(pasta_base).mkdir(exist_ok=True)
    
    for idx, row in df_filtrado.iterrows():
        # Determina o rótulo
        label_val = row[coluna_label]
        if label_val == 1:
            label = "true"
        else:
            label = "fake"   # se for 0 ou qualquer outro valor, vai para fake
        
        pasta_destino = os.path.join(pasta_base, label)
        Path(pasta_destino).mkdir(exist_ok=True, parents=True)
        
        nome_arquivo = f"noticia_{idx}.txt"
        caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
        
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            titulo = row.get(coluna_titulo, '')
            texto = row.get(coluna_texto, '')
            f.write(f"{titulo}\n\n{texto}")
    
    print(f" Pastas criadas: {pasta_base}/fake/ e {pasta_base}/true/")
    print(f"   Total de arquivos salvos: {len(df_filtrado)}")

    # 6. Estatísticas
    qtd_fake = len(df_filtrado[df_filtrado[coluna_label] == 0])
    qtd_true = len(df_filtrado[df_filtrado[coluna_label] == 1])
    print("\n Resumo:")
    print(f"   - Fake: {qtd_fake}")
    print(f"   - True: {qtd_true}")
    print(f"   - Total: {len(df_filtrado)}")

if __name__ == "__main__":
    main()
