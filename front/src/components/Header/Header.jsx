import styles from "./Header.module.css"
import { doubles, search, loading, entityType, me } from "../../signals/doublesSignals";
import { useSignals } from "@preact/signals-react/runtime";
import { getDoubles } from "../../services/doublesServices";
import { FiSearch } from "react-icons/fi";
import React from "react";
import { WIN_STATES, winState } from "../../signals/pageStateSignals";

const Header = () => {

    useSignals()

    const adminHandle = () => {
        winState.value = WIN_STATES.ADMIN
    }

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
            { me.value && me.value.is_admin && (<button className={styles.button} onClick={adminHandle}>Админ панель</button>)}
        </div>
    )
}

export default Header