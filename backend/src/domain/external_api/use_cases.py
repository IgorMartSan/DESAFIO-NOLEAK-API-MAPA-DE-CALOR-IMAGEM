from typing import List, Dict
import pandas as pd
import requests
import unicodedata
import pandas as pd

class UseCases:
    @staticmethod
    def fetch_data(url: str, sep: str = ';', encoding: str = 'latin1') -> List[Dict]:
        try:
            # Verifica se a URL está acessível
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Gera um erro se o status não for 200

            # Lê o CSV diretamente da URL
            df = pd.read_csv(url, sep=sep, encoding=encoding)
            df.to_csv("./data.csv")
            return df.fillna('')

        except requests.exceptions.HTTPError as http_err:
            raise Exception(f"Erro HTTP ao acessar {url}: {http_err}")
        except requests.exceptions.ConnectionError:
            raise Exception(f"Erro de conexão ao acessar {url}. Verifique a URL ou sua conexão.")
        except requests.exceptions.Timeout:
            raise Exception(f"Timeout ao tentar acessar {url}.")
        except pd.errors.ParserError as parse_err:
            raise Exception(f"Erro ao ler o CSV de {url}: {parse_err}")
        except Exception as e:
            raise Exception(f"Erro inesperado ao processar {url}: {e}")
        

        
    @staticmethod
    def remover_acentos(texto):
        if not isinstance(texto, str):
            return texto
        nfkd = unicodedata.normalize('NFKD', texto)
        return ''.join([c for c in nfkd if not unicodedata.combining(c)])
    
    @staticmethod
    def transformar_dataframe_em_json(df: pd.DataFrame, num_colunas_fixas: int) -> list:
        """
        Transforma um DataFrame onde as primeiras N colunas são fixas
        e o restante são valores de séries temporais com o ano como nome da coluna.

        Args:
            df (pd.DataFrame): DataFrame de entrada.
            num_colunas_fixas (int): Quantidade de colunas fixas (ex: Id e Pais = 2).

        Returns:
            list: Lista de dicionários estruturados com campo 'dados'.
        """
        # Remove acentos das colunas
        df.columns = [UseCases.remover_acentos(str(c)) for c in df.columns]

        # Remove acentos em colunas tipo "Pais"
        for col in df.columns[:num_colunas_fixas]:
            if df[col].dtype == object:
                df[col] = df[col].apply(UseCases.remover_acentos)

        colunas_fixas = df.columns[:num_colunas_fixas]
        colunas_dados = df.columns[num_colunas_fixas:]

        resultado = []

        for _, row in df.iterrows():
            item = {col: row[col] for col in colunas_fixas}
            dados = []

            for col in colunas_dados:
                try:
                    ano = float(col)
                    valor = row[col]
                    dados.append({"ano": ano, "valor": valor})
                except:
                    continue

            item["dados"] = dados
            resultado.append(item)

        return resultado

    @staticmethod
    def get_producao(csv_url: str = "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv", sep: str = ';', encoding: str = 'latin1') -> List[Dict]:
        df = UseCases.fetch_data(csv_url, sep=sep, encoding=encoding)
        json = UseCases.transformar_dataframe_em_json(df,3)
        return json

    @staticmethod
    def get_processamento(csv_url: str = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv", sep: str = ';', encoding: str = 'latin1') -> List[Dict]:  
        df = UseCases.fetch_data(csv_url, sep=sep, encoding=encoding)
        json = UseCases.transformar_dataframe_em_json(df,3)
        return json 

    @staticmethod
    def get_comercializacao(csv_url: str = "http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv", sep: str = ';', encoding: str = 'latin1') -> List[Dict]:
        df = UseCases.fetch_data(csv_url, sep=sep, encoding=encoding)
        json = UseCases.transformar_dataframe_em_json(df,3)
        return json 

    @staticmethod
    def get_importacao(csv_url: str = "http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv", sep: str = '\t', encoding: str = 'latin1') -> List[Dict]:
        df = UseCases.fetch_data(csv_url, sep=sep, encoding=encoding)
        json = UseCases.transformar_dataframe_em_json(df,3)
        return json 

    @staticmethod
    def get_exportacao(csv_url: str = "http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv", sep: str = '\t', encoding: str = 'latin1') -> List[Dict]:
        df = UseCases.fetch_data(csv_url, sep=sep, encoding=encoding)
        json = UseCases.transformar_dataframe_em_json(df,3)
        return json 
