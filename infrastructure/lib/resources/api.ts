import * as apigateway from '@aws-cdk/aws-apigateway'
import * as cdk from '@aws-cdk/core'
import * as lambda from '@aws-cdk/aws-lambda'
import * as acm from '@aws-cdk/aws-certificatemanager'
import * as route53 from '@aws-cdk/aws-route53'
import * as targets from '@aws-cdk/aws-route53-targets'
import { getFootwedgeHostedZone } from './route53'

export function generateFootwedgeApi(
  scope: cdk.Construct,
  footwedgeApiLambda: lambda.Function,
  footwedgeApiDomainName: string
): apigateway.LambdaRestApi {
  const api = new apigateway.LambdaRestApi(scope, 'FootwedgeApi', {
    handler: footwedgeApiLambda,
  })
  const domainCert = acm.Certificate.fromCertificateArn(
    scope,
    'FootwedgeApiCert',
    'arn:aws:acm:us-east-1:753710783959:certificate/eae95265-612c-4a51-b197-6d0c8923e728'
  )
  api.addDomainName('FootwedgeApiDomain', {
    certificate: domainCert,
    domainName: footwedgeApiDomainName,
    endpointType: apigateway.EndpointType.EDGE,
  })
  const footwedgeHostedZone = getFootwedgeHostedZone(scope)
  new route53.ARecord(scope, 'FootwedgeApiARecord', {
    zone: footwedgeHostedZone,
    target: route53.RecordTarget.fromAlias(new targets.ApiGateway(api)),
    recordName: footwedgeApiDomainName,
  })

  return api
}

export function generateSearchServiceApi(
  scope: cdk.Construct,
  searchServiceLambda: lambda.Function
): apigateway.LambdaRestApi {
  return new apigateway.LambdaRestApi(scope, 'SearchServiceApi', {
    handler: searchServiceLambda,
  })
}
