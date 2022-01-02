import * as cdk from '@aws-cdk/core'
import * as cognito from '@aws-cdk/aws-cognito'
import * as lambda from '@aws-cdk/aws-lambda'
import { ResourceServerScope } from '@aws-cdk/aws-cognito'

export function generateCognitoUserPool(
  scope: cdk.Construct,
  envName: string,
  postConfirmationLambda: lambda.Function
): cognito.UserPool {
  return new cognito.UserPool(scope, 'FootwedgeUserPool', {
    userPoolName: `${envName}-footwedge`,
    selfSignUpEnabled: true,
    signInAliases: {
      email: true,
    },
    autoVerify: {
      email: true,
    },
    accountRecovery: cognito.AccountRecovery.EMAIL_ONLY,
    standardAttributes: {
      givenName: {
        required: true,
        mutable: true,
      },
      familyName: {
        required: true,
        mutable: true,
      },
      email: {
        required: true,
        mutable: false,
      },
    },
    customAttributes: {
      'firstName': new cognito.StringAttribute({ mutable: true }),
      'lastName': new cognito.StringAttribute({ mutable: true }),
    },
    passwordPolicy: {
      minLength: 8,
      requireLowercase: true,
      requireUppercase: true,
      requireDigits: true,
      requireSymbols: true,
    },
    signInCaseSensitive: false,
    lambdaTriggers: {
      postConfirmation: postConfirmationLambda,
    },
  })
}

export function addDomain(
  userPool: cognito.UserPool,
  envName: string
): cognito.UserPoolDomain {
  return userPool.addDomain('CognitoDomain', {
    cognitoDomain: {
      domainPrefix: `${envName}-footwedge`,
    },
  })
}

export function generateScope(
  scopeName: string,
  scopeDescription: string
): cognito.ResourceServerScope {
  return new ResourceServerScope({ scopeName, scopeDescription })
}

export function addResourceServer(
  userPool: cognito.UserPool,
  golfRoundsReadScope: cognito.ResourceServerScope,
  handicapWriteScope: cognito.ResourceServerScope,
  golfClubWriteScope: cognito.ResourceServerScope
): cognito.UserPoolResourceServer {
  return userPool.addResourceServer('FootwedgeUserPoolResourceServer', {
    identifier: 'footwedge-api',
    scopes: [golfRoundsReadScope, handicapWriteScope, golfClubWriteScope],
  })
}

export function addWebClient(
  userPool: cognito.UserPool
): cognito.UserPoolClient {
  return userPool.addClient('WebClient', {
    userPoolClientName: 'footwedge-web',
  })
}

export function addStreamServiceClient(
  userPool: cognito.UserPool,
  resourceServer: cognito.UserPoolResourceServer,
  golfRoundsReadScope: cognito.ResourceServerScope,
  handicapWriteScope: cognito.ResourceServerScope
): cognito.UserPoolClient {
  return userPool.addClient('StreamServiceClient', {
    oAuth: {
      flows: {
        clientCredentials: true,
      },
      scopes: [
        cognito.OAuthScope.resourceServer(resourceServer, golfRoundsReadScope),
        cognito.OAuthScope.resourceServer(resourceServer, handicapWriteScope),
      ],
    },
    generateSecret: true,
    userPoolClientName: 'stream-service',
  })
}

export function addScrapeServiceClient(
  userPool: cognito.UserPool,
  resourceServer: cognito.UserPoolResourceServer,
  golfClubWriteScope: cognito.ResourceServerScope
): cognito.UserPoolClient {
  return userPool.addClient('ScrapeServiceClient', {
    oAuth: {
      flows: {
        clientCredentials: true,
      },
      scopes: [
        cognito.OAuthScope.resourceServer(resourceServer, golfClubWriteScope),
      ],
    },
    generateSecret: true,
    userPoolClientName: 'scrape-service',
  })
}
