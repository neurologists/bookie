import React, { useState, useEffect, useContext } from "react"

const WSBDataContext = React.createContext({})

interface TickerData {
  prev_daily_mentions: number
  daily_mentions: number
  weekly_mentions: number
  prev_weekly_mentions: number
}

type GMEData = { [ticker: string]: TickerData }

const WSBDataProvider: React.FC<{}> = ({ children }) => {
  const [data, setData] = useState<GMEData>({})

  const loadData = () => {
    fetch("https://ledger.nyc3.digitaloceanspaces.com/data.json")
      .then(response => {
        if (!response.ok) {
          throw new Error("Failed to fetch data!")
        }
        return response.json()
      })
      .then(WSBdata => {
        setData(WSBdata)
      })
  }

  useEffect(loadData, [])

  return (
    <WSBDataContext.Provider value={data}>{children}</WSBDataContext.Provider>
  )
}

const useWSBData = () => useContext(WSBDataContext)

export { WSBDataProvider, useWSBData }
