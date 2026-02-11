import json
import boto3
import os
import csv
import codecs
import re

# 1. Configuración desde Variables de Entorno
NOMBRE_BUCKET = os.environ.get('BUCKET_NAME')
ARCHIVO_CSV = os.environ.get('FILE_NAME')

def normalizar(texto):
    """Limpia texto para una búsqueda robusta sin acentos ni mayúsculas."""
    texto = texto.lower()
    texto = re.sub(r'[áéíóú]', lambda m: {'á':'a','é':'e','í':'i','ó':'o','ú':'u'}[m.group()], texto)
    return texto.strip()

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

    # Validación preventiva de variables
    if not NOMBRE_BUCKET or not ARCHIVO_CSV:
        return {
            'statusCode': 500,
            'body': "Error: Variables de entorno BUCKET_NAME o FILE_NAME no configuradas."
        }

    try:
        # 2. Captura de parámetros desde la URL
        params = event.get('queryStringParameters', {}) or {}
        sector = normalizar(params.get('sector', 'Energia'))
        estado = normalizar(params.get('estado', 'Mexico'))

        # 3. Lectura eficiente de S3
        response = s3.get_object(Bucket=NOMBRE_BUCKET, Key=ARCHIVO_CSV)
        stream = codecs.getreader('latin-1')(response['Body'])
        reader = csv.DictReader(stream)
        
        muestra_raw = []
        for i, row in enumerate(reader):
            if i > 15000: break # Límite de seguridad
            
            # Unimos la fila para búsqueda
            fila_texto = normalizar(" ".join(filter(None, row.values())))
            
            if sector in fila_texto and estado in fila_texto:
                muestra_raw.append({
                    'Empresa': row.get('nom_estab', 'N/A'),
                    'Actividad': row.get('nombre_act', 'N/A'),
                    'Ubicacion': f"{row.get('municipio', '')}, {row.get('entidad', '')}",
                    'Tamano': row.get('per_ocu', 'N/A')
                })
            
            if len(muestra_raw) >= 10: break

        # 4. Generación de Resumen con IA
        if muestra_raw:
            prompt = f"""You are a SPM Consultant. 
            Analyze these companies: {json.dumps(muestra_raw)}.
            Provide a 2-paragraph executive summary in English about why this specific 
            sector needs automated sales incentive solutions. Professional tone."""
            
            body_ia = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "messages": [{"role": "user", "content": prompt}]
            })
            
            res_ai = bedrock.invoke_model(modelId='anthropic.claude-3-haiku-20240307-v1:0', body=body_ia)
            texto_ia = json.loads(res_ai.get('body').read())['content'][0]['text']
        else:
            texto_ia = f"No records found for sector '{sector}' in '{estado}'."

        # 5. Construcción del Reporte
        reporte = f"""
        ======================================================================
        STRATEGIC INSIGHTS: {sector.upper()}
        ======================================================================
        
        PART I: EXECUTIVE SUMMARY (AI-GENERATED)
        ----------------------------------------------------------------------
        {texto_ia}
        
        PART II: DATA TRACEABILITY (EVIDENCE)
        ----------------------------------------------------------------------
        Target:  [{sector.upper()}] in [{estado.upper()}]
        
        Raw Data (JSON):
        {json.dumps(muestra_raw, indent=4, ensure_ascii=False)}
        
        PART III: INFRASTRUCTURE METADATA
        ----------------------------------------------------------------------
        Cloud:   AWS Serverless (Lambda + Bedrock)
        Storage: Amazon S3 (Streaming Mode)
        Status:  Operational
        
        ======================================================================
        Prepared by Esteban Rojano | Data Architecture Demo
        ======================================================================
        """

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain; charset=utf-8',
                'Access-Control-Allow-Origin': '*'
            },
            'body': reporte
        }

    except Exception as e:
        print(f"Error detectado: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": "Pipeline Failure", "details": str(e)})
        }