import styles from './DoublesContainer.module.css';
import { doubles, search } from '../../signals/doublesSignals';
import { useSignals } from '@preact/signals-react/runtime';
import React from "react";

const DoublesContainer = () => {
    useSignals()
    return (
        <div className={styles.doublesCont}>
            {Object.entries(doubles.value).map(([number, accounts]) => {
                if (!number.includes(search.value) && search.value.length !== 0) {
                    return null;
                }
                return (
                    <div key={number} className={styles.group}>
                        <div className={styles.innerGroup}>
                            <div className={styles.numberContainer}>
                                <span className={styles.number}>{number}</span>
                            </div>
                            <div className={styles.accounts}>
                                {accounts.map((account) => (
                                    <div key={account.id} className={styles.account}>
                                        <span className={styles.accountCont}>
                                            {account.name || "Нет имени"}
                                        </span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                );
            })}
        </div>
    );
};

export default DoublesContainer;
