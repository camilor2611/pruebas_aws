# Requisitos
- Docker
- Python 3.12 o posterior
- Node 18 o posterior
- Cuenta de AWS con permisos de administrador
- AWS CLI 2.17 o posterior
- Crear el bucket en S3

# Configuración
1. Crear persona en IAM con política AdministratorAccess (Está politica puede ser con menores permisos, pero a nivel didactico dejaremos la política de administrador), crear sus access key y secret key
2. Configurar AWS CLI con el comando `aws configure`, aquí se necesitanrán el access key y secret key creados en el paso anterior
3. Instalar `npm install -g aws-cdk aws-cdk-lib`  
4. Ejecutar el siguiente comando para crear el entorno de despliegue del aplicativo en cloud formation `cdk bootstrap aws://<NUMERO_DE_CUENTA_AWS>/<REGION_DE_CUENTA_AWS> --qualifier bcrcprecia --toolkit-stack-name CDKToolkit-bcrcprecia --bootstrap-bucket-name cdk-bcrcprecia-assets-<NUMERO_DE_CUENTA_AWS>-<REGION_DE_CUENTA_AWS>`
5. Crear un bucket en S3
6. Crear una tabla en DynamoDB con clave de paticion file_id (String), y clave de ordenación version (Number)  
7. Configurar las variables de entorno, para ello se debe crear un archivo .env en la raiz del proyecto con las siguientes variables

ENVIRONMENT = "dev"
AWS_ACCOUNT_DEPLOY = "<NUMERO_DE_CUENTA_AWS>"
AWS_REGION_DEPLOY = "<REGION_DE_CUENTA_AWS>"
QUALIFIER = "bcrcprecia"
BUCKET_NAME = "<NOMBRE_DEL_BUCKET_CREADO_ANTERIORMENTE>"
DYNAMO_TABLE_NAME = "<NOMBRE_DE_LA_TABLA_CREADA_ANTERIORMENTE>"

8. Crear un entorno virtual en la raíz del proyecto, activar el entorno virtual y instalar en el `requirements_dev.txt`, posteriormente dentro de la carpeta lib ejecutar el comando `npx cdk deploy --require-approval never devStackLambdas`
