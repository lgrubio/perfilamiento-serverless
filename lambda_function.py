import boto3
import os
from boto3.dynamodb.conditions import Key

DYNAMO_BD = os.environ['DYNAMO_BD']

# Función de perfilamiento de clientes

class DynamoAccessor:
    def __init__(self, dynamo_table):
        dynamo_db = boto3.resource('dynamodb')
        self.table = dynamo_db.Table(dynamo_table)

    def get_data_from_dynamo(self, cedula):
        response = self.table.query(KeyConditionExpression=Key('cedula').eq(cedula))
        print("Nombre", response["Items"][0]['nombre'])
        print("Score", response["Items"][0]['score'])
        
        score = response["Items"][0]['score']
        activo = response["Items"][0]['usuarioActivo']
        mora = response["Items"][0]['usuarioMora']
        
        if score>70 and activo == bool(True) and mora ==bool(False) :
            print("Usuario apto para realizar prestamo")
        elif score >70 and activo == bool(False) and mora ==bool(False):
          print("Usuario no Activo")
        elif score >70 and activo == bool(True) and mora ==bool(True):
          print("El usuario se encuentra en mora")
        elif score <70 and activo == bool(True) and mora ==bool(False):
          print("Puntuacion baja para prestamo")
        elif score >70 and activo == bool(False) and mora ==bool(False):
          print("Usuario no Activo")
        else:
          print("El usuario no cumple con los requisitos para el prestamo")
        return response["Items"][0] if any(response["Items"]) else None

def lambda_handler(event, context):
    dynamo_backend = DynamoAccessor(DYNAMO_BD)
    db_element = dynamo_backend.get_data_from_dynamo(event['cedula'])
    return db_element

print("Perfilamiento de clientes:")