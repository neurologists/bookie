/**
 * Implement Gatsby's Browser APIs in this file.
 *
 * See: https://www.gatsbyjs.com/docs/browser-apis/
 */

// You can delete this file if you're not using it

import React from "react"
import { WSBDataProvider } from "./src/components/WSBDataProvider"

const wrapRootElement = ({ element }) => {
  return <WSBDataProvider>{element}</WSBDataProvider>
}

export { wrapRootElement }
