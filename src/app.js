import express from "express"
import cors from "cors"
import bodyParser from "body-parser"
import { initDriver } from './neo4j.js'
import { config } from "dotenv"

const app = express()

/* ------------------------------ middle wares ------------------------------ */
config()
app.use(cors())
app.use(bodyParser.json())

/* ---------------------------------- neo4j --------------------------------- */
const {
  NEO4J_URI,
  NEO4J_USERNAME,
  NEO4J_PASSWORD,
} = process.env

initDriver(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

export default app