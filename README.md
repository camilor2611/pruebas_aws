# Requisitos
- Docker
- Python 3.12 o posterior
- Node 18 o posterior
- Cuenta de AWS con permisos de administrador
- AWS CLI 2.17 o posterior
- Crear el bucket en S3

# Configuración y despliegue
1. Crear persona en IAM con política AdministratorAccess (Está politica puede ser con menores permisos, pero a nivel didactico dejaremos la política de administrador), crear sus access key y secret key
2. Configurar AWS CLI con el comando `aws configure`, aquí se necesitanrán el access key y secret key creados en el paso anterior, tambien se debe configurar "Default region name" y "Default output format" cuyos valores son <REGION_DE_CUENTA_AWS> y json respectivamente
3. Instalar `npm install -g aws-cdk aws-cdk-lib`  
4. Ejecutar el siguiente comando para crear el entorno de despliegue del aplicativo en cloud formation `cdk bootstrap aws://<NUMERO_DE_CUENTA_AWS>/<REGION_DE_CUENTA_AWS> --qualifier bcrcprecia --toolkit-stack-name CDKToolkit-bcrcprecia --bootstrap-bucket-name cdk-bcrcprecia-assets-<NUMERO_DE_CUENTA_AWS>-<REGION_DE_CUENTA_AWS>`
5. Crear un bucket privado de S3
6. Crear una tabla en DynamoDB con clave de paticion **file_id (String)**, y clave de ordenación **version (Number)**
7. Configurar las variables de entorno, para ello se debe crear un archivo .env en la raiz del proyecto con las siguientes variables

```json
ENVIRONMENT = "dev"
AWS_ACCOUNT_DEPLOY = "<NUMERO_DE_CUENTA_AWS>"
AWS_REGION_DEPLOY = "<REGION_DE_CUENTA_AWS>"
QUALIFIER = "bcrcprecia"
BUCKET_NAME = "<NOMBRE_DEL_BUCKET_CREADO_ANTERIORMENTE>"
DYNAMO_TABLE_NAME = "<NOMBRE_DE_LA_TABLA_CREADA_ANTERIORMENTE>"
```

8. Crear un entorno virtual en la raíz del proyecto, activar el entorno virtual y instalar en el `requirements_dev.txt`, posteriormente dentro de la carpeta `lib` ejecutar el comando `npx cdk deploy --require-approval never devStackLambdas` esto creará los 3 lambda y sus respectivas imagenes Docker.

Una vez desplegadas podemos probar su funcionamento en las lambdas creadas
- load_file
- generate_check_sum
- get_check_sum

# Probar aplicativo

Desde la consola de AWS nos dirijimos al lambda **dev_load_file** y el evento de prueba se configura de la siguiente manera
```json
{
  "content": "RVNUTyBFUyBVTiBBUkNISVZPIERFIFBSVUVCQSAy",
  "content_type": "text/plain",
  "format_file": "txt",
  "create_new_version": false 
}
```

El "content" es el valor de un archivo en base64, para la prueba se sugiere crear un archivo .txt y cargarlo en [base64.guru](https://base64.guru/converter/encode/file) y reemplazar el valor

Si el valor de **create_new_version** es false, significa que si existe un archivo con el mismo id (hash) no subirá ningun archivo a s3 y retornará los datos del archivo ya existente y su estado será "READY". En caso de ser true creará otro archivo en s3, con el mismo id (hash, es decir, mismo contenido) pero con una version diferente

Una vez ejecutada la lambda se sube el archivo a s3 y genera el file_id, version y demás datos. Tenga en cuenta que esta lambda no registra nada en DynamoDB y responderá
```json
{
  "success": true,
  "data": {
    "file_id": "f16e1ab30c2e9ff43352ee0c5a7d966acb8e2fd0026552d3a887135a3254d8d4",
    "path_s3": "files/1740800450_43421c9f-5897-4207-a455-f1fae4593b9d.txt",
    "version": 1740800450, // la version es un timestamp
    "status": "PROCESSING"
  }
}
```
Luego la lambda **generate_check_sum** se ejecuta automaticamente cuando detecta que un archivo es subido al bucket, posteriormente descarga el archivo de s3 y guarda el file_id, version, y el path_s3 en DynamoDB. En el código se agregó un tiempo de espera (10s) antes de radicar la información en DynamoDB esto con el fin de validar la siguiente lambda.

Finalmente podemos validar si nuestro id (hash) ya está radicado en nuestra base de datos Dynamo, ejecutando el lambda **get_check_sum** y teniendo en cuenta los datos obtenidos de **create_new_version**, para ello configuramos el evento de prueba así

```json
{
  "file_id": "f16e1ab30c2e9ff43352ee0c5a7d966acb8e2fd0026552d3a887135a3254d8d4",
  "version": 1740800450, // es opcional
}
```

si la version es `null` se validará la última versión

# Destruir recursos
Una vez se realicen las pruebas correspondientes se pueden eliminar los recursos con `npx cdk destoy devStackLambdas` y manualmente se deben eliminar los siguientes recursos
- En CloudFormation eliminar la pila CDKToolkit-bcrcprecia
- En s3 eliminar el bucket
- En DynamoDb eliminar la tabla
