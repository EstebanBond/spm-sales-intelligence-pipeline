import boto3
import os
from pathlib import Path
from dotenv import load_dotenv

def upload_to_s3():
    # 1. Localizar el archivo .env con ruta absoluta
    env_path = Path(__file__).parent / '.env'
    
    # 2. Cargar y verificar
    if not load_dotenv(dotenv_path=env_path):
        print(f"❌ Error: No se encontró el archivo .env en: {env_path}")
        return

    # 3. Asignar variables DENTRO de la función para asegurar que ya cargaron
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    bucket_name = os.getenv('AWS_BUCKET_NAME')
    file_path = os.getenv('LOCAL_FILE_PATH')
    object_name = os.getenv('AWS_S3_OBJECT')

    # 4. Diagnóstico de variables (Esto nos dirá qué falta)
    print("--- Diagnóstico de Carga ---")
    print(f"Bucket: {'✅ Detectado' if bucket_name else '❌ VACÍO (None)'}")
    print(f"Ruta Archivo: {'✅ Detectada' if file_path else '❌ VACÍA (None)'}")
    print(f"Llaves AWS: {'✅ Detectadas' if access_key and secret_key else '❌ FALTAN'}")
    print("----------------------------")

    # 5. Validación de seguridad antes de conectar
    if not all([access_key, secret_key, bucket_name, file_path]):
        print("🛑 Deteniendo: Revisa que los nombres en el .env coincidan con el código.")
        return

    # 6. Verificación física del archivo en tu Mac
    if not os.path.exists(file_path):
        print(f"❌ Error: El archivo NO existe en la ruta: {file_path}")
        return

    # 7. Conexión y subida
    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    
    try:
        print(f"🚀 Iniciando carga a S3 ({bucket_name})...")
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"✅ ¡Éxito! El archivo del INEGI ya está en la nube.")
    except Exception as e:
        print(f"❌ Error de AWS: {e}")

if __name__ == "__main__":
    upload_to_s3()