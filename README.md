# Introducción

Este documento proporciona una guía detallada para la configuración, despliegue, prueba y eliminación de un aplicativo en AWS utilizando **Docker, AWS Lambda, S3, DynamoDB y AWS CDK**. Se describen los requisitos previos, los pasos de configuración y los comandos necesarios para gestionar los recursos en la nube de manera eficiente.

El aplicativo funciona de la siguiente manera:

1. **dev_load_file**: Esta función Lambda recibe un archivo en **base64** y lo almacena en **S3**, y retorna el file_id hash **SHA-256** y su versión **timestamp**.
2. **generate_check_sum**: Descarga el archivo desde **S3**, guarda el hash **SHA-256** del contenido como `file_id` en **DynamoDB**.
3. **get_check_sum**: Verifica si el `file_id` ya está registrado en **DynamoDB**.

Este flujo garantiza la integridad y trazabilidad de los archivos procesados.

# Requisitos  
- Docker  
- Python 3.12 o posterior  
- Node 18 o posterior  
- Cuenta de AWS con permisos de administrador  
- AWS CLI 2.17 o posterior  
- Crear un bucket en S3  

# Configuración y despliegue  
1. Crear un usuario en IAM con la política **AdministratorAccess** (esta política puede tener permisos más restrictivos, pero para fines didácticos usaremos la de administrador). Luego, generar las claves de acceso (**access key** y **secret key**).  
2. Configurar AWS CLI con el comando `aws configure`. Se necesitarán las claves creadas en el paso anterior. También se debe configurar:  
   - **Default region name:** `<REGION_DE_CUENTA_AWS>`  
   - **Default output format:** `json`  
3. Instalar los paquetes necesarios con:  
   ```sh
   npm install -g aws-cdk aws-cdk-lib
   ```  
4. Ejecutar el siguiente comando para crear el entorno de despliegue en **CloudFormation**:  
   ```sh
   cdk bootstrap aws://<NUMERO_DE_CUENTA_AWS>/<REGION_DE_CUENTA_AWS> --qualifier bcrcprecia --toolkit-stack-name CDKToolkit-bcrcprecia --bootstrap-bucket-name cdk-bcrcprecia-assets-<NUMERO_DE_CUENTA_AWS>-<REGION_DE_CUENTA_AWS>
   ```  
5. Crear un **bucket** privado en S3.  
6. Crear una tabla en **DynamoDB** con:  
   - **Clave de partición:** `file_id (String)`  
   - **Clave de ordenación:** `version (Number)`  
7. Configurar las variables de entorno creando un archivo **.env** en la raíz del proyecto con el siguiente contenido:  

   ```text
   ENVIRONMENT = "dev"
   AWS_ACCOUNT_DEPLOY = "<NUMERO_DE_CUENTA_AWS>"
   AWS_REGION_DEPLOY = "<REGION_DE_CUENTA_AWS>"
   QUALIFIER = "bcrcprecia"
   BUCKET_NAME = "<NOMBRE_DEL_BUCKET_CREADO_ANTERIORMENTE>"
   DYNAMO_TABLE_NAME = "<NOMBRE_DE_LA_TABLA_CREADA_ANTERIORMENTE>"
   ```  
8. Crear y activar un entorno virtual en la raíz del proyecto, instalar las dependencias desde `requirements_dev.txt` y luego ejecutar el siguiente comando dentro de la carpeta `lib`:  
   ```sh
   npx cdk deploy --require-approval never devStackLambdas
   ```  
   Esto creará las **tres funciones Lambda** y sus respectivas imágenes **Docker**.  

Una vez desplegadas, podemos probar su funcionamiento con las siguientes Lambdas:  
- `load_file`  
- `generate_check_sum`  
- `get_check_sum`  

# Probar el aplicativo  

Desde la consola de AWS, dirígete a la función Lambda **dev_load_file** y configura el evento de prueba de la siguiente manera:  

```json
{
  "content": "RVNUTyBFUyBVTiBBUkNISVZPIERFIFBSVUVCQSAy",
  "content_type": "text/plain",
  "format_file": "txt",
  "create_new_version": false
}
```  

- El campo **"content"** es el contenido del archivo en **Base64**. Para la prueba, puedes crear un archivo **.txt**, cargarlo en [base64.guru](https://base64.guru/converter/encode/file) y reemplazar el valor.  
- Si **"create_new_version"** es `false`, la Lambda verificará si ya existe un archivo con el mismo **ID (hash)** en S3. Si existe, no subirá un nuevo archivo y retornará los datos del archivo existente con estado `"READY"`.  
- Si **"create_new_version"** es `true`, se subirá un nuevo archivo con el mismo contenido pero con una versión diferente.  

Cuando se ejecuta esta Lambda, el archivo se sube a S3 y se genera un **file_id**, una **versión** y otros datos. Esta Lambda **no** guarda información en **DynamoDB** y responderá con un JSON similar al siguiente:  

```json
{
  "success": true,
  "data": {
    "file_id": "f16e1ab30c2e9ff43352ee0c5a7d966acb8e2fd0026552d3a887135a3254d8d4",
    "path_s3": "files/1740800450_43421c9f-5897-4207-a455-f1fae4593b9d.txt",
    "version": 1740800450,
    "status": "PROCESSING"
  }
}
```  

La Lambda **generate_check_sum** se ejecuta automáticamente al detectar un nuevo archivo en S3. Luego, descarga el archivo y guarda en **DynamoDB** el `file_id`, la `version` y el `path_s3`.  

**Nota:** Se ha agregado un **retraso de 10 segundos** antes de registrar la información en **DynamoDB**, para permitir la ejecución de la siguiente Lambda.  

Finalmente, podemos verificar si nuestro archivo ya está registrado en **DynamoDB** ejecutando la Lambda **get_check_sum**. Para ello, configuramos el evento de prueba de la siguiente manera:  

```json
{
  "file_id": "f16e1ab30c2e9ff43352ee0c5a7d966acb8e2fd0026552d3a887135a3254d8d4",
  "version": 1740800450
}
```  

Si el campo `"version"` es `null`, se consultará la versión más reciente del archivo.  

# Destruir recursos  

Una vez finalizadas las pruebas, se pueden eliminar los recursos con el siguiente comando (ejecutado dentro de la carpeta `lib`):  

```sh
npx cdk destroy devStackLambdas
```  

También se deben eliminar manualmente los siguientes recursos:  
- En **CloudFormation**, eliminar la pila **CDKToolkit-bcrcprecia**.  
- En **S3**, eliminar el bucket.  
- En **DynamoDB**, eliminar la tabla.  

