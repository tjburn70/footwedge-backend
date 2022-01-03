import axios from 'axios'
import qs from 'qs'
import * as aws from 'aws-sdk'
import { CognitoTokenRespBody, GolfClub, GolfCourse, TeeBox } from './types'

export async function getAccessToken(): Promise<string> {
  const cognitoDomain = process.env.COGNITO_DOMAIN
  const cognitoRegion = process.env.AWS_REGION
  const cognitoTokenUrl = `https://${cognitoDomain}.auth.${cognitoRegion}.amazoncognito.com/oauth2/token`
  const clientId = process.env.SCRAPE_SERVICE_COGNITO_CLIENT_ID
  const clientSecret = process.env.SCRAPE_SERVICE_COGNITO_CLIENT_SECRET

  const data = {
    grant_type: 'client_credentials',
    client_id: clientId,
    client_secret: clientSecret,
  }
  const headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
  }
  const resp = await axios.post(cognitoTokenUrl, qs.stringify(data), {
    headers,
  })
  const responseBody: CognitoTokenRespBody = resp.data
  return responseBody.access_token
}

export async function getGolfClubs(
  s3Client: aws.S3,
  params: aws.S3.GetObjectRequest[]
): Promise<GolfClub[]> {
  try {
    return await Promise.all(
      params.map(async (param) => {
        const result = await s3Client.getObject(param).promise()
        return JSON.parse(result.Body?.toString('utf-8') as string)
      })
    )
  } catch (err: unknown) {
    console.log(err)
    throw err
  }
}

export async function addGolfClubs(
  accessToken: string,
  baseFootwedgeUrl: string,
  golfClubs: GolfClub[]
): Promise<Record<string, GolfCourse[]>> {
  try {
    const golfClubMap: Record<string, GolfCourse[]> = {}
    await Promise.all(
      golfClubs.map(async (golfClub) => {
        const golfClubId = await addGolfClub(
          accessToken,
          baseFootwedgeUrl,
          golfClub
        )
        golfClubMap[golfClubId] = golfClub.courses
      })
    )
    return golfClubMap
  } catch (err: unknown) {
    console.log(err)
    throw err
  }
}

async function addGolfClub(
  accessToken: string,
  baseFootwedgeUrl: string,
  golfClub: GolfClub
): Promise<string> {
  const headers = {
    Authorization: `Bearer ${accessToken}`,
  }
  const url = `${baseFootwedgeUrl}/golf-clubs/`
  const data = {
    name: golfClub.golf_club_name,
    city: golfClub.city,
    state_code: golfClub.state_code,
  }
  const resp = await axios.post(url, data, {
    headers,
  })
  return resp.data.data.golf_club_id
}

export async function addGolfCourses(
  accessToken: string,
  baseFootwedgeUrl: string,
  golfCoursesByGolfClubId: Record<string, GolfCourse[]>
): Promise<Record<string, TeeBox[]>> {
  const golfCourseMap: Record<string, TeeBox[]> = {}
  await Promise.all(
    Object.keys(golfCoursesByGolfClubId).map(async (golfClubId) => {
      const golfCourses = golfCoursesByGolfClubId[golfClubId]
      try {
        await Promise.all(
          golfCourses.map(async (golfCourse) => {
            const golfCourseId = await addGolfCourse(
              accessToken,
              baseFootwedgeUrl,
              golfClubId,
              golfCourse
            )
            golfCourseMap[golfCourseId] = golfCourse.tee_boxes
          })
        )
        return golfCourseMap
      } catch (err: unknown) {
        console.log(err)
        throw err
      }
    })
  )

  return golfCourseMap
}

async function addGolfCourse(
  accessToken: string,
  baseFootwedgeUrl: string,
  golfClubId: string,
  golfCourse: GolfCourse
): Promise<string> {
  const headers = {
    Authorization: `Bearer ${accessToken}`,
  }
  const url = `${baseFootwedgeUrl}/golf-clubs/${golfClubId}/golf-courses`
  const data = {
    name: golfCourse.golf_course_name,
    num_holes: golfCourse.num_holes,
  }
  const resp = await axios.post(url, data, {
    headers,
  })
  return resp.data.data.golf_course_id
}

export async function addTeeBoxes(
  accessToken: string,
  baseFootwedgeUrl: string,
  teeBoxesByGolfCourseId: Record<string, TeeBox[]>
): Promise<void> {
  await Promise.all(
    Object.keys(teeBoxesByGolfCourseId).map(async (golfCourseId) => {
      const teeBoxes = teeBoxesByGolfCourseId[golfCourseId]
      try {
        await Promise.all(
          teeBoxes.map(async (teeBox) => {
            await addTeeBox(accessToken, baseFootwedgeUrl, golfCourseId, teeBox)
          })
        )
      } catch (err: unknown) {
        console.log(err)
        throw err
      }
    })
  )
}

async function addTeeBox(
  accessToken: string,
  baseFootwedgeUrl: string,
  golfCourseId: string,
  teeBox: TeeBox
) {
  const headers = {
    Authorization: `Bearer ${accessToken}`,
  }
  const url = `${baseFootwedgeUrl}/golf-courses/${golfCourseId}/tee-boxes`
  const data = {
    tee_box_color: teeBox.tee_box_color,
    gender: teeBox.gender,
    par: teeBox.par,
    distance: teeBox.distance,
    unit: teeBox.units,
    course_rating: teeBox.course_rating,
    slope: teeBox.slope,
  }
  const resp = await axios.post(url, data, {
    headers,
  })
  return resp.data.data.tee_box_id
}
