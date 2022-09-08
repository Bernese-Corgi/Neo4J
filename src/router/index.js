import { Router } from "express";
import people from './people.routes.js'

const router = new Router()

router.use('/people', people)

export default router;
