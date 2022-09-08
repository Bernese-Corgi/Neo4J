import { Router } from "express";
import people from './people.routes.js'
import want from "./want.routes.js";

const router = new Router()

router.use('/people', people)
router.use('/want', want)

export default router;
