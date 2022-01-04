import * as cdk from '@aws-cdk/core'
import * as lambda from '@aws-cdk/aws-lambda'
import * as dynamo from '@aws-cdk/aws-dynamodb'

export function generateTable(
  scope: cdk.Construct,
  tableName: string,
  footwedgeApiLambda: lambda.Function
): dynamo.Table {
  const table = new dynamo.Table(scope, 'FootwedgeTable', {
    tableName: tableName,
    partitionKey: { name: 'pk', type: dynamo.AttributeType.STRING },
    sortKey: { name: 'sk', type: dynamo.AttributeType.STRING },
    stream: dynamo.StreamViewType.NEW_IMAGE,
    billingMode: dynamo.BillingMode.PAY_PER_REQUEST,
  })
  table.addGlobalSecondaryIndex({
    indexName: 'GSI1',
    partitionKey: { name: 'gsi1pk', type: dynamo.AttributeType.STRING },
    sortKey: { name: 'gsi1sk', type: dynamo.AttributeType.STRING },
    projectionType: dynamo.ProjectionType.ALL,
  })
  table.grantReadWriteData(footwedgeApiLambda)

  return table
}
