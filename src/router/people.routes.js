import { Router } from "express";
import neo4j from "neo4j-driver";
import recordLogger from "../logger.js";
import { getDriver } from "../neo4j.js";

const people = new Router()
const database = 'test'

people.post('/create', async (req, res) => {
  const driver = getDriver()

  try {    
    const { name, birthday } = req.body

    const session = driver.session({
      defaultAccessMode: neo4j.session.WRITE,
      database
    })

    const result = await session.writeTransaction(tx => {
      return tx.run(
        'CREATE (p:Person {name: $name, birthday: $birthday}) RETURN p',
        { name, birthday }
      )
    })

    const p = result.records[0].get('p')

    await session.close()
    
    res.send(result).json()

  } catch (error) {
    console.log(error);

    res.status(500).send(error)
  }
})

people.post('/makeFriends', async (req, res) => {
  try {
    const { follower, followee, relationship } = req.body

    const driver = getDriver()

    const session = driver.session({
      defaultAccessMode: neo4j.session.WRITE,
      database
    })

    const result = await session.writeTransaction(tx => {
      return tx.run(
        'MATCH (a:Person {name: $follower}) ' +
        'MATCH (b:Person {name: $followee}) ' +
        `MERGE (a)-[:${relationship}]->(b)`,
        { follower, followee }
      )
    })

    await session.close()

    res.send(result).json()

  } catch (error) {
    console.log(error)
    res.status(500)
  }
})

people.get('/findFriendships', async (req, res) => {
  try {
    const { search } = req.query

    const readSession = getDriver().session({
      defaultAccessMode: neo4j.session.READ,
      database
    })

    const result = await readSession.readTransaction(tx => {
      return tx.run(`MATCH (a)-[:FRIENDS]->(b) ${search === 'between' ? 'MATCH (b)-[:FRIENDS]->(a)' : ''} RETURN a.name, b.name`)
    })

    await readSession.close()

    res.send(result).json()

  } catch (error) {
    console.log(error)
    recordLogger('error', error)
    res.status(500)
  }
})

people.get('/followers', async (req, res) => {
  try {
    const { username, search } = req.query

    const readSession = getDriver().session({
      defaultAccessMode: neo4j.session.READ,
      database
    })

    const result = await readSession.readTransaction(tx => {
      return tx.run(
        `MATCH (a:Person)-[${search === 'all' ? '' : ':FOLLOW'}]->(b:Person {name: $name}) RETURN a`,
        { name: username }
      )
    })

    await readSession.close()

    res.send(result.records.map(v => v.get('a').properties)).json()

  } catch (error) {
    console.log(error)
    recordLogger('error', error)
    res.status(500)
  }
})

people.get('/hasDaughter', async (req, res) => {
  try {
    const readSession = getDriver().session({
      defaultAccessMode: neo4j.session.READ,
      database
    })

    const result = await readSession.readTransaction(tx => {
      return tx.run(
        `MATCH (a:Person)-[:DAUGHTER]->(b:Person) RETURN b`
      )
    })

    await readSession.close()

    res.send(result.records.map(v => v.get('b').properties)).json()
  } catch (error) {
    
  }
})

export default people;
