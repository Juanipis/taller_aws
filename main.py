import argparse
import datetime
import json
import boto3
from dotenv import load_dotenv
import requests
import os


class AWSCredentials:
    def __init__(self):
        self.access_key_id = os.getenv('AWS_ACCES_KEY_ID')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

def main(aws_credentials : AWSCredentials):
    parser = argparse.ArgumentParser(description='Retrieve and save Pokemon data from PokeAPI')
    parser.add_argument('pokemon_name', type=str, help='Name of the Pokemon to retrieve data for')
    args = parser.parse_args()

    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{args.pokemon_name}')
    if response.status_code != 200:
        print(f'Error retrieving data for {args.pokemon_name}: {response.status_code}')
        return
    print(f'Successfully retrieved data for {args.pokemon_name}')

    s3 = boto3.client('s3', aws_access_key_id=aws_credentials.access_key_id, aws_secret_access_key=aws_credentials.secret_key)
    bucket_name = 'eia-so-bucket-dev'
    key = f'natynaro-juanipis/pokemon/{args.pokemon_name}/{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.json'
    #Create json file
    with open(f'{args.pokemon_name}.json', 'w') as outfile:
        json.dump(response.json(), outfile)
    #Upload file to S3
    s3.upload_file(f'{args.pokemon_name}.json', bucket_name, key)
    print(f'Successfully uploaded data for {args.pokemon_name} to S3')



if __name__ == '__main__':
    load_dotenv()
    aws_credentials = AWSCredentials()
    print(f'Using AWS credentials: {aws_credentials.access_key_id}')
    print(f'Using AWS credentials: {aws_credentials.secret_key}')
    main(aws_credentials)
