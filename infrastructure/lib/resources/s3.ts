import * as s3 from '@aws-cdk/aws-s3'
import * as sns from '@aws-cdk/aws-sns'
import * as s3n from '@aws-cdk/aws-s3-notifications'
import * as cdk from '@aws-cdk/core'

export function generateGolfClubSourceBucket(
  scope: cdk.Construct,
  bucketName: string,
  golfClubTopic: sns.Topic
): s3.Bucket {
  const bucket = new s3.Bucket(scope, 'FootwedgeGolfClubSourceBucket', {
    bucketName: bucketName,
    versioned: true,
    encryption: s3.BucketEncryption.S3_MANAGED,
  })

  bucket.addEventNotification(
    s3.EventType.OBJECT_CREATED_PUT,
    new s3n.SnsDestination(golfClubTopic)
  )

  return bucket
}
