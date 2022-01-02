import * as cdk from '@aws-cdk/core'
import * as lambda from '@aws-cdk/aws-lambda'
import * as dynamo from '@aws-cdk/aws-dynamodb'
import { DynamoEventSource } from '@aws-cdk/aws-lambda-event-sources'
import * as path from 'path'

export interface FootwedgeApiProps {
  envName: string,
  serviceName: string,
  cognitoRegion: string,
  cognitoUserPoolId: string,
  cognitoWebClientId: string,
  dynamoDbUrl: string,
  footwedgeDynamoTableName: string,
}

export function generateFootwedgeApiLambda(
  scope: cdk.Construct,
  props: FootwedgeApiProps
): lambda.Function {
  const id = 'footwedge-api'
  return new lambda.Function(scope, id, {
    runtime: lambda.Runtime.PYTHON_3_7,
    code: lambda.Code.fromAsset(
      path.join(__dirname, `../../../${id}/target`)
    ),
    handler: 'handler.lambda_handler',
    functionName: `${props.envName}-${props.serviceName}-${id}`,
    memorySize: 512,
    timeout: cdk.Duration.minutes(5),
    environment: {
      ENV_NAME: props.envName,
      PYTHONPATH: 'src',
      COGNITO_REGION: props.cognitoRegion,
      COGNITO_USER_POOL_ID: props.cognitoUserPoolId,
      COGNITO_WEB_CLIENT_ID: props.cognitoWebClientId,
      DYNAMO_DB_URL: props.dynamoDbUrl,
      FOOTWEDGE_DYNAMO_TABLE: props.footwedgeDynamoTableName,
    }
  })
}

export function generateSearchServiceLambda(
  scope: cdk.Construct,
  envName: string,
  serviceName: string,
  algoliaAppId: string,
  algoliaApiKey: string
): lambda.Function {
  const id = 'searchService'
  const searchServiceLambda = new lambda.Function(scope, id, {
    runtime: lambda.Runtime.NODEJS_14_X,
    code: lambda.Code.fromAsset(path.join(__dirname, `../../../dist/${id}`)),
    handler: 'index.lambdaHandler',
    functionName: `${envName}-${serviceName}-${id}`,
    memorySize: 512,
    timeout: cdk.Duration.minutes(5),
    environment: {
      ENV_NAME: envName,
      ALGOLIA_FOOTWEDGE_APP_ID: algoliaAppId,
      ALGOLIA_API_KEY: algoliaApiKey,
    },
  })

  return searchServiceLambda
}

export function generatePostConfirmationLambda(
  scope: cdk.Construct,
  envName: string,
  serviceName: string,
): lambda.Function {
  const id = 'post-confirmation-service'
  return new lambda.Function(scope, id, {
    runtime: lambda.Runtime.PYTHON_3_7,
    code: lambda.Code.fromAsset(
      path.join(__dirname, `../../../${id}/target`)
    ),
    handler: 'handler.lambda_handler',
    functionName: `${envName}-${serviceName}-${id}`,
    memorySize: 512,
    timeout: cdk.Duration.minutes(2),
    environment: {
      FOOTWEDGE_API_URL: 'https://api.footwedge.io/v1',
      ENV_NAME: envName,
    }
  })
}

export interface StreamServiceProps {
  envName: string,
  serviceName: string,
  cognitoDomain: string,
  cognitoRegion: string,
  streamServiceCognitoClientId: string,
  streamServiceCognitoClientSecret: string,
  footwedgeTable: dynamo.Table,
}

export function generateStreamServiceLambda(
  scope: cdk.Construct,
  props: StreamServiceProps,
): lambda.Function {
  const id = 'stream-service'
  const fn = new lambda.Function(scope, id, {
    runtime: lambda.Runtime.PYTHON_3_7,
    code: lambda.Code.fromAsset(
      path.join(__dirname, `../../../${id}/target`)
    ),
    handler: 'handler.lambda_handler',
    functionName: `${props.envName}-${props.serviceName}-${id}`,
    memorySize: 512,
    timeout: cdk.Duration.minutes(2),
    environment: {
      ENV_NAME: props.envName,
      COGNITO_DOMAIN: props.cognitoDomain,
      COGNITO_REGION: props.cognitoRegion,
      STREAM_SERVICE_COGNITO_CLIENT_ID: props.streamServiceCognitoClientId,
      STREAM_SERVICE_COGNITO_CLIENT_SECRET: props.streamServiceCognitoClientSecret,
      FOOTWEDGE_API_URL: 'https://api.footwedge.io/v1',
      FOOTWEDGE_SEARCH_URL: 'https://search.footwedge.io',
    }
  })
  fn.addEventSource(new DynamoEventSource(footwedgeTable, {
    startingPosition: lambda.StartingPosition.TRIM_HORIZON,
    batchSize: 5,
    bisectBatchOnError: true,
    // onFailure: new SqsDlq(deadLetterQueue),
    retryAttempts: 5,
  }))
  return fn
}
