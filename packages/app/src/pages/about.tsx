import React from "react"

import Layout from "../components/layout"
import SEO from "../components/seo"

const SecondPage = () => (
  <Layout>
    <SEO title="About" />
    <h1>What is the WSB Explorer?</h1>
    <p>
      With over 9 million members at the time of writing, r/WallStreetBets is a
      significant source of data about "meme stocks" and retail investors as a
      whole. This project is intented to tap this source and provide an easier
      way to visualize this data.
    </p>
    <h1>What information does it provide?</h1>
    <p>
      Currently, it provide a list of stocks mentioned in r/WSB and how often
      they're mentioned.
    </p>
    <h1>Who made it?</h1>
    <p>Just a couple of dudes with 💎👐 who like to code.</p>
    <h1>Why did you make it?</h1>
    <p>
      To bring about the dogecoin revolution and overthrow all inferior
      currencies.
    </p>
  </Layout>
)

export default SecondPage
