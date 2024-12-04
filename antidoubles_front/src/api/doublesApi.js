import { TOKEN, BASE_URL } from "../config"


export const fetchDoubles = async (entityType) => {
    const response = await fetch(`${BASE_URL}/get_doubles`, {
        method: "POST",
        headers: {
            Authorization: `Bearer ${TOKEN}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            entity_type: entityType,
            search_type: "phone"
        })
    })
    if (response.ok) {
        return await response.json()
    } else {
        const errorBody = await response.json()
        if (errorBody.detail === "beasy") {
            throw new Error("beasy")
        }
        return {}
    }
}

export const getMe = async () => {
    const response = await fetch(`${BASE_URL}/me`, {
        method: "GET",
        headers: {
            Authorization: `Bearer ${TOKEN}`,
            "Content-Type": "application/json",
        },
    })
    return await response.json()
}

