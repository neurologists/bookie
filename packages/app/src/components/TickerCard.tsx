import React from "react"
import styled from "@emotion/styled"

export default function TickerCard({ ticker, price, mentions, prevMentions }) {
  return (
    <Card>
      <Heading>{ticker}</Heading>
      <Quote>{price}</Quote>
      <Mentions>
        Mentions: {mentions}
        {mentions > prevMentions ? "🔺" : "🔻"}
      </Mentions>
    </Card>
  )
}

const Card = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
  height: 100%;
  overflow: hidden;
  padding: 1rem;
  border: 2px solid #2f353c;
  border-radius: 15px;
  box-shadow: 0 1px 6px 0 rgba(0, 0, 0, 0.09);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
`

const Heading = styled.h3`
  display: flex;
  align-items: left;
  justify-content: left;
  margin-bottom: 0px;
  padding: 15px;
`

const Quote = styled.h1`
  display: flex;
  align-items: left;
  justify-content: left;
  margin-bottom: 0px;
  padding: 15px;
`
const Mentions = styled.h4`
  display: flex;
  align-items: left;
  justify-content: left;
  padding: 0px 15px 15px 15px;
  margin-bottom: 0px;
`
