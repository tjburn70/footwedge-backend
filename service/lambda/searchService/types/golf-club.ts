import { GolfCourse } from './golf-course'

interface GolfClub {
  readonly golf_club_id: string
  readonly golf_club_name: string
  readonly golf_courses?: GolfCourse[]
}

export { GolfClub }
