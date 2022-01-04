import * as sqs from '@aws-cdk/aws-sqs'
import * as cdk from '@aws-cdk/core'

export function generateGolfClubQueue(scope: cdk.Construct) {
  return new sqs.Queue(scope, 'GolfClubQueue', {
    visibilityTimeout: cdk.Duration.minutes(5),
    deadLetterQueue: {
      queue: new sqs.Queue(scope, 'GolfClubQueueDLQ'),
      maxReceiveCount: 2,
    }
  })
}

export function generateDynamoStreamsDeadLetterQueue(scope: cdk.Construct) {
  return new sqs.Queue(scope, 'FootwedgeDynamoStreamsDLQ')
}
