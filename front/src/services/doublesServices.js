import { doubles, loading, entityType } from "../signals/doublesSignals";
import { fetchDoubles } from "../api/doublesApi";

export const getDoubles = async () => {
    if (loading.value)
        return
    doubles.value = {};
    loading.value = true;
    try {
        const response = await fetchDoubles(entityType.value);
        doubles.value = response;
    } catch (error) {
        console.log(`Ошибка: ${error}`);
    } finally {
        loading.value = false;
    }
};