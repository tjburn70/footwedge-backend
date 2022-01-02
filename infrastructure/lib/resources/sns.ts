import * as sns from '@aws-cdk/aws-sns'
import * as cdk from '@aws-cdk/core'
import * as sqs from '@aws-cdk/aws-sqs'
import * as subscriptions from '@aws-cdk/aws-sns-subscriptions'

export function generateNewGolfClubTopic(
  scope: cdk.Construct,
  golfClubQueue: sqs.Queue
): sns.Topic {
  const newGolfClubTopic = new sns.Topic(scope, 'newGolfClubTopic')
  newGolfClubTopic.addSubscription(
    new subscriptions.SqsSubscription(golfClubQueue)
  )
  return newGolfClubTopic
}
