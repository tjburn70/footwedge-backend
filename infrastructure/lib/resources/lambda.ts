import * as cdk from '@aws-cdk/core'
import * as lambda from '@aws-cdk/aws-lambda'
import * as path from 'path'

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
