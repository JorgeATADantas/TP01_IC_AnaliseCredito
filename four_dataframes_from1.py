import pandas as pd
import os, re
import numpy as np
import time
from sklearn.preprocessing import LabelEncoder
from sklearnex import patch_sklearn

patch_sklearn()

le = LabelEncoder()
CSV_PATH = (
    "/home/gi/Desktop/Semestre8/Inteligencia_Computacional/TP1_csvs"  # Path Giovanni
)

df_auxiliar_bureau = pd.read_csv(f"{CSV_PATH}/bureau.csv")
df_auxiliar_bureau_balance = pd.read_csv(f"{CSV_PATH}/bureau_balance.csv")
df_auxiliar_previous_application = pd.read_csv(f"{CSV_PATH}/previous_application.csv")
df_auxiliar_POS_CASH_balance = pd.read_csv(f"{CSV_PATH}/POS_CASH_balance.csv")
df_auxiliar_installments_payments = pd.read_csv(f"{CSV_PATH}/installments_payments.csv")
df_auxiliar_credit_card_balances = pd.read_csv(f"{CSV_PATH}/credit_card_balance.csv")

#df_train = pd.read_csv(f"{CSV_PATH}/application_train.csv")


# Renomeando colunas evitando duplicatas
def renomear_seguro(cols):
    novas = []
    vistos = set()
    for col in cols:
        base = re.sub(r"[^\w]", "", col)
        nome = base
        i = 1
        while nome in vistos:
            nome = f"{base}_{i}"
            i += 1
        vistos.add(nome)
        novas.append(nome)
    return novas


def four_dataframes_from_one(
    df_main, save: bool = False, save_file_name="default", sample=-1
):
    df_01 = df_main.copy()
    # Realização do left join de df_train com df_auxiliar_bureau
    # DF da esquerda = df_train
    # DF da direita  = df_auxiliar_bureau
    df_01 = df_01.join(df_auxiliar_bureau, on="SK_ID_CURR", lsuffix="-", how="left")
    df_01 = df_01.drop(columns={"SK_ID_CURR-"})  # Excluir coluna duplicada

    # Realização do left join de df_01 com df_auxiliar_bureau_balance
    # DF da esquerda = df_01
    # DF da direita  = df_auxiliar_bureau_balance
    df_01 = df_01.join(
        df_auxiliar_bureau_balance, on="SK_ID_BUREAU", lsuffix="-", how="left"
    )
    df_01 = df_01.drop(columns={"SK_ID_BUREAU-"})  # Excluir coluna duplicada

    # Limpa caracteres especiais das colunas
    df_01.columns = renomear_seguro(df_01.columns)

    # Label encoder nas colunas categóricas

    colunas_categoricas = df_01.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
    for coluna in colunas_categoricas:
        df_01[coluna] = le.fit_transform(df_01[coluna].astype(str))
    if sample > 0:
        df_01 = df_01.sample(frac=sample, random_state=42)

    if save:
        df_01.to_csv(
            f"{CSV_PATH}/{save_file_name}1.csv", index=False
        )  # Salvar df_01 em CSV
        print("df_01 criado e salvo com sucesso.")

    df_02 = df_main.copy()
    # Realização do left join de df_train com df_auxiliar_previous_application
    # DF da esquerda = df_train
    # DF da direita  = df_auxiliar_previous_application
    df_02 = df_02.join(
        df_auxiliar_previous_application, on="SK_ID_CURR", lsuffix="-", how="left"
    )
    df_02 = df_02.drop(columns={"SK_ID_CURR-"})  # Excluir coluna duplicada

    # Realização do left join de df_02 com df_auxiliar_POS_CASH_balance
    # DF da esquerda = df_02
    # DF da direita  = df_auxiliar_POS_CASH_balance
    df_02 = df_02.join(
        df_auxiliar_POS_CASH_balance, on="SK_ID_PREV", lsuffix="-", how="left"
    )
    df_02 = df_02.drop(columns={"SK_ID_PREV-"})  # Excluir coluna duplicada

    # Limpa caracteres especiais das colunas
    df_02.columns = renomear_seguro(df_02.columns)
    colunas_categoricas = df_02.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
    for coluna in colunas_categoricas:
        try:
            df_02[coluna] = le.fit_transform(df_02[coluna].astype(str))
        except ValueError:
            print(f"Erro ao converter coluna {coluna} para string. Verifique os dados.")
            raise ValueError
    if sample > 0:
        df_02 = df_02.sample(frac=sample, random_state=42)
    if save:
        df_02.to_csv(
            f"{CSV_PATH}/{save_file_name}2.csv", index=False
        )  # Salvar df_02 em CSV
        print("df_02 criado e salvo com sucesso.")

    df_03 = df_main.copy()
    df_03 = df_03.join(
        df_auxiliar_previous_application, on="SK_ID_CURR", lsuffix="-", how="left"
    )
    df_03 = df_03.drop(columns={"SK_ID_CURR-"})  # Excluir coluna duplicada

    # Realização do left join de df_03 com df_auxiliar_installments_payments
    # DF da esquerda = df_03
    # DF da direita  = df_auxiliar_installments_payments
    df_03 = df_03.join(
        df_auxiliar_installments_payments, on="SK_ID_PREV", lsuffix="-", how="left"
    )
    df_03 = df_03.drop(columns={"SK_ID_PREV-"})  # Excluir coluna duplicada

    # Limpa caracteres especiais das colunas
    df_03.columns = renomear_seguro(df_03.columns)
    colunas_categoricas = df_03.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
    for coluna in colunas_categoricas:
        df_03[coluna] = le.fit_transform(df_03[coluna].astype(str))
    if sample > 0:
        df_03 = df_03.sample(frac=sample, random_state=42)

    if save:
        df_03.to_csv(
            f"{CSV_PATH}/{save_file_name}3.csv", index=False
        )  # Salvar df_03 em CSV
        print("df_03 criado e salvo com sucesso.")

    df_04 = df_main.copy()
    df_04 = df_04.join(
        df_auxiliar_previous_application, on="SK_ID_CURR", lsuffix="-", how="left"
    )
    df_04 = df_04.drop(columns={"SK_ID_CURR-"})  # Excluir coluna duplicada

    # Realização do left join de df_03 com df_auxiliar_credit_card_balances
    # DF da esquerda = df_04
    # DF da direita  = df_auxiliar_credit_card_balances
    df_04 = df_04.join(
        df_auxiliar_credit_card_balances, on="SK_ID_PREV", lsuffix="-", how="left"
    )
    df_04 = df_04.drop(columns={"SK_ID_PREV-"})  # Excluir coluna duplicada

    # Limpa caracteres especiais das colunas
    df_04.columns = renomear_seguro(df_04.columns)

    colunas_categoricas = df_04.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
    for coluna in colunas_categoricas:
        df_04[coluna] = le.fit_transform(df_04[coluna].astype(str))
    if sample > 0:
        df_04 = df_04.sample(frac=sample, random_state=42)

    if save:
        df_04.to_csv(
            f"{CSV_PATH}/{save_file_name}4.csv", index=False
        )  # Salvar df_04 em CSV
        print("df_04 criado e salvo com sucesso.")

    # Tamanhos dos Data Frames criados
    print(
        f"df_test shape {df_main.shape}, df_01 shape {df_01.shape}, df_02 shape {df_02.shape}, df_03 shape {df_03.shape}, df_04 shape {df_04.shape}"
    )
    return df_01, df_02, df_03, df_04


# four_dataframes_from_one(df_train, save=True, save_file_name="/apocalipse/df_01_train")
