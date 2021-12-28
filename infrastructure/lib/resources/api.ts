import * as apigateway from '@aws-cdk/aws-apigateway'
import * as cdk from '@aws-cdk/core'
import * as lambda from '@aws-cdk/aws-lambda'

export function generateSearchServiceApi(
  scope: cdk.Construct,
  searchServiceLambda: lambda.Function
): apigateway.LambdaRestApi {
  return new apigateway.LambdaRestApi(scope, 'SearchServiceApi', {
    handler: searchServiceLambda,
  })
}
