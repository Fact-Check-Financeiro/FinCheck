from pathlib import Path

import pandas as pd


# ============================================================
# 1. CAMINHOS DO DATASET
# ============================================================

BASE_DIR = (
    Path(__file__).resolve().parent.parent
    / "dataset"
    / "noticias"
    / "full_texts"
)

true_path = BASE_DIR / "true"
fake_path = BASE_DIR / "fake"

true_meta_path = BASE_DIR / "true-meta-information"
fake_meta_path = BASE_DIR / "fake-meta-information"


# print("TRUE:", true_path)
# print("FAKE:", fake_path)
# print("TRUE META:", true_meta_path)
# print("FAKE META:", fake_meta_path)


# ============================================================
# 2. CAMPOS DOS METADADOS
# ============================================================

metadata_columns = [
    "author",
    "link",
    "category",
    "date_of_publication",
    "number_of_tokens",
    "number_of_words_without_punctuation",
    "number_of_types",
    "number_of_links",
    "number_of_uppercase_words",
    "number_of_verbs",
    "number_of_subjunctive_imperative_verbs",
    "number_of_nouns",
    "number_of_adjectives",
    "number_of_adverbs",
    "number_of_modal_verbs",
    "number_of_singular_first_second_person_pronouns",
    "number_of_plural_first_person_pronouns",
    "number_of_pronouns",
    "pausality",
    "number_of_characters",
    "average_sentence_length",
    "average_word_length",
    "percentage_of_news_with_spelling_errors",
    "emotiveness",
    "diversity"
]


# ============================================================
# 3. CONVERTER VALORES DOS METADADOS
# ============================================================

def convert_value(value):
    value = value.strip()

    if value == "None":
        return None

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value


# ============================================================
# 4. LER UMA NOTÍCIA
# ============================================================

def ler_noticia(news_file, label, meta_path):

    # Pega o número do arquivo
    # Exemplo: 1.txt -> 1
    news_id = int(news_file.stem)

    # --------------------------------------------------------
    # Lê o texto da notícia
    # --------------------------------------------------------

    with open(news_file, "r", encoding="utf-8") as file:
        news = file.read()

    # --------------------------------------------------------
    # Encontra o arquivo de metadata correspondente
    # Exemplo:
    # 1.txt -> 1-meta.txt
    # --------------------------------------------------------

    meta_file = meta_path / f"{news_id}-meta.txt"

    with open(meta_file, "r", encoding="utf-8") as file:
        metadata = file.read()

    # --------------------------------------------------------
    # Separa as 25 linhas do metadata
    # --------------------------------------------------------

    metadata_lines = metadata.splitlines()

    # --------------------------------------------------------
    # Cria o dicionário
    # --------------------------------------------------------

    metadata_dict = dict(
        zip(metadata_columns, metadata_lines)
    )

    # --------------------------------------------------------
    # Converte os valores para os tipos corretos
    # --------------------------------------------------------

    for column in metadata_dict:
        metadata_dict[column] = convert_value(
            metadata_dict[column]
        )

    # --------------------------------------------------------
    # Adiciona informações que não estão no metadata
    # --------------------------------------------------------

    metadata_dict["id"] = news_id
    metadata_dict["label"] = label
    metadata_dict["news"] = news

    return metadata_dict


# ============================================================
# 5. CARREGAR TODAS AS NOTÍCIAS DE UMA PASTA
# ============================================================

def carregar_noticias(news_path, label, meta_path):

    noticias = []

    for news_file in news_path.glob("*.txt"):

        noticia = ler_noticia(
            news_file,
            label,
            meta_path
        )

        noticias.append(noticia)

    return noticias


# ============================================================
# 6. TESTE
# ============================================================

true_news = carregar_noticias(
    true_path,
    "true",
    true_meta_path
)

# print("Quantidade de notícias verdadeiras:", len(true_news))


# Mostra a primeira notícia
# print(true_news[0])


# Mostra algumas informações
# print("ID:", true_news[0]["id"])
# print("Label:", true_news[0]["label"])
# print("Autor:", true_news[0]["author"])

# print("Notícia:")
# print(true_news[0]["news"][:200])

fake_news = carregar_noticias(
    fake_path,
    "fake",
    fake_meta_path
)

# print("Quantidade de notícias falsas:", len(fake_news))

todas_noticias = true_news + fake_news
# print("Total de notícias:", len(todas_noticias))

# Mostra a primeira e a última notícia (true e false)
# print(todas_noticias[0]["label"])
# print(todas_noticias[-1]["label"])

df = pd.DataFrame(todas_noticias)

# print(df.shape)
# print(df.head())

# print(df.columns.tolist())
# print(df["label"].value_counts())
# print(df["category"].value_counts())

# print(df.isnull().sum())

palavras_chave = [
    "mercado financeiro",
    "bolsa de valores",
    "ações",
    "investimento",
    "economia",
    "dólar",
    "inflação",
    "juros",
    "banco central",
    "bovespa",
    "ibovespa",
    "renda fixa",
    "pib",
    "taxa selic",
    "câmbio",
    "recessão",
    "crescimento econômico",
    "empregos",
    "desemprego",
    "crise econômica",
    "mercado de ações",
    "investidores"
]

def encontrar_palavras_financeiras(texto):
    if not isinstance(texto, str):
        return []

    texto_lower = texto.lower()

    encontradas = []

    for palavra in palavras_chave:
        if palavra in texto_lower:
            encontradas.append(palavra)

    return encontradas


df["palavras_financeiras"] = df["news"].apply(
    encontrar_palavras_financeiras
)

df_financeiro = df[
    df["palavras_financeiras"].apply(len) > 0
].copy()

print("Total original:", len(df))
print("Total financeiro:", len(df_financeiro))

print("\nDistribuição por label:")
print(df_financeiro["label"].value_counts())

print("\nDistribuição por categoria:")
print(df_financeiro["category"].value_counts())


for _, row in df_financeiro.head(5).iterrows():

    print("-" * 80)
    print("Categoria:", row["category"])
    print("Label:", row["label"])
    print("Palavras encontradas:", row["palavras_financeiras"])
    print("Notícia:", row["news"][:300])