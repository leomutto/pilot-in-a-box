'use client'

import { useEffect } from "react"
import { initOTel } from "../otel"

export default function OTelClient() {
  useEffect(() => {
    initOTel()
  }, [])

  return null
}