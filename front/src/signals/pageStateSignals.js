import { signal } from "@preact/signals-react"

export const WIN_STATES = {
    ADMIN: "admin",
    DOUBLES: "doubles"
}

export const winState = signal(WIN_STATES.DOUBLES)