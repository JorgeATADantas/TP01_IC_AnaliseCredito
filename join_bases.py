@pip install modin
import modin.pandas as pd


# Caminhos para os arquivos (você pode passar como argumentos ou alterar diretamente aqui)
arquivo1 = "E:/Documentos/CEFET/OneDrive/Documentos/2ECOM067_INTELIGENCIA-COMPUTACIONAL-I_T01/TP1/bases/application_train.csv"
arquivo2 = "E:/Documentos/CEFET/OneDrive/Documentos/2ECOM067_INTELIGENCIA-COMPUTACIONAL-I_T01/TP1/bases/bureau.csv"
arquivo3 = "E:/Documentos/CEFET/OneDrive/Documentos/2ECOM067_INTELIGENCIA-COMPUTACIONAL-I_T01/TP1/bases/bureau_balance.csv"

# Lê as três bases
df1 = df.read_csv(arquivo1)
df2 = df.read_csv(arquivo2)
df3 = df.read_csv(arquivo3)

# Exemplo: fazendo joins
# Ajuste os nomes das colunas para corresponder às chaves de junção reais
df_merged = df1.merge(df2, on="SK_ID_CURR", how="left")  # join entre base1 e base2
df_merged = df_merged.merge(df3, on="SK_ID_BUREAU", how="left")  # join com base3

# Salva o resultado
df_merged.to_csv("base_final.csv", index=False)

print("Join realizado com sucesso! Resultado salvo em base_final.csv")