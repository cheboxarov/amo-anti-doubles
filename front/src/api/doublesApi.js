import { TOKEN, SUBDOMAIN, BASE_URL } from "../config"


export const fetchDoubles = async (entityType) => {
    const response = await fetch(`${BASE_URL}/get_doubles/${SUBDOMAIN}/`, {
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