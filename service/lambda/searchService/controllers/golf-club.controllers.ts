import type { Request, Response } from 'express'

import {
  addGolfClub,
  addGolfCourse,
  searchGolfClubs,
} from '../services/golf-club.services'

const addGolfClubHandler = async (request: Request, response: Response) => {
  try {
    const result = await addGolfClub(request.body)
    return response.status(201).send({ golf_club_id: result })
  } catch (error: unknown) {
    console.log(error)
    return response.status(500).send('Internal Server Error')
  }
}

const addGolfCourseHandler = async (request: Request, response: Response) => {
  try {
    const result = await addGolfCourse(request.params.golfClubId, request.body)
    return response.send({
      message: 'successfully added golf course',
      golf_club_id: result,
    })
  } catch (error: unknown) {
    console.log(error)
    return response.status(500).send('Internal Server Error')
  }
}

const searchGolfClubHandler = async (request: Request, response: Response) => {
  try {
    const searchText = request.query.search as string
    if (!searchText) {
      return response.status(400).send("Missing required query param: 'search'")
    }
    const golfClubs = await searchGolfClubs(searchText)
    return response.status(200).send(golfClubs)
  } catch (error: unknown) {
    console.log(error)
    return response.status(500).send('Internal Server Error')
  }
}

export { addGolfClubHandler, addGolfCourseHandler, searchGolfClubHandler }
