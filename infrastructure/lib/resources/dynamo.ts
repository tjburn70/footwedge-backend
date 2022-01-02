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
    partitionKey: { name: 'PK', type: dynamo.AttributeType.STRING },
    sortKey: { name: 'SK', type: dynamo.AttributeType.STRING },
    readCapacity: 1,
    writeCapacity: 1,
    stream: dynamo.StreamViewType.NEW_IMAGE,
  })
  table.addGlobalSecondaryIndex({
    indexName: 'GSI1',
    partitionKey: { name: 'GSI1PK', type: dynamo.AttributeType.STRING },
    sortKey: { name: 'GSI1SK', type: dynamo.AttributeType.STRING },
    readCapacity: 1,
    writeCapacity: 1,
    projectionType: dynamo.ProjectionType.ALL,
  })
  table.grantReadWriteData(footwedgeApiLambda)

  return table
}
