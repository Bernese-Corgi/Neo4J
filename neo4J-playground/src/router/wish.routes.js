import { Router } from "express";
import neo4j from "neo4j-driver";
import { getDriver } from "../neo4j.js";

const wish = new Router()
const database = 'test'