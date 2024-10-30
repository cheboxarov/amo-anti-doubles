import React, { useState } from 'react';
import styles from './App.module.css';
import { fetchDoubles } from './api';
import Spinner from './components/spinner/Spinner';

function App() {
    const [doubles, setDouble] = useState({});
    const [loading, setLoading] = useState(false);
    const [search, setSearch] = useState("");

    const handleGetDoubles = async () => {
        setLoading(true);
        const doubles = await fetchDoubles();
        setDouble(doubles);
        setLoading(false);
    };

    if (loading) {
        return (
            <div className={styles.App}>
                <Spinner />
            </div>
        );
    }

    return (
        <div className={styles.App}>
            <div className={styles.header}>
                <button 
                    className={styles.button} 
                    onClick={handleGetDoubles}
                >
                    Поиск дублей
                </button>
                <input className={styles.searchInput} value={search} onInput={(e) => { setSearch(e.target.value) }} />
                <div>Общее кол-во дублей: {Object.keys(doubles).length}</div>
            </div>
            <div className={styles.doublesCont}>
                {Object.entries(doubles).map(([number, accounts]) => {
                    if (!number.includes(search) && search.length != 0) {
                        return null
                    }
                    return (
                        <div key={number} className={styles.group}>
                            <div className={styles.verticalLine}></div>
                            <div className={styles.innerGroup}>
                                <div className={styles.numberContainer}>
                                    <span className={styles.number}>{number}</span>
                                </div>
                                <div className={styles.accounts}>
                                    {accounts.map((account, index) => (
                                        <div key={account.id} className={styles.account}>
                                            <span>{account.name} (ID: {account.id})</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                        )
                })}
            </div>
        </div>
    );
}

export default App;
