import algoliasearch from 'algoliasearch'

import { appConfig } from '../modules/config'
import type { GolfClub } from '../types/golf-club'
import type { GolfCourse } from '../types/golf-course'

const client = algoliasearch(appConfig.algoliaAppId, appConfig.algoliaApiKey)
const index = client.initIndex('golfClub')

type AlgoliaHit = {
  objectId: string
  golf_club_id: string
  golf_club_name: string
  golf_courses: GolfCourse[]
}

type AlgoliaHits = {
  hits: AlgoliaHit[]
}

type AlgoliaSaveObjectResult = {
  objectID: string
  taskID: number
}

const searchGolfClubs = async (searchText: string): Promise<GolfClub[]> => {
  const content: AlgoliaHits = await index.search(searchText)
  const golfClubs = content.hits.map((hit) => {
    return <GolfClub>{
      golf_club_id: hit.golf_club_id,
      golf_club_name: hit.golf_club_name,
      golf_courses: hit.golf_courses,
    }
  })
  return golfClubs
}

const addGolfClub = async (payload: GolfClub): Promise<string> => {
  const result: AlgoliaSaveObjectResult = await index.saveObject({
    objectID: payload.golf_club_id,
    ...payload,
  })
  return result.objectID
}

const getGolfClub = async (golfClubId: string): Promise<GolfClub> => {
  const golfClub: GolfClub = await index.getObject(golfClubId)
  return golfClub
}

const addGolfCourse = async (
  golfClubId: string,
  payload: GolfCourse
): Promise<string> => {
  const golfClub = await getGolfClub(golfClubId)
  const golfCourses = golfClub?.golf_courses ?? []
  golfCourses.push(payload)
  const result: AlgoliaSaveObjectResult = await index.partialUpdateObject({
    golf_courses: golfCourses,
    objectID: golfClubId,
  })
  return result.objectID
}

export { searchGolfClubs, addGolfClub, addGolfCourse }
