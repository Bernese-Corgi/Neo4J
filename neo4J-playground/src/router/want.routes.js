import neo4j from "neo4j-driver";
import { Router } from "express";
import { getDriver } from "../neo4j.js";

const want = new Router()

const database = 'test'

want.post('/create', async (req, res) => {
  const session = getDriver().session({
    defaultAccessMode: neo4j.session.WRITE,
    database
  })

  try {
    const { name } = req.body

    const result = await session.writeTransaction(tx => {
      return tx.run(
        'CREATE (p:Want {name: $name}) RETURN p',
        { name }
      )
    })

    await session.close()

    res.send(result).json()
  } catch (error) {
    console.log(error)
    res.status(500)
  }
})

want.post('/followWant', async (req, res) => {
  const session = getDriver().session({
    defaultAccessMode: neo4j.session.WRITE,
    database
  })

  try {
    const { follower, want } = req.body

    const result = await session.writeTransaction(tx => {
      return tx.run(
        'MATCH (a:Person {name: $follower}) ' +
        'MATCH (b:Want {name: $want}) ' +
        `MERGE (a)-[:WANT]->(b)`,
        { follower, want }
      )
    })

    await session.close()

    res.send(result).json()
  } catch (error) {
    console.log(error)
    res.status(500)
  }
})

export default want;
