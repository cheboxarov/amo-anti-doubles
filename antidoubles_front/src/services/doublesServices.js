import { doubles, loading, entityType, me } from "../signals/doublesSignals";
import { fetchDoubles, getMe } from "../api/doublesApi";

export const getDoubles = async () => {
    if (loading.value)
        return
    doubles.value = {};
    loading.value = true;
    try {
        const response = await fetchDoubles(entityType.value);
        doubles.value = response.doubles;
    } catch (error) {
        console.log(`Ошибка: ${error}`);
    } finally {
        loading.value = false;
    }
};

export const updateMe = async() => {
    try {
        const response = await getMe()
        me.value = response
    } catch (error) {
        console.log("error to get me", error)
    }
}