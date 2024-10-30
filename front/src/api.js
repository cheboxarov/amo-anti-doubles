import { TOKEN, SUBDOMAIN, BASE_URL } from "./config"


export const fetchDoubles = async () => {
    const response = await fetch(`${BASE_URL}/get_doubles/${SUBDOMAIN}/`, {
        method: "POST",
        headers: {
            Authorization: `Bearer ${TOKEN}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            entity_type: "contacts",
            search_type: "phone"
        })
    })
    if (response.ok) {
        return await response.json()
    } else {
        return {}
    }
}