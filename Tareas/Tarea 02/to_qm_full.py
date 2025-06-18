from typing import Any, Dict, List
import sys

import pandas as pd

#########################################################################################
#### READ CSV
#########################################################################################

BASE_PATH = "participacion/"
PARLAMENTARIOS_INFO_GENERAL_PATH = BASE_PATH + "parlamentarios_info_general.csv"
PARTICIPACION_DESCRIPCION_2023_1_PATH = BASE_PATH + "participacion_descripcion_2023_1.csv"
PARTICIPACION_DESCRIPCION_2023_2_PATH = BASE_PATH + "participacion_descripcion_2023_2.csv"
PARTICIPACION_DESCRIPCION_2024_PATH = BASE_PATH + "participacion_descripcion_2024.csv"
EMBEDDINGS_PATH = BASE_PATH + "embeddings_with_id.csv"

df_general = pd.read_csv(PARLAMENTARIOS_INFO_GENERAL_PATH)
df_participacion_2023_1 = pd.read_csv(PARTICIPACION_DESCRIPCION_2023_1_PATH)
df_participacion_2023_2 = pd.read_csv(PARTICIPACION_DESCRIPCION_2023_2_PATH)
df_participacion_2024 = pd.read_csv(PARTICIPACION_DESCRIPCION_2024_PATH)

#########################################################################################
#### UTILS
#########################################################################################


def value_or_none(value: pd.Series) -> Any:
    if pd.notna(value):
        return value
    return None


def escape_str(s: str) -> str:
    return s.replace("\n", "\\n").replace('"', '\\"')


#########################################################################################
#### PARLAMENTARIOS
#########################################################################################


def process_parlamentarios():
    partido2id: Dict[str, int] = {}
    unidad2id: Dict[str, int] = {}

    # process parlamentarios csv
    for _, row in df_general.iterrows():
        parlamentario_id = row["PARLAMENTARIO_ID"]
        nombre_completo = row["NOMBRE_COMPLETO"]
        vigente = "true" if row["VIGENTE"] == 1 else "false"
        fecha_nacimiento = value_or_none(row["FECHA_NACIMIENTO"])
        camara_actual = value_or_none(row["CAMARA_ACTUAL"])
        camara = value_or_none(row["CAMARA"])
        inicio = value_or_none(row["INICIO"])
        final = value_or_none(row["FINAL"])
        partido_politico = value_or_none(row["PARTIDO_POLITICO"])
        unidad = value_or_none(row["UNIDAD_QUE_REPRESENTA"])

        line = f"parl_{parlamentario_id} :Parlamentario"
        line += f" parl_id:{parlamentario_id}"
        line += f' nombre_completo:"{nombre_completo}"'
        line += f" vigente:{vigente}"
        if fecha_nacimiento:
            line += f' fecha_nacimiento:date("{fecha_nacimiento}")'
        if camara_actual:
            line += f' camara_actual:"{camara_actual}"'
        if camara:
            line += f' camara:"{camara}"'
        if inicio:
            line += f" inicio:{int(inicio)}"
        if final:
            line += f" inicio:{int(final)}"

        print(line)

        if partido_politico:
            if not partido_politico in partido2id:
                partido2id[partido_politico] = len(partido2id)
            part_id = partido2id[partido_politico]
            print(f"parl_{parlamentario_id}->partid_{part_id} :enPartido")

        if unidad:
            if not unidad in unidad2id:
                unidad2id[unidad] = len(unidad2id)
            unidad_id = unidad2id[unidad]
            print(f"parl_{parlamentario_id}->uni_{unidad_id} :enUnidad")

    # write partido
    for partido_nombre, partido_id in partido2id.items():
        print(f'partid_{partido_id} :Partido nombre:"{partido_nombre}"')

    # write unidad
    for unidad_nombre, unidad_id in unidad2id.items():
        print(f'uni_{unidad_id} :Unidad nombre:"{unidad_nombre}"')


#########################################################################################
#### PARTICIPACIONES
#########################################################################################


def process_participaciones():
    for df_participacion in [df_participacion_2023_1, df_participacion_2023_2, df_participacion_2024]:
        # process participacion csv
        for idx, row in df_participacion.iterrows():
            participacion_id = row["ID_PARTICIPACION"]
            parlamentario_id = value_or_none(row["PARLAMENTARIO_ID"])
            fecha = value_or_none(row["FECHA"])
            legislatura = value_or_none(row["LEGISLATURA"])
            sesion = value_or_none(row["SESION"])
            tipo_sesion = value_or_none(row["TIPO_SESION"])
            tipo_participacion = value_or_none(row["TIPO_PARTICIPACION"])
            camara = value_or_none(row["CAMARA"])
            parlamentarios = value_or_none(row["PARLAMENTARIOS"])
            texto_principal = value_or_none(row["TEXTO_PRINCIPAL"])
            texto_antecedente = value_or_none(row["TEXTO_ANTECEDENTE"])
            descripcion_debate = value_or_none(row["DESCRIPCION_DEBATE"])
            boletin_id = value_or_none(row["BOLETIN_ID"])

            line = f"partic_{participacion_id} :Participacion"
            if fecha:
                line += f' fecha:date("{fecha}")'
            if legislatura:
                line += f" legislatura:{legislatura}"
            if sesion:
                line += f" sesion:{int(sesion)}"
            if tipo_sesion:
                line += f' tipo_sesion:"{tipo_sesion}"'
            if tipo_participacion:
                line += f' tipo_participacion:"{tipo_participacion}"'
            if camara:
                line += f' camara:"{camara}"'
            if parlamentarios:
                line += f' parlamentarios:"{parlamentarios}"'
            if texto_principal:
                line += f' texto_principal:"{escape_str(texto_principal)}"'
            if texto_antecedente:
                line += f' texto_antecedente:"{escape_str(texto_antecedente)}"'
            if descripcion_debate:
                line += f' descripcion_debate:"{escape_str(descripcion_debate)}"'
            if boletin_id:
                line += f" boletin_id:{int(boletin_id)}"

            print(line)
            print(f"parl_{parlamentario_id}->partic_{participacion_id} :enParticipacion")


#########################################################################################
#### EMBEDDINGS
#########################################################################################
def process_embeddings():
    chunksize = 1000
    with pd.read_csv(EMBEDDINGS_PATH, chunksize=chunksize) as reader:
        for chunk in reader:
            for idx, row in chunk.iterrows():
                embedding_id = row["ID_EMBEDDING"]
                participacion_id = row["ID_PARTICIPACION"]
                embedding = row["EMBEDDINGS"]

                line = f'emb_{embedding_id} :Embedding value:tensorFloat("{embedding}")'
                print(line)
                print(f"emb_{embedding_id}->partic_{participacion_id} :tieneParticipation")


if __name__ == "__main__":
    with open("congress.qm", "w", encoding="utf-8") as f:
        sys.stdout = f  # Redirect all print output to this file
        process_parlamentarios()
        process_participaciones()
        process_embeddings()
        sys.stdout = sys.__stdout__  # Restore stdout 

