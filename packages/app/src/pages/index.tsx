import React from "react"
import { Link } from "gatsby"
import styled from "@emotion/styled"

import Layout from "../components/layout"
import TickerCard from "../components/TickerCard"
import SEO from "../components/seo"

const data = {
  GME: {
    prev_daily_mentions: 200,
    daily_mentions: 300,
    weekly_mentions: 999,
    prev_weekly_mentions: 1,
  },
  AMZN: {
    prev_daily_mentions: 100,
    daily_mentions: 2,
    weekly_mentions: 69,
    prev_weekly_mentions: 420,
  },
  TSLA: {
    prev_daily_mentions: 123,
    daily_mentions: 420,
    weekly_mentions: 69420,
    prev_weekly_mentions: 1,
  },
}

const IndexPage = () => (
  <Layout>
    <SEO title="Home" />
    <h1>Activity</h1>
    <p>
      Here's the most recent activity from{` `}
      <a href="https://reddit.com/r/wallstreetbets">r/WallStreetBets</a>
    </p>
    <div>
      <div>
        <div>
          <h3
            style={{
              marginBottom: `.5rem`,
            }}
          >
            Most mentioned
          </h3>
          <p>The most mentioned stocks today</p>
        </div>
        <CardGrid>
          {Object.entries(data).map(([ticker, stats]) => (
            <TickerCard
              ticker={ticker}
              price={"420.69"}
              mentions={stats.daily_mentions}
              prevMentions={stats.prev_daily_mentions}
            />
          ))}
        </CardGrid>
      </div>
    </div>
  </Layout>
)

const CardGrid = styled.div`
  display: grid;
  align-items: center;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: 8fr;
  gap: 1.2rem 1.2rem;
  @media (max-width: 960px) {
    grid-template-columns: repeat(2, 1fr);
  }
  @media (max-width: 680px) {
    grid-template-columns: 1fr;
  }
`

export default IndexPage
