import {
  SQSHandler,
  SQSEvent,
  SQSRecord,
  SNSMessage,
  S3Event,
  S3EventRecord,
} from 'aws-lambda'
import * as aws from 'aws-sdk'
import {
  getAccessToken,
  getGolfClubs,
  addGolfClubs,
  addGolfCourses,
  addTeeBoxes,
} from './helper'

export const handler: SQSHandler = async (event: SQSEvent) => {
  const params = parseEvent(event)
  console.log(`Fetching from S3: ${JSON.stringify(params)}`)
  const s3Client = new aws.S3()
  const golfClubs = await getGolfClubs(s3Client, params)

  console.log(`Golf clubs to upload: ${golfClubs}`)
  const envName = process.env.ENV_NAME || 'dev'
  const accessToken = await getAccessToken(envName)
  const footwedgeBaseUrl = 'https://api.footwedge.io/v1'
  const golfCoursesByGolfClubId = await addGolfClubs(
    accessToken,
    footwedgeBaseUrl,
    golfClubs
  )
  console.log(
    `Golf Courses by Golf Club ID: ${JSON.stringify(golfCoursesByGolfClubId)}`
  )
  const teeBoxesByGolfCourseId = await addGolfCourses(
    accessToken,
    footwedgeBaseUrl,
    golfCoursesByGolfClubId
  )
  console.log(
    `Tee Boxes by Golf Course ID: ${JSON.stringify(teeBoxesByGolfCourseId)}`
  )
  await addTeeBoxes(accessToken, footwedgeBaseUrl, teeBoxesByGolfCourseId)
}

function parseEvent(event: SQSEvent): aws.S3.GetObjectRequest[] {
  return event.Records.map((record: SQSRecord) => {
    const snsMessage: SNSMessage = JSON.parse(record.body)
    const s3Event: S3Event = JSON.parse(snsMessage.Message)
    const s3Record: S3EventRecord = s3Event.Records[0]
    return {
      Bucket: s3Record.s3.bucket.name,
      Key: decodeURIComponent(s3Record.s3.object.key),
    }
  })
}
