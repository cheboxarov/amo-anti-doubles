import styles from "./Header.module.css"
import { doubles, search, loading, entityType } from "../../signals/doublesSignals";
import { useSignals } from "@preact/signals-react/runtime";
import { getDoubles } from "../../services/doublesServices";
import { FiSearch } from "react-icons/fi";

const Header = () => {

    useSignals()

    return (
        <div className={styles.header}>
            <div>
                <button className={styles.button} onClick={getDoubles}>Поиск дублей</button>
                <select
                    className={styles.selectEntity}
                    onChange={(e) => { entityType.value = e.target.value }}
                >
                    <option value="contacts">Контакты</option>
                    <option value="companies">Компании</option>
                </select>
            </div>
            <div className={styles.outerInput}>
                <input
                    className={styles.searchInput}
                    value={search.value}
                    onInput={(e) => { search.value = e.target.value }}
                />
                <div className={styles.searchIcon}><FiSearch /></div>
            </div>
            {Object.keys(doubles.value).length == 0 ? (<div>Дубли не найдены</div>) : (<div>Общее кол-во дублей: {Object.keys(doubles.value).length}</div>)}
        </div>
    )
}

export default Header